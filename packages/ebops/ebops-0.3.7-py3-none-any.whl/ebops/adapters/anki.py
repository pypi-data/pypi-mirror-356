"""Define the Anki adapter."""

import logging
import subprocess  # nosec
from contextlib import suppress
from pathlib import Path
from time import sleep
from typing import Any, List, Optional, Union

import requests
from pydantic import BaseModel

from ebops.exceptions import AnkiError  # noqa: E0611

from ..model import AnkiModel, AnkiNote

Response = Union[List[str], List[int]]

log = logging.getLogger(__name__)


class Anki(BaseModel):
    """Define the Anki adapter.

    This class provides methods to interact with the Anki server for tasks such as
    managing decks, models, and notes.
    """

    url: str = "http://localhost:8765"
    base_directory: Optional[Path] = None
    process: Optional[Any] = None

    # ANN401: The API returns List[str], List[int], bool, str... And I don't want to
    # waste time checking the type of all the elements of the result. I assume that
    # the interface is consistent. It also accepts different types in the params
    # argument.
    def requests(
        self, action: str, params: Any = None  # noqa: ANN401
    ) -> Any:  # noqa: ANN401
        """Send a request to the Anki server.

        Args:
            action (str): The action to be performed by the Anki server.
            params (Any, optional): The parameters for the action. Defaults to None.

        Returns:
            Any: The result of the server's action.

        Raises:
            Exception: If the response structure is unexpected or contains an error.
        """
        if params is None:
            params = {}

        log.debug(f"Sending request to Anki server: action={action}, params={params}")
        response = requests.post(
            self.url,
            json={"action": action, "params": params, "version": 6},
            timeout=30,
        ).json()

        if len(response) != 2:
            log.error(f"Response has an unexpected number of fields: {response}")
            raise AnkiError("response has an unexpected number of fields")
        if "error" not in response:
            log.error(f"Response is missing required error field: {response}")
            raise AnkiError("response is missing required error field")
        if "result" not in response:
            log.error(f"Response is missing required result field: {response}")
            raise AnkiError("response is missing required result field")
        if response["error"] is not None:
            raise AnkiError(
                f"Anki server returned an error: {response['error']} "
                f"when running action {action} with params {params}"
            )

        log.debug(f"Received response from Anki server: {response}")
        return response["result"]

    def wait_server(self) -> None:
        """Wait for the Anki server to start.

        This method continually checks the server's URL until a successful connection
        is made, indicating that the server is up and running.
        """
        log.info(f"Waiting for the server to start at {self.url}...")
        while True:
            with suppress(requests.ConnectionError):
                requests.get(self.url, timeout=60)
                log.info(f"The server is up and running at {self.url}.")
                sleep(0.05)  # To make sure that everything is set

                return

    def start_server(self) -> None:
        """Start the Anki server and wait for it to be ready.

        This method launches the Anki server using the 'anki' command and then waits
        for the server to become available by calling `wait_server()`.
        """
        log.info("Starting the server...")
        command = ["anki"]
        if self.base_directory:
            command.extend(["-b", str(self.base_directory)])
            log.debug(f"Using base directory: {self.base_directory}")

        # Consider using 'with' for resource-allocating operations, but I want to use
        # it in two steps
        self.process = subprocess.Popen(  # noqa: R1732 # nosec:
            subprocess.list2cmdline(command)
        )
        log.info(f"Server process started with PID: {self.process.pid}")

        self.wait_server()

    def stop_server(self) -> None:
        """Stop the Anki server process.

        This method terminates the Anki server process that was started by
        `start_server()`.
        """
        if self.process:
            log.info(f"Stopping the server with PID: {self.process.pid}")
            self.process.terminate()
            self.process.wait()  # Optionally wait for the process to fully terminate
            log.info("Server stopped.")
        else:
            log.warning("No server process to stop.")

    def sync(self) -> None:
        """Sync the local collection with the Anki server."""
        log.info("Syncing the collection with the Anki server")
        self.requests("sync")

    def get_decks(self) -> List[str]:
        """Get the available decks on the Anki server.

        Returns:
            List[str]: A list of deck names.
        """
        log.info("Retrieving deck names from the server...")
        decks = self.requests("deckNames")
        log.debug(f"Decks retrieved: {decks}")
        return decks

    def create_deck(self, name: str, base_deck: Optional[str] = None) -> None:
        """Create a new deck on the Anki server.

        Args:
            name (str): The name of the new deck.
            base_deck (Optional[str], optional): The base deck to nest under. Defaults
            to None.
        """
        if base_deck is not None:
            deck = f"{base_deck}::{name}"
        else:
            deck = name

        log.info(f"Creating deck: {deck}")
        self.requests("createDeck", {"deck": deck})

    def get_models(self) -> List[AnkiModel]:
        """Retrieve the available Anki models.

        Returns:
            List[AnkiModel]: A list of AnkiModel objects.
        """
        log.info("Retrieving Anki models...")
        model_names = self.requests(action="modelNames")
        models = [self.get_model(name) for name in model_names]
        log.debug(f"Models retrieved: {models}")
        return models

    def get_model(self, name: str = "Default") -> AnkiModel:
        """Retrieve an Anki model by its name.

        Args:
            name (str, optional): The name of the model. Defaults to "Default".

        Returns:
            AnkiModel: The retrieved Anki model.
        """
        log.info(f"Retrieving Anki model: {name}")
        data = self.requests(action="modelFieldNames", params={"modelName": name})
        model = AnkiModel(name=name, fields=data)
        log.debug(f"Model retrieved: {model}")
        return model

    def get_notes(self, deck: str = "Default") -> List[AnkiNote]:
        """Retrieve the notes of a specified deck.

        Args:
            deck (str, optional): The name of the deck. Defaults to "Default".

        Returns:
            List[AnkiNote]: A list of AnkiNote objects.
        """
        log.info(f"Retrieving notes from deck: {deck}")
        note_ids = self.requests(action="findNotes", params={"query": f"deck:{deck}"})
        notes = [
            AnkiNote(
                anki_model=note["modelName"],
                fields=note["fields"],
                tags=note["tags"],
            )
            for note in self.requests(action="notesInfo", params={"notes": note_ids})
        ]
        log.debug(f"Notes retrieved: {notes}")
        return notes

    def add_notes(self, notes: List[AnkiNote]) -> None:
        """Add multiple Anki notes to the server.

        Args:
            notes (List[AnkiNote]): List of AnkiNote objects to be added.
        """
        log.info(f"Adding {len(notes)} notes to the server...")

        error = False
        for note in notes:
            formatted_notes = [
                {
                    "deckName": note.deck,
                    "modelName": note.anki_model,
                    "fields": note.fields,
                }
            ]
            try:
                self.requests(
                    action="addNotes",
                    params={"notes": formatted_notes},
                )
            except AnkiError:
                log.error(f"Error adding note {note.fields}")
                error = True
        if error:
            raise AnkiError("Adding notes")
        log.info("Notes successfully added.")
