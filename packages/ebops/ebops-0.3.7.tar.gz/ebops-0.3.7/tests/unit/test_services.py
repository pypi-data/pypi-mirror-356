"""Test the services."""

import sqlite3
from pathlib import Path
from typing import List

import pytest

from ebops.model import AnkiNote, Book, Highlight, Section
from ebops.services import (
    convert_highlights_to_org,
    convert_toc_to_org,
    extract_epub_data,
    extract_highlights,
    match_highlights_to_sections,
    parse_anki_notes,
    remove_anki_notes_from_org_file,
    update_orgmode_file,
)


@pytest.fixture(name="sqlite_temp_db")
def sqlite_temp_db_(tmpdir: Path) -> Path:
    """
    Create a temporary SQLite database file with sample data for testing.
    """
    db_path = tmpdir / "test.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE Bookmark (
            StartContainerPath TEXT,
            Text TEXT,
            ContentID TEXT
        )
        """
    )

    # Insert sample data
    cursor.executemany(
        """
        INSERT INTO Bookmark (StartContainerPath, Text, ContentID)
        VALUES (?, ?, ?)
        """,
        [
            (
                "OEBPS/xhtml/Burk_epub3_c02_r1.xhtml#point(/1/4/2/34/3:128)",
                "Highlight 1",
                "Sample Book Title",
            ),
            (
                "OEBPS/xhtml/Burk_epub3_c03_r1.xhtml#point(/2/5/3/45/4:200)",
                "Highlight 2",
                "Sample Book Title",
            ),
            (
                "OEBPS/xhtml/Burk_epub3_c02_r1.xhtml#point(/1/6/2/50/1:300)",
                "Highlight 3",
                "Another Book Title",
            ),
        ],
    )

    conn.commit()
    conn.close()

    return db_path


class TestExtractEpubData:
    def test_on_simple_epub(self) -> None:
        epub_file_path = Path("tests/assets/frankenstein.epub")

        result = extract_epub_data(epub_file_path)

        assert result.title == "Frankenstein; Or, The Modern Prometheus"
        assert result.author == "Mary Wollstonecraft Shelley"
        assert [section.title for section in result.toc] == [
            "Frankenstein;",
            "or, the Modern Prometheus",
            "CONTENTS",
            "Letter 1",
            "Letter 2",
            "Letter 3",
            "Letter 4",
            "Chapter 1",
            "Chapter 2",
            "Chapter 3",
            "Chapter 4",
            "Chapter 5",
            "Chapter 6",
            "Chapter 7",
            "Chapter 8",
            "Chapter 9",
            "Chapter 10",
            "Chapter 11",
            "Chapter 12",
            "Chapter 13",
            "Chapter 14",
            "Chapter 15",
            "Chapter 16",
            "Chapter 17",
            "Chapter 18",
            "Chapter 19",
            "Chapter 20",
            "Chapter 21",
            "Chapter 22",
            "Chapter 23",
            "Chapter 24",
            "THE FULL PROJECT GUTENBERG LICENSE",
        ]
        content = result.toc[4].content
        assert content is not None
        assert content.strip()[:30] == "Letter 2\n\nTo Mrs. Saville, Eng"

    @pytest.mark.slow
    def test_with_nested_sections_epub(self) -> None:
        epub_file_path = Path("tests/assets/shakespeare.epub")

        result = extract_epub_data(epub_file_path)

        section = result.toc[6]
        assert section.content is None
        assert len(section.sections) == 3
        assert (
            section.sections[0].title
            == "SCENE I. Rossillon. A room in the Countess’s palace."
        )


class TestConvertTocToOrg:
    def test_basic(self) -> None:
        toc = [
            Section(
                id="intro.xhtml",
                title="Introduction",
                content="Introduction content",
                sections=[],
            ),
            Section(
                id="chapter1.xhtml",
                title="Chapter 1",
                content="Chapter 1 content",
                sections=[
                    Section(
                        id="section1_1.xhtml",
                        title="Section 1.1",
                        content="Section 1.1 content",
                        sections=[],
                    ),
                    Section(
                        id="section1_2.xhtml",
                        title="Section 1.2",
                        content="Section 1.2 content",
                        sections=[],
                    ),
                ],
            ),
            Section(
                id="chapter2.xhtml",
                title="Chapter 2",
                content="Chapter 2 content",
                sections=[],
            ),
        ]
        book = Book(title="Sample Book", author="Author Name", toc=toc)

        result = convert_toc_to_org(book, initial_level=1)

        expected_result = (
            "* Sample Book by Author Name\n"
            "** Introduction\n"
            "** Chapter 1\n"
            "*** Section 1.1\n"
            "*** Section 1.2\n"
            "** Chapter 2"
        )
        assert result == expected_result

    def test_with_different_initial_level(self) -> None:
        toc = [
            Section(
                id="intro.xhtml",
                title="Introduction",
                content="Introduction content",
                sections=[],
            ),
            Section(
                id="chapter1.xhtml",
                title="Chapter 1",
                content="Chapter 1 content",
                sections=[
                    Section(
                        id="section1_1.xhtml",
                        title="Section 1.1",
                        content="Section 1.1 content",
                        sections=[],
                    ),
                    Section(
                        id="section1_2.xhtml",
                        title="Section 1.2",
                        content="Section 1.2 content",
                        sections=[],
                    ),
                ],
            ),
        ]
        book = Book(title="Sample Book", author="Author Name", toc=toc)

        result = convert_toc_to_org(book, initial_level=2)

        expected_result = (
            "** Sample Book by Author Name\n"
            "*** Introduction\n"
            "*** Chapter 1\n"
            "**** Section 1.1\n"
            "**** Section 1.2"
        )
        assert result == expected_result

    def test_empty_toc(self) -> None:
        book = Book(title="Empty Book", author="No Author", toc=[])

        result = convert_toc_to_org(book)

        expected_result = "* Empty Book by No Author"
        assert result == expected_result


class TestConvertHighlightsToOrg:
    def test_basic(self) -> None:
        toc = [
            Section(
                id="intro.xhtml",
                title="Introduction",
                content="Introduction content",
                highlights=[
                    Highlight(
                        section_id="intro.xhtml",
                        position="/1/1",
                        text="Welcome to the book.",
                    )
                ],
                sections=[],
            ),
            Section(
                id="chapter1.xhtml",
                title="Chapter 1",
                content="Chapter 1 content",
                highlights=[
                    Highlight(
                        section_id="chapter1.xhtml",
                        position="/1/2",
                        text="Important point in Chapter 1.",
                    )
                ],
                sections=[
                    Section(
                        id="section1.1.xhtml",
                        title="Section 1.1",
                        content="Section 1.1 content",
                        highlights=[
                            Highlight(
                                section_id="section1.1.xhtml",
                                position="/1/2/1",
                                text="Detail in Section 1.1",
                            )
                        ],
                        sections=[],
                    )
                ],
            ),
            Section(
                id="chapter2.xhtml",
                title="Chapter 2",
                content="Chapter 2 content",
                sections=[],
            ),
        ]
        book = Book(title="Sample Book", author="Author Name", toc=toc)

        result = convert_highlights_to_org(book, initial_level=1)

        expected_result = (
            "* Sample Book by Author Name\n"
            "** Introduction\n"
            "   - Welcome to the book.\n"
            "** Chapter 1\n"
            "   - Important point in Chapter 1.\n"
            "*** Section 1.1\n"
            "    - Detail in Section 1.1"
        )
        assert result == expected_result

    def test_with_multiple_highlights(self) -> None:
        toc = [
            Section(
                id="chapter1.xhtml",
                title="Chapter 1",
                content="Chapter 1 content",
                highlights=[
                    Highlight(
                        section_id="chapter1.xhtml",
                        position="/1/1",
                        text="Highlight 1 in Chapter 1.",
                    ),
                    Highlight(
                        section_id="chapter1.xhtml",
                        position="/1/2",
                        text="Highlight 2 in Chapter 1.",
                    ),
                ],
                sections=[],
            ),
        ]
        book = Book(title="Sample Book", author="Author Name", toc=toc)

        result = convert_highlights_to_org(book, initial_level=1)

        expected_result = (
            "* Sample Book by Author Name\n"
            "** Chapter 1\n"
            "   - Highlight 1 in Chapter 1.\n"
            "   - Highlight 2 in Chapter 1."
        )
        assert result == expected_result

    def test_no_highlights(self) -> None:
        toc = [
            Section(
                id="intro.xhtml",
                title="Introduction",
                content="Introduction content",
                sections=[],
            ),
            Section(
                id="chapter1.xhtml",
                title="Chapter 1",
                content="Chapter 1 content",
                sections=[
                    Section(
                        id="section1.1.xhtml",
                        title="Section 1.1",
                        content="Section 1.1 content",
                        sections=[],
                    )
                ],
            ),
        ]
        book = Book(title="Sample Book", author="Author Name", toc=toc)

        result = convert_highlights_to_org(book, initial_level=1)

        expected_result = "* Sample Book by Author Name"
        assert result == expected_result

    def test_with_different_initial_level(self) -> None:
        toc = [
            Section(
                id="chapter1.xhtml",
                title="Chapter 1",
                content="Chapter 1 content",
                highlights=[
                    Highlight(
                        section_id="chapter1.xhtml",
                        position="/1/1",
                        text="Highlight in Chapter 1.",
                    )
                ],
                sections=[],
            ),
        ]
        book = Book(title="Sample Book", author="Author Name", toc=toc)

        result = convert_highlights_to_org(book, initial_level=2)

        expected_result = (
            "** Sample Book by Author Name\n"
            "*** Chapter 1\n"
            "    - Highlight in Chapter 1."
        )
        assert result == expected_result

    def test_nested_sections(self) -> None:
        toc = [
            Section(
                id="chapter1.xhtml",
                title="Chapter 1",
                content="Chapter 1 content",
                highlights=[
                    Highlight(
                        section_id="chapter1.xhtml",
                        position="/1/1",
                        text="Highlight in Chapter 1.",
                    )
                ],
                sections=[
                    Section(
                        id="section1.1.xhtml",
                        title="Section 1.1",
                        content="Section 1.1 content",
                        highlights=[
                            Highlight(
                                section_id="section1.1.xhtml",
                                position="/1/1/1",
                                text="Highlight in Section 1.1",
                            )
                        ],
                        sections=[],
                    )
                ],
            ),
        ]
        book = Book(title="Sample Book", author="Author Name", toc=toc)

        result = convert_highlights_to_org(book, initial_level=1)

        expected_result = (
            "* Sample Book by Author Name\n"
            "** Chapter 1\n"
            "   - Highlight in Chapter 1.\n"
            "*** Section 1.1\n"
            "    - Highlight in Section 1.1"
        )
        assert result == expected_result


class TestMatchHighlightsToSections:
    def test_basic(self) -> None:
        toc = [
            Section(
                id="chapter1.xhtml",
                title="Chapter 1",
                content="Chapter 1 content",
                sections=[],
            ),
            Section(
                id="section1.1.xhtml",
                title="Section 1.1",
                content="Section 1.1 content",
                sections=[],
            ),
        ]
        book = Book(title="Sample Book", author="Author Name", toc=toc)
        highlights = [
            Highlight(
                section_id="chapter1.xhtml",
                position="/1/1",
                text="Highlight in Chapter 1.",
            ),
            Highlight(
                section_id="section1.1.xhtml",
                position="/1/1/1",
                text="Highlight in Section 1.1",
            ),
        ]

        result = match_highlights_to_sections(book, highlights)

        assert len(result.toc[0].highlights) == 1
        assert result.toc[0].highlights[0].text == "Highlight in Chapter 1."
        assert len(result.toc[1].highlights) == 1
        assert result.toc[1].highlights[0].text == "Highlight in Section 1.1"

    def test_no_matches(self) -> None:
        toc = [
            Section(
                id="chapter1.xhtml",
                title="Chapter 1",
                content="Chapter 1 content",
                sections=[],
            ),
        ]
        book = Book(title="Sample Book", author="Author Name", toc=toc)
        highlights = [
            Highlight(
                section_id="section1.1.xhtml",
                position="/1/1/1",
                text="Highlight in Section 1.1",
            )
        ]

        result = match_highlights_to_sections(book, highlights)

        assert len(result.toc[0].highlights) == 0

    def test_empty_highlights(self) -> None:
        toc = [
            Section(
                id="chapter1.xhtml",
                title="Chapter 1",
                content="Chapter 1 content",
                sections=[],
            ),
        ]
        book = Book(title="Sample Book", author="Author Name", toc=toc)
        highlights: List[Highlight] = []

        result = match_highlights_to_sections(book, highlights)

        assert len(result.toc[0].highlights) == 0

    def test_nested_sections(self) -> None:
        toc = [
            Section(
                id="chapter1.xhtml",
                title="Chapter 1",
                content="Chapter 1 content",
                sections=[
                    Section(
                        id="section1.1.xhtml",
                        title="Section 1.1",
                        content="Section 1.1 content",
                        sections=[],
                    )
                ],
            )
        ]
        book = Book(title="Sample Book", author="Author Name", toc=toc)
        highlights = [
            Highlight(
                section_id="chapter1.xhtml",
                position="/1/1",
                text="Highlight in Chapter 1.",
            ),
            Highlight(
                section_id="section1.1.xhtml",
                position="/1/1/1",
                text="Highlight in Section 1.1",
            ),
        ]

        result = match_highlights_to_sections(book, highlights)

        assert len(result.toc[0].highlights) == 1
        assert result.toc[0].highlights[0].text == "Highlight in Chapter 1."
        section_highlights = result.toc[0].sections[0].highlights
        assert len(section_highlights) == 1
        assert section_highlights[0].text == "Highlight in Section 1.1"


class TestExtractHighlights:
    def test_basic(self, sqlite_temp_db: Path) -> None:
        """
        Test extraction of highlights from a SQLite database.
        """
        result = extract_highlights(str(sqlite_temp_db), "Sample Book Title")

        expected_highlights = [
            Highlight(
                section_id="Burk_epub3_c02_r1.xhtml",
                position="/1/4/2/34/3:128",
                text="Highlight 1",
            ),
            Highlight(
                section_id="Burk_epub3_c03_r1.xhtml",
                position="/2/5/3/45/4:200",
                text="Highlight 2",
            ),
        ]
        assert len(result) == len(expected_highlights)
        for expected, actual in zip(expected_highlights, result):
            assert actual.section_id == expected.section_id
            assert actual.position == expected.position
            assert actual.text == expected.text

    def test_no_matches(self, sqlite_temp_db: Path) -> None:
        result = extract_highlights(str(sqlite_temp_db), "Nonexistent Title")

        assert not result

    def test_empty_text(self, sqlite_temp_db: Path) -> None:
        """
        Test extraction of highlights that ignores the highlights that have
        empty text fields.
        """
        conn = sqlite3.connect(str(sqlite_temp_db))
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE Bookmark
            SET Text = NULL
            WHERE ContentID = 'Sample Book Title'
            """
        )
        conn.commit()
        conn.close()

        result = extract_highlights(str(sqlite_temp_db), "Sample Book Title")

        expected_highlights: List[Highlight] = []
        assert len(result) == len(expected_highlights)
        for expected, actual in zip(expected_highlights, result):
            assert actual.section_id == expected.section_id
            assert actual.position == expected.position
            assert actual.text == expected.text


