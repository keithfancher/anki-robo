from pathlib import Path
from typing import Optional


def get_path(additional: Optional[Path] = None) -> Path:
    """Get path where extractor test data lives. Can optionally pass in an
    additional path, relative to the test data base path, for a particular
    extractor's data."""
    # TODO: Test this when installed. Probably want to turn this into an
    # absolute path based on location of this module or something.
    base_path = Path("ankirobo/extractors/testdata")
    if additional:
        return base_path / additional
    else:
        return base_path
