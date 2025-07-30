"""Test the model."""

from ebops.model import Highlight


def test_highlight_comparison_less_than() -> None:
    """Test the comparison operator '<' for Highlight objects.

    Compares two Highlight objects to ensure the '<' operator works
    correctly, based on their positions.
    """
    highlight1 = Highlight(
        section_id="section1", position="/1/2/3:4", text="Highlight 1"
    )
    highlight2 = Highlight(
        section_id="section2", position="/1/2/4:1", text="Highlight 2"
    )

    result = highlight1 < highlight2

    assert result is True


def test_highlight_comparison_greater_than() -> None:
    """Test the comparison operator '>' for Highlight objects.

    Compares two Highlight objects to ensure the '>' operator works
    correctly, based on their positions.
    """
    highlight1 = Highlight(
        section_id="section1", position="/1/2/4:1", text="Highlight 1"
    )
    highlight2 = Highlight(
        section_id="section2", position="/1/2/3:4", text="Highlight 2"
    )

    result = highlight1 > highlight2

    assert result is True
