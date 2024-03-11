from robo.api import RoboOpts, extract_list
from robo.types import ResultSummary


def from_plaintext(text: str, extractor_name: str, opts: RoboOpts) -> ResultSummary:
    """Extract data from the given source given a plaintext, newline-delimited
    list of words."""
    keys = text.splitlines()
    return extract_list(extractor_name, keys, opts)
