"""Define all the orchestration functionality required by the program to work.

Classes and functions that connect the different domain model objects with the adapters
and handlers to achieve the program's purpose.
"""

import logging
import os
import re
import sqlite3
import subprocess  # nosec
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional, Union
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, epub
from org_rw import dumps, loads

from .model import AnkiNote, Book, Highlight, Section

if TYPE_CHECKING:
    from .adapters.anki import Anki


log = logging.getLogger(__name__)


def extract_epub_data(epub_path: Path) -> Book:
    """Extract the TOC, title, and author from an EPUB file.

    This function loads the EPUB file from the given path, extracts the TOC,
    title, and author, and returns them in a Book Pydantic model.

    Args:
        epub_path (Path): Path to the EPUB file.

    Returns:
        Book: A Pydantic model containing the title, author, and a nested list
        representing the TOC.
    """
    log.info(f"Extracting data from EPUB file at {epub_path}")
    book = epub.read_epub(str(epub_path), options={"ignore_ncx": True})
    title = book.get_metadata("DC", "title")[0][0]
    try:
        author = book.get_metadata("DC", "creator")[0][0]
    except IndexError:
        author = "unknown"
    toc_sections = parse_toc_as_list(book.toc, book)

    return Book(title=title, author=author, toc=toc_sections)


def parse_toc_as_list(
    toc: List[Union[epub.Link, tuple]], book: epub.EpubBook  # type: ignore
) -> List[Section]:
    """Parse the TOC from the EPUB file and return it as a nested list of Section models.

    This function iterates over the TOC entries and organizes them into a
    nested list of Section models. Chapters with sub-sections are represented
    as nested Section models.

    Args:
        toc (List[Union[epub.Link, tuple]]): The TOC data from the EPUB file,
        which can contain links and nested sections.
        book (epub.EpubBook): The full EPUB book object.

    Returns:
        List[Section]: A nested list of Section models representing the TOC,
        where chapters with sub-sections are nested Section models.
    """
    sections = []
    for item in toc:
        if isinstance(item, epub.Link):
            section_text = get_section_text(book, item.href)
            sections.append(
                Section(id=item.href, title=item.title, content=section_text)
            )
        elif isinstance(item, tuple) and isinstance(item[0], epub.Section):
            section_title = item[0].title
            section_id = item[0].href if hasattr(item[0], "href") else section_title
            sub_sections = parse_toc_as_list(item[1], book)
            sections.append(
                Section(id=section_id, title=section_title, sections=sub_sections)
            )
    return sections


def get_section_text(book: epub.EpubBook, href: str) -> str:
    """Get the full text content of a section from its href in the EPUB.

    Args:
        book (epub.EpubBook): The full EPUB book object.
        href (str): The href (link) to the section within the EPUB.

    Returns:
        str: The full text content of the section.
    """
    log.debug(f"Getting section text for href: {href}")
    # Remove any fragment identifiers from the href
    href_without_fragment = urlparse(href).path

    for item in book.items:
        if item.get_type() == ITEM_DOCUMENT and item.file_name == href_without_fragment:
            # Decode the HTML content
            html_content = item.get_body_content().decode("utf-8")
            # Use BeautifulSoup to strip HTML tags and return plain text
            return BeautifulSoup(html_content, "html.parser").get_text()
    log.warning(f"Section text not found for href: {href}")
    return ""


