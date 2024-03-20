from pathlib import Path
from typing import Optional


def get_path(additional: Optional[Path] = None) -> Path:
    """Get path where extractor test data lives. Can optionally pass in an
    additional path, relative to the test data base path, for a particular
    extractor's data."""
    # Absolute path of the directory which contains this module (which should be
    # the `testdata` package):
    base_path = Path(__file__).parent.resolve()
    if additional:
        return base_path / additional
    else:
        return base_path
