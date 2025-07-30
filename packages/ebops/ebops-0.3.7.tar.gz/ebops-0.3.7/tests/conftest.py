"""Store the classes and fixtures used throughout the tests."""

import os
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture(name="work_dir")
def work_dir_(tmp_path: Path) -> Generator[Path, None, None]:
    """Create the work directory for the tests."""
    old_cwd = os.getcwd()
    os.chdir(tmp_path)

    yield tmp_path

    # Reset the current working directory after the test is done
    os.chdir(old_cwd)
