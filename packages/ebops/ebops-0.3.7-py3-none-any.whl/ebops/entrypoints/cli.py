"""Define the command line interface."""

import logging
import shutil
import tempfile
from pathlib import Path
from typing import Optional

import typer

from ebops.adapters.anki import Anki

from .. import services
from . import utils

log = logging.getLogger(__name__)
cli = typer.Typer()


@cli.callback()
def main(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(  # noqa: W0613, M511, B008
        None, "--version", callback=utils.version_callback, is_eager=True
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    """Manage e-book and org files to make analytical reading easy."""
    ctx.ensure_object(dict)
    utils.load_logger(verbose)


@cli.command()
def load(
    epub_path: Path,
    mount_point: Optional[Path] = None,
    books_orgmode_path: Optional[Path] = typer.Option(
        None, "--learn-orgmode-path", envvar="BOOKS_ORGMODE_PATH"
    ),
) -> None:
    """Load an EPUB document, mount an e-reader, and update an Org-mode file.

    Args:
        epub_path (Path): The path to the EPUB document to load.
        mount_point (Path, optional): The directory where the e-reader should
            be mounted. Defaults to /mnt.
        books_orgmode_path (Path, optional): The path to the Org-mode file to update.
            If not provided, uses the environment variable BOOKS_ORGMODE_PATH.
    """
    if books_orgmode_path is None:
        log.error(
            "No path provided and BOOKS_ORGMODE_PATH environment variable is not set."
        )
        raise ValueError(
            "No path provided and BOOKS_ORGMODE_PATH environment variable is not set."
        )
    if not mount_point:
        mount_point = Path(tempfile.mkdtemp())
    services.mount_ereader(mount_point)
    services.copy_epub_to_mount(epub_path, mount_point)

    # Convert TOC to Org-mode formatted string
    book = services.extract_epub_data(epub_path)
    toc_org = services.convert_toc_to_org(book)

    services.update_orgmode_file(books_orgmode_path, toc_org)


@cli.command()
def export_highlights(
    title_regexp: str,
    mount_point: Optional[Path] = None,
    learn_orgmode_path: Optional[Path] = typer.Option(
        None, "--learn-orgmode-path", envvar="LEARN_ORGMODE_PATH"
    ),
) -> None:
    """Export highlights from an EPUB to an Org-mode file.

    Args:
        mount_point (Path): The mount point where the e-reader is connected.
        title_regexp (str): The regular expression to find a title in the available
            ebooks.
        learn_orgmode_path (Optional[Path]): The path to the Org-mode file to save
            highlights. Defaults to the LEARN_ORGMODE_PATH environment variable if
            not provided.
    """
    if learn_orgmode_path is None:
        log.error(
            "No path provided and LEARN_ORGMODE_PATH environment variable is not set."
        )
        raise ValueError(
            "No path provided and LEARN_ORGMODE_PATH environment variable is not set."
        )
    if not mount_point:
        mount_point = Path(tempfile.mkdtemp())

    services.mount_ereader(mount_point)

    epub_path = services.find_epub_path(title_regexp, mount_point)
    log.info(f"Found EPUB: {epub_path}")

    log.debug("Finding KoboReader.sqlite...")
    sqlite_path = services.find_kobo_sqlite(mount_point)
    if sqlite_path is None:
        log.error("KoboReader.sqlite not found.")
        raise FileNotFoundError("KoboReader.sqlite not found.")
    log.info(f"Found Kobo sqlite at {sqlite_path}")

    # Create a temporary directory for the SQLite copy as the original is readonly
    with tempfile.TemporaryDirectory() as temp_dir:
        log.info("Extracting EPUB data...")
        book = services.extract_epub_data(epub_path)

        temp_sqlite_path = Path(temp_dir) / "KoboReader.sqlite"

        log.info(
            f"Copying the SQLite file to the temporary directory: {temp_sqlite_path}"
        )
        shutil.copy2(sqlite_path, temp_sqlite_path)
        log.info("Extract highlights from the SQLite database ...")
        highlights = services.extract_highlights(str(temp_sqlite_path), book.title)

        log.info("Match the highlights to sections in the book ...")
        book = services.match_highlights_to_sections(book, highlights)

        log.info("Converting highlights to Org-mode format...")
        highlights_org = services.convert_highlights_to_org(book)

        log.info(f"Saving highlights to {learn_orgmode_path}...")
        services.update_orgmode_file(learn_orgmode_path, highlights_org)

        log.info("Export complete.")


@cli.command()
def add_anki_notes(
    anki_orgmode_path: Optional[Path] = typer.Option(
        None, "--anki-orgmode-path", envvar="ANKI_ORGMODE_PATH"
    ),
    deck: str = typer.Option("Default", "--deck", "-d"),
) -> None:
    """Adds notes to Anki from the specified org mode file.

    Args:
        anki_orgmode_path (Optional[str]): The path to the org mode file.
            If not provided, uses the ANKI_ORGMODE_PATH environment variable.
        deck (str): The name of the deck to add notes to. Defaults to "Default".

    Returns:
        None

    Raises:
        FileNotFoundError: If the org mode file cannot be found.
        Exception: For any errors encountered while processing notes.
    """
    # Determine the path to the org mode file
    if anki_orgmode_path is None:
        log.error(
            "No path provided and ANKI_ORGMODE_PATH environment variable is not set."
        )
        raise ValueError(
            "No path provided and ANKI_ORGMODE_PATH environment variable is not set."
        )
    log.debug(f"Using org mode file at: {anki_orgmode_path}")
    log.debug(f"Using Anki deck: {deck}")

    # Parse notes from org mode file
    notes = services.parse_anki_notes(anki_orgmode_path, deck=deck)
    log.debug(f"Parsed {len(notes)} notes from org mode file.")
    if len(notes) == 0:
        log.info("There are no new notes to add to Anki")
        return

    anki = Anki()
    try:

        # Start the server
        anki.start_server()

        # Create Anki notes
        services.create_anki_notes(notes, anki)
        log.info(f"Successfully added {len(notes)} notes to the '{deck}' deck.")

        # Optionally remove the org file if necessary
        services.remove_anki_notes_from_org_file(notes, anki_orgmode_path)
        log.info(f"Removed org mode file: {anki_orgmode_path}")

    except FileNotFoundError as e:
        log.error(f"File not found: {e}")
        raise
    except Exception as e:
        log.error(f"An error occurred: {e}")
        raise
    finally:
        anki.stop_server()


if __name__ == "__main__":
    cli()