def convert_toc_to_org(book: Book, initial_level: int = 1) -> str:
    """Convert a nested TOC list into an Org-mode formatted string.

    This function takes a Book model and converts its TOC into an Org-mode
    formatted string with headline items. The initial heading level for the headline
    items can be specified.

    Args:
        book (Book): The Book model containing the title, author, and chapters.
        initial_level (int): The starting level of headings for headline items.

    Returns:
        str: A string formatted for Org-mode with headline items for each chapter
        and sub-section.
    """
    log.info("Converting TOC to Org-mode format")
    org_representation = []

    # Titles to disregard in the Org-mode export
    ignore_patterns = {
        "cover",
        "title page",
        "front endpapers",
        "illustrations",
        "copyright",
        "dedication",
        "contents",
        "references",
        "index",
        "foreword.*",
        "acknowled.*",
        "glossary.*",
        "epilogue",
        "postscript",
        "epigraph",
        "back cover",
        "about the.*",
        "also by.*",
        "notes",
        "cubierta",
        "portada",
        "créditos",
        "índice",
        "prólogo",
    }

    # Compile regex patterns
    ignore_patterns_compiled = [
        re.compile(pattern, re.IGNORECASE) for pattern in ignore_patterns
    ]
    # Add the book title and author as the top-level heading
    org_representation.append(f"{'*' * initial_level} {book.title} by {book.author}")

    def format_toc(sections: List[Section], level: int) -> None:
        for section in sections:
            # Skip sections with titles in the ignore list
            if any(
                pattern.match(section.title) for pattern in ignore_patterns_compiled
            ):
                log.debug(f"Skipping section: {section.title}")
                continue
            org_representation.append(f"{'*' * level} {section.title}")
            if section.sections:
                format_toc(section.sections, level + 1)

    format_toc(book.toc, initial_level + 1)

    return "\n".join(org_representation)


def update_orgmode_file(books_orgmode_path: Path, toc_org: str) -> None:
    """Update the Org-mode file with new TOC content.

    This function reads the current contents of the Org-mode file if it exists,
    prepends the new TOC content, and writes the updated content back to the file.

    Args:
        books_orgmode_path (Path): Path to the Org-mode file to be updated.
        toc_org (str): The new TOC content to prepend to the file.

    Raises:
        IOError: If an error occurs during file reading or writing.
    """
    if books_orgmode_path.exists():
        try:
            with open(books_orgmode_path, "r", encoding="utf8") as file:
                current_content = file.read()
        except IOError as e:
            log.error(f"Error reading file {books_orgmode_path}: {e}")
            raise
    else:
        log.warning(
            f"I could not find the {books_orgmode_path} document, creating a new one"
        )
        current_content = ""

    try:
        log.info(f"Adding the book TOC to the {books_orgmode_path}")
        with open(books_orgmode_path, "w", encoding="utf8") as file:
            file.write(toc_org + "\n\n" + current_content)
    except IOError as e:
        log.error(f"Error writing to file {books_orgmode_path}: {e}")
        raise