class TestUpdateOrgmodeFile:

    @pytest.fixture
    def temp_orgmode_file(self, tmpdir: Path) -> Path:
        """Fixture for creating a temporary Org-mode file."""
        return tmpdir / "test.org"

    def test_update_orgmode_file_existing_file(self, temp_orgmode_file: Path) -> None:
        """Test updating an existing Org-mode file."""
        initial_content = "Existing content"
        temp_orgmode_file.write_text(initial_content, encoding="utf8")
        toc_org = "* New TOC Content"

        update_orgmode_file(temp_orgmode_file, toc_org)  # act

        expected_content = f"{toc_org}\n\n{initial_content}"
        assert temp_orgmode_file.read_text(encoding="utf8") == expected_content

    def test_update_orgmode_file_nonexistent_file(self, tmpdir: Path) -> None:
        """Test creating a new Org-mode file if it doesn't exist."""
        toc_org = "* New TOC Content"
        books_orgmode_path = tmpdir / "newfile.org"

        update_orgmode_file(books_orgmode_path, toc_org)  # act

        expected_content = f"{toc_org}\n\n"
        assert books_orgmode_path.read_text(encoding="utf8") == expected_content

    def test_update_orgmode_file_no_existing_file(
        self, temp_orgmode_file: Path
    ) -> None:
        toc_org = "* Sample TOC\n"
        # Ensure the file does not exist
        if temp_orgmode_file.exists():
            temp_orgmode_file.unlink()

        update_orgmode_file(temp_orgmode_file, toc_org)  # act

        # Verify the file was created and content was written
        assert temp_orgmode_file.exists()
        with open(temp_orgmode_file, "r", encoding="utf8") as file:
            content = file.read()
            assert content == toc_org + "\n\n"


