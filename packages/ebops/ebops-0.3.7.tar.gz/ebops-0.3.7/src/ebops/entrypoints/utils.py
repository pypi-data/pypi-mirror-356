"""Define the utils for the entrypoints."""

import logging
import sys

import typer

from ..version import version_info  # noqa: E0402

# E0402: can't import from top level, but it's a false positive

log = logging.getLogger(__name__)


def load_logger(verbose: bool = False) -> None:  # pragma no cover
    """Configure the Logging logger.

    Args:
        verbose: Set the logging level to Debug.
    """
    logging.addLevelName(logging.INFO, "\033[36mINFO\033[0m   ")
    logging.addLevelName(logging.ERROR, "\033[31mERROR\033[0m  ")
    logging.addLevelName(logging.DEBUG, "\033[32mDEBUG\033[0m  ")
    logging.addLevelName(logging.WARNING, "\033[33mWARNING\033[0m")

    if verbose:
        logging.basicConfig(
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
            stream=sys.stderr,
            level=logging.DEBUG,
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        logging.getLogger("sh").setLevel(logging.WARN)
        logging.getLogger("urllib3").setLevel(logging.WARN)

    else:
        logging.basicConfig(
            stream=sys.stderr, level=logging.INFO, format="%(levelname)s %(message)s"
        )


def version_callback(value: bool) -> None:
    """Print the version of the program."""
    if value:
        print(version_info())
        raise typer.Exit()
