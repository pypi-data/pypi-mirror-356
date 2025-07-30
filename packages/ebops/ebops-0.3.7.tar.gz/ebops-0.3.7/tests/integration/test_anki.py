"""Test Anki adapter."""

import contextlib
import os
import shutil
import subprocess
from typing import Generator

import pytest
from _pytest._py.path import LocalPath
from filelock import BaseFileLock, FileLock

from ebops.adapters.anki import Anki
from ebops.model import AnkiModel, AnkiNote


@pytest.fixture(name="lock", scope="session")
def lock_(
    tmp_path_factory: pytest.TempPathFactory,
) -> Generator[BaseFileLock, None, None]:
    """Create lock file."""
    base_temp = tmp_path_factory.getbasetemp()
    lock_file = base_temp.parent / "serial.lock"

    yield FileLock(lock_file=str(lock_file))

    with contextlib.suppress(OSError):
        os.remove(path=lock_file)


@pytest.fixture(name="serial")
def _serial(lock: BaseFileLock) -> Generator[None, None, None]:
    """Fixture to run tests in serial."""
    with lock.acquire(poll_interval=0.1):
        yield


@pytest.fixture(name="anki_server")
def _anki(tmpdir: "LocalPath") -> Generator[None, None, None]:
    """Start Anki instance with Anki Connect."""
    anki_dir = tmpdir.join("anki")  # type: ignore

    shutil.copytree("tests/assets/anki", anki_dir)
    with subprocess.Popen(["anki", "-b", anki_dir]) as process:
        yield
        process.terminate()


@pytest.fixture(name="anki")
def anki_() -> Anki:
    """Build the Anki adapter for each def test."""
    anki = Anki()
    anki.wait_server()
    return anki


@pytest.mark.gui
@pytest.mark.usefixtures("serial", "anki_server")
class TestDecks:
    """Gather tests dealing with decks."""

    def test_get_decks(self, anki: Anki) -> None:
        """
        Given: A configured Anki adapter
        When: calling the get_decks
        Then: the existing decks are returned
        """
        result = anki.get_decks()

        assert result == ["Default"]

    def test_create_decks(self, anki: Anki) -> None:
        """
        Given: A configured Anki adapter
        When: creating a new deck
        Then: the deck is created
        """
        anki.create_deck("NewDeck")  # act

        decks = anki.get_decks()
        assert "NewDeck" in decks

    def test_create_decks_accepts_base_deck(self, anki: Anki) -> None:
        """
        Given: A configured Anki adapter
        When: creating a new deck with a base deck
        Then: the deck is created
        """
        anki.create_deck("NewSubDeck", base_deck="NewDeck")  # act

        decks = anki.get_decks()
        assert "NewDeck::NewSubDeck" in decks


@pytest.mark.gui
@pytest.mark.usefixtures("serial", "anki_server")
class TestModels:
    """Gather tests dealing with models."""

    def test_get_models(self, anki: Anki) -> None:
        """
        Given: A configured Anki adapter
        When: asking for the models
        Then: the models are returned
        """
        result = anki.get_models()

        assert len(result) == 5
        assert AnkiModel(name="Basic", fields=["Front", "Back"]) in result


@pytest.mark.gui
@pytest.mark.usefixtures("serial", "anki_server")
class TestNotes:
    """Gather tests dealing with notes."""

    def test_get_note(self, anki: Anki) -> None:
        """
        Given: A configured Anki adapter with no cards
        When: asking for the cards in the default deck
        Then: an empty list is returned
        """
        result = anki.get_notes()

        assert result == []

    def test_add_note(self, anki: Anki) -> None:
        """
        Given: A configured Anki interface
        When: adding a card
        Then: the card is added
        """
        desired_note = AnkiNote(
            anki_model="Basic",
            fields={"Front": "front content", "Back": "back content"},
        )

        anki.add_notes([desired_note])  # act

        notes = anki.get_notes()
        assert len(notes) == 1
        note = notes[0]
        assert note.anki_model == "Basic"
        assert note.fields["Front"]["value"] == "front content"
        assert note.fields["Back"]["value"] == "back content"