class TestParseAnkiNotes:

    def test_parse_anki_notes_with_questions_in_title(self, tmpdir: Path) -> None:
        org_file = tmpdir / "test.org"
        content = """* Question?
This is the answer.

* Another question

Here is the back content.
"""
        org_file.write_text(content, encoding="utf8")

        result = parse_anki_notes(org_file)

        assert len(result) == 2
        note1 = result[0]
        assert note1.fields == {"Front": "Question?", "Back": "This is the answer."}
        assert note1.anki_model == "Basic"
        assert note1.tags == ["automatic"]
        assert note1.deck == "Default"
        note2 = result[1]
        assert note2.fields == {
            "Front": "Another question",
            "Back": "Here is the back content.",
        }
        assert note2.anki_model == "Basic"
        assert note2.tags == ["automatic"]
        assert note2.deck == "Default"

    def test_parse_anki_notes_with_no_questions(self, tmpdir: Path) -> None:
        org_file = tmpdir / "test_no_questions.org"
        content = """* Simple Note
This is the content for the note.

* Another Note
More content here.
"""
        org_file.write_text(content, encoding="utf8")

        result = parse_anki_notes(org_file)

        assert len(result) == 2
        note1 = result[0]
        assert note1.fields == {
            "Front": "Simple Note",
            "Back": "This is the content for the note.",
        }
        assert note1.anki_model == "Basic"
        assert note1.tags == ["automatic"]
        assert note1.deck == "Default"
        note2 = result[1]
        assert note2.fields == {"Front": "Another Note", "Back": "More content here."}
        assert note2.anki_model == "Basic"
        assert note2.tags == ["automatic"]
        assert note2.deck == "Default"

    def test_parse_anki_notes_with_lists_in_body(self, tmpdir: Path) -> None:
        org_file = tmpdir / "test_list_body.org"
        content = """* Simple Note
- This is the content for the note.
- This is more content for the first note.

* Another Note

- More content here.
"""
        org_file.write_text(content, encoding="utf8")

        result = parse_anki_notes(org_file)

        assert len(result) == 2
        note1 = result[0]
        assert note1.fields == {
            "Front": "Simple Note",
            "Back": (
                "\n- This is the content for the note.\n"
                "- This is more content for the first note."
            ),
        }
        assert note1.anki_model == "Basic"
        assert note1.tags == ["automatic"]
        assert note1.deck == "Default"
        note2 = result[1]
        assert note2.fields == {
            "Front": "Another Note",
            "Back": "\n- More content here.",
        }
        assert note2.anki_model == "Basic"
        assert note2.tags == ["automatic"]
        assert note2.deck == "Default"

    def test_parse_anki_notes_with_questions_in_body(self, tmpdir: Path) -> None:
        org_file = tmpdir / "test.org"
        content = """* Question?
This is the answer?
"""
        org_file.write_text(content, encoding="utf8")

        result = parse_anki_notes(org_file)

        note1 = result[0]
        assert note1.fields == {"Front": "Question?", "Back": "This is the answer?"}
        assert note1.anki_model == "Basic (and reversed card)"
        assert note1.tags == ["automatic"]
        assert note1.deck == "Default"