def is_device_mounted(device_path: Path, mount_point: Path) -> bool:
    """Check if the device is already mounted at the specified mount point.

    Args:
        device_path (Path): The path to the device.
        mount_point (Path): The mount point to check.

    Returns:
        bool: True if the device is mounted at the mount point, False otherwise.
    """
    try:

        result = subprocess.run(  # nosec
            subprocess.list2cmdline(
                ["findmnt", "--source", str(device_path), "--target", str(mount_point)]
            ),
            capture_output=True,
            text=True,
            check=True,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def mount_ereader(mount_point: Path) -> None:  # noqa: M511, B008
    """Detects and mounts an e-reader device to the specified mount point.

    This function detects connected e-reader devices based on common USB device
    identifiers and mounts the detected device to the given mount point.

    Args:
        mount_point (Path): The directory where the e-reader should be mounted.
            Defaults to '/mnt'.

    Raises:
        RuntimeError: If no e-reader device is found or if mounting fails.
        subprocess.CalledProcessError: If the subprocess commands fail.
    """
    log.info(f"Attempting to mount e-reader to {mount_point}")

    # Run lsblk to get a list of devices
    try:
        result = subprocess.run(  # nosec
            ["lsblk", "-o", "NAME,TRAN"], capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        log.error(f"Failed to list devices: {e}")
        raise RuntimeError("Failed to list devices") from e

    devices = result.stdout

    # Regex pattern for detecting e-reader devices based on common USB transport
    usb_pattern = re.compile(r"(sd[b-z]+)\s+usb")

    # Check for e-reader devices
    device_match = usb_pattern.search(devices)
    if not device_match:
        raise RuntimeError("No e-reader device found.")

    device_name = device_match.group(1)
    device_path = Path(f"/dev/{device_name}")

    # Create the mount point directory if it does not exist
    mount_point.mkdir(parents=True, exist_ok=True)

    # Check if the device is already mounted at the mount point
    if is_device_mounted(device_path, mount_point):
        log.info(f"Device {device_path} is already mounted at {mount_point}")
        return

    # Check if we have permissions to write to the mount point
    if not mount_point.is_dir() or not os.access(mount_point, os.W_OK):
        log.error(f"Mount point {mount_point} is not writable")
        raise RuntimeError(
            f"Mount point {mount_point} is not writable. Check permissions."
        )

    # Mount the device
    try:
        # DUO116: use of "shell=True" is insecure in "subprocess" module
        # The input is already cleaned by list2cmdline and it fails if it's not enabled
        subprocess.run(  # noqa: DUO116 # nosec
            subprocess.list2cmdline(
                ["sudo", "mount", str(device_path), str(mount_point)]
            ),
            check=True,
            shell=True,
        )
        log.info(f"Mounted {device_path} to {mount_point}")

    except subprocess.CalledProcessError as e:
        log.error(f"Failed to mount device {device_path}: {e}")
        raise RuntimeError(
            f"Failed to mount device {device_path}. You might need to run"
            "this script with superuser privileges."
        ) from e


def find_epub_path(title_regexp: str, mount_point: Path) -> Path:
    """Search for an EPUB file within the mount point that matches the title regexp."""
    pattern = re.compile(title_regexp, re.IGNORECASE)

    # Traverse the mount point to find a matching file using pathlib
    for epub_file in mount_point.rglob("*.epub"):
        if pattern.search(epub_file.name):
            return epub_file

    raise FileNotFoundError(f"No ePub file found matching title regexp: {title_regexp}")


def copy_epub_to_mount(epub_path: Path, mount_point: Path) -> None:
    """Copy an EPUB file to the mounted e-reader device.

    This function copies the specified EPUB file to the mounted e-reader device.
    It uses sudo to ensure the file is copied with the correct permissions.
    It checks if the file already exists and if it is the same before copying.

    Args:
        epub_path (Path): The path to the EPUB file.
        mount_point (Path): The mount point where the e-reader device is mounted.

    Raises:
        RuntimeError: If copying fails.
    """
    destination_file = mount_point / epub_path.name
    log.info(f"Copying EPUB file {epub_path} to {destination_file}")

    # Check if the file already exists at the destination
    if (
        destination_file.exists()
        and destination_file.stat().st_size == epub_path.stat().st_size
    ):
        log.info(f"File {destination_file} already exists and is up-to-date.")
        return

    # Copy the file using sudo to ensure correct permissions
    try:
        subprocess.run(  # nosec
            ["sudo", "cp", str(epub_path), str(destination_file)],
            check=True,
        )
        log.info(f"Successfully copied {epub_path} to {destination_file}")
    except subprocess.CalledProcessError as e:
        log.error(f"Failed to copy EPUB file to {destination_file}: {e}")
        raise RuntimeError(f"Failed to copy EPUB file to {destination_file}.") from e


def find_kobo_sqlite(mount_point: Path) -> Optional[Path]:
    """Find the KoboReader.sqlite path on the mount point.

    Args:
        mount_point (Path): The directory where the e-reader is mounted.

    Returns:
        Optional[Path]: The path to the KoboReader.sqlite file if found, otherwise None.
    """
    for file_path in mount_point.rglob(".kobo/KoboReader.sqlite"):
        return file_path
    return None


def extract_highlights(sqlite_path: str, book_title: str) -> List[Highlight]:
    """Extract highlights from a SQLite database for a given book title.

    This function connects to a SQLite database and extracts highlights
    from the `Bookmark` table where the `ContentID` matches the provided
    book title. The search is case-insensitive. The `StartContainerPath`
    is parsed to extract the section ID and position.

    Args:
        sqlite_path (str): The path to the SQLite database file.
        book_title (str): The title of the book to match in the `ContentID`.

    Returns:
        List[Highlight]: A list of Highlight objects, each containing the
        section ID, position, and highlight text. Example:

        Highlight(
          section_id='Burk_9780735232464_epub3_c02_r1.xhtml',
          position='/1/4/2/34/3:128',
          text='It’s an attempt to devour'
        )
    """
    log.debug("Cleaning the book title")
    book_title = re.sub(r"[^a-zA-Z0-9 ]", "", book_title)
    log.debug(f"Connecting to SQLite database at: {sqlite_path}")
    conn = sqlite3.connect(sqlite_path)
    cursor = conn.cursor()

    query = """
    SELECT StartContainerPath, Text FROM Bookmark
    WHERE ContentID LIKE ?
    """
    log.debug(f"Executing query: {query} on %{book_title}%")
    cursor.execute(query, (f"%{book_title}%",))

    rows = cursor.fetchall()
    if len(rows) == 0:
        log.warning("Number of highlights found: %d", len(rows))
    else:
        log.debug("Number of highlights found: %d", len(rows))

    def parse_start_container_path(path: str) -> tuple[str, str]:
        """Parse the StartContainerPath to extract the section ID and position.

        Args:
            path (str): The StartContainerPath containing section ID and position.

        Returns:
            Tuple[str, str]: The section ID and position extracted from the path.
        """
        section_id, position = path.split("#", 1)
        section_id = section_id.split("/")[-1]  # Extract the filename
        position = position.split("point(")[-1].rstrip(")")  # Extract the position
        return section_id, position

    highlights = []
    for start_container_path, text in rows:
        if text is None:
            continue
        section_id, position = parse_start_container_path(start_container_path)
        highlights.append(
            Highlight(section_id=section_id, position=position, text=text)
        )

    conn.close()
    log.debug("Closed connection to SQLite database")

    return highlights


def match_highlights_to_sections(book: Book, highlights: List[Highlight]) -> Book:
    """Match highlights extracted from an EPUB's SQLite database to sections.

    Sectios in the book's TOC based on section IDs and update the Book object with these
    highlights.

    Args:
        book (Book): The Book object containing the TOC and other details.
        highlights (List[Highlight]): List of Highlight objects extracted from
            the SQLite database.

    Returns:
        Book: The updated Book object with highlights added to each section.
    """

    def get_section_by_id(section_id: str) -> Optional[Section]:
        """Find and return a section from the book's TOC based on the section ID."""
        # Extract the filename from the section_id
        file_name = section_id.split("/")[-1].strip()

        # Iterate through the sections in the book's TOC
        for section in book.toc:
            if file_name == section.id.split("/")[-1]:
                return section

            for sub_section in section.sections:
                if file_name == sub_section.id.split("/")[-1]:
                    return sub_section
        return None

    for highlight in highlights:
        section = get_section_by_id(highlight.section_id)
        if section:
            section.highlights.append(highlight)

    return book


def convert_highlights_to_org(book: Book, initial_level: int = 1) -> str:
    """Convert sections with highlights to an Org-mode formatted string.

    This function takes a Book model and converts its sections that contain
    highlights into an Org-mode formatted string. Only sections with highlights
    are included in the output, including their subsections.

    Args:
        book (Book): The Book model containing the title, author, and chapters.
        initial_level (int): The initial heading level for the book title.

    Returns:
        str: A string formatted for Org-mode with headline items and highlights
        for each section and subsection that contains highlights.
    """

    def format_section(section: Section, level: int) -> str:
        """Format a single section and its highlights into Org-mode.

        Args:
            section (Section): The section to format.
            level (int): The heading level in Org-mode.

        Returns:
            str: The Org-mode formatted string for the section.
        """
        org_representation = []

        # Only include the section if it has highlights or
        # if any of its subsections have highlights
        if section.highlights or any(
            sub_section.highlights for sub_section in section.sections
        ):
            org_representation.append(f"{'*' * level} {section.title}")

            if section.highlights:
                for highlight in sorted(section.highlights):
                    org_representation.append(f"{' ' * (level + 1)}- {highlight.text}")

            for sub_section in section.sections:
                formatted_sub_section = format_section(sub_section, level + 1)
                if formatted_sub_section:
                    org_representation.append(formatted_sub_section)

        return "\n".join(org_representation)

    # Add the book title and author as the top-level heading
    org_representation = [f"{'*' * initial_level} {book.title} by {book.author}"]

    for section in book.toc:
        formatted_section = format_section(section, initial_level + 1)
        if formatted_section:
            org_representation.append(formatted_section)

    return "\n".join(org_representation)


def parse_anki_notes(org_file: Path, deck: str = "Default") -> List[AnkiNote]:
    """Parse an orgmode file and create AnkiNote objects.

    This function reads an orgmode file, processes each headline, and creates an
    AnkiNote object for each. The note is tagged with 'automatic'. Depending on the
    content, it assigns the appropriate Anki model (Basic or Basic (and reversed
    card)).

    Args:
        org_file (Path): Path to the orgmode file.

    Returns:
        List[AnkiNote]: List of created AnkiNote objects.
    """
    notes = []

    log.info(f"Starting to parse the orgmode file: {org_file}")

    doc = loads(org_file.read_text(encoding="utf-8"))

    for headline in doc.headlines:
        front_content = headline.title.get_text()
        if len(headline.get_lists()) > 0:
            back_content = "\n- " + "\n- ".join(
                element.content[0] for element in headline.get_lists()[0]
            )
        else:
            back_content = "\n".join(
                [content.get_text() for content in headline.contents]
            ).strip()
        tags = ["automatic"]

        if "?" in back_content:
            log.debug("Detected question mark in the title, using reversed model.")
            anki_model = "Basic (and reversed card)"
        else:
            log.debug("No question mark detected in the title, using Basic model.")
            anki_model = "Basic"

        fields = {"Front": front_content, "Back": back_content}
        note = AnkiNote(
            anki_model=anki_model,
            fields=fields,
            tags=tags,
            deck=deck,
        )

        log.info(f"Created AnkiNote with model: {anki_model}, fields: {fields}")
        notes.append(note)

    log.info(f"Finished parsing the orgmode file. Total notes created: {len(notes)}")
    return notes


def create_anki_notes(notes: List[AnkiNote], anki: "Anki") -> None:
    """Adds a list of Anki notes to the Anki application.

    Args:
        notes (List[AnkiNote]): A list of AnkiNote objects to be added.
        adapter (Anki): The adapter used to interact with Anki.

    Returns:
        None

    Raises:
        Exception: If an error occurs while adding notes.
    """
    try:
        log.debug(f"Attempting to add {len(notes)} notes to Anki.")
        anki.add_notes(notes)
        log.info(f"Successfully added {len(notes)} notes to Anki.")
        anki.sync()
    except Exception as e:
        log.error(f"Failed to add notes to Anki: {e}")
        raise


def remove_anki_notes_from_org_file(
    notes_to_remove: List[AnkiNote], org_file: Path
) -> None:
    """Remove Anki notes from an orgmode file.

    Args:
        notes_to_remove (List[AnkiNote]): List of AnkiNote objects to remove.
        org_file (Path): Path to the orgmode file from which notes will be removed.

    Raises:
        FileNotFoundError: If the org_file does not exist.
        IOError: If there is an error reading or writing the org_file.
    """
    log.info(f"Removing notes from {org_file}")

    # Check if the file exists
    if not org_file.is_file():
        log.error(f"The file {org_file} does not exist.")
        raise FileNotFoundError(f"The file {org_file} does not exist.")

    try:
        # Load the orgmode file
        doc = loads(org_file.read_text())

        # Remove headlines that match any note to remove
        for note in notes_to_remove:
            for headline in doc.headlines:
                if note.fields.get("Front", "") in headline.title.get_text():
                    doc.headlines.remove(headline)
                    log.info(f"Marking '{headline.title.get_text()}' for removal.")

        # Write the updated document back to the file
        org_file.write_text(dumps(doc), encoding="utf8")
        log.info(f"File {org_file} updated.")

    except IOError as e:
        log.error(f"Error reading or writing the file {org_file}: {e}")
        raise
