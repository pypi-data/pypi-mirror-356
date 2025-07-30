"""Define the data models of the program."""

import logging
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel

log = logging.getLogger(__name__)


class Highlight(BaseModel):
    """Model an e-reader highlight."""

    section_id: str
    position: str
    text: str

    def parse_position(self) -> Tuple[int, ...]:
        """Parse the position string into a tuple of integers for comparison.

        Returns:
            Tuple[int, ...]: A tuple of integers representing the position.
        """
        # Remove any leading slashes and split by '/'
        parts = self.position.replace(":", "/").strip("/").split("/")
        return tuple(int(part) for part in parts)

    def __lt__(self, other: "Highlight") -> bool:
        """Less-than comparison based on the position.

        Args:
            other (Highlight): The other Highlight object to compare against.

        Returns:
            bool: True if this Highlight's position is less than the other's position.
        """
        return self.parse_position() < other.parse_position()


class Section(BaseModel):
    """Model an e-pub section."""

    # VNE003 variable names that shadow builtins are not allowed
    id: str  # noqa: VNE003
    title: str
    content: Optional[str] = None
    sections: List["Section"] = []
    highlights: List[Highlight] = []

    def __repr__(self) -> str:
        """Simplify the representation of a Section."""
        return self.title


class Book(BaseModel):
    """Model an e-pub book."""

    title: str
    author: str
    toc: List[Section]


class AnkiModel(BaseModel):
    """Define the model of an Anki model."""

    name: str
    fields: List[str]


class AnkiNote(BaseModel):
    """Define the model of an Anki note."""

    anki_model: str
    fields: Dict[str, Any]
    deck: str = "Default"
    tags: Optional[List[str]] = None