class TestRemoveAnkiNotes:

    def test_remove_existing_note(self, tmp_path: Path) -> None:
        """Test removal of an existing note."""
        org_file = tmp_path / "test.org"
        initial_content = "* Note 1\nContent here\n\n* Note 2\nMore content here\n"
        org_file.write_text(initial_content, encoding="utf8")
        note_to_remove = AnkiNote(
            anki_model="Basic",
            fields={"Front": "Note 1", "Back": "Content here"},
            tags=["automatic"],
            deck="Test Deck",
        )

        remove_anki_notes_from_org_file([note_to_remove], org_file)  # act

        final_content = org_file.read_text(encoding="utf8")
        assert "Note 1" not in final_content
        assert "Note 2" in final_content

    def test_remove_non_existing_note(self, tmp_path: Path) -> None:
        """Test that non-existing notes are not removed."""
        org_file = tmp_path / "test.org"
        initial_content = "* Note 1\nContent here\n\n* Note 2\nMore content here\n"
        org_file.write_text(initial_content, encoding="utf8")
        note_to_remove = AnkiNote(
            anki_model="Basic",
            fields={"Front": "Non-existent Note", "Back": "Some content"},
            tags=["automatic"],
            deck="Test Deck",
        )

        remove_anki_notes_from_org_file([note_to_remove], org_file)  # act

        final_content = org_file.read_text(encoding="utf8")
        assert "Note 1" in final_content
        assert "Note 2" in final_content

    def test_remove_multiple_notes(self, tmp_path: Path) -> None:
        """Test removal of multiple notes."""
        org_file = tmp_path / "test.org"
        initial_content = (
            "* Note 1\nFront content 1\n\n"
            "* Note 2\nFront content 2\n\n"
            "* Note 3\nSome other content\n"
        )
        org_file.write_text(initial_content, encoding="utf8")
        notes_to_remove = [
            AnkiNote(
                anki_model="Basic",
                fields={"Front": "Note 1", "Back": "Front content 1"},
                tags=["automatic"],
                deck="Test Deck",
            ),
            AnkiNote(
                anki_model="Basic",
                fields={"Front": "Note 2", "Back": "Front content 2"},
                tags=["automatic"],
                deck="Test Deck",
            ),
        ]

        remove_anki_notes_from_org_file(notes_to_remove, org_file)  # act

        final_content = org_file.read_text(encoding="utf8")
        assert "Note 1" not in final_content
        assert "Note 2" not in final_content
        assert "Note 3" in final_content
