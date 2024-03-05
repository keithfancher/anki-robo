import robo
from robo.types import Result


def from_plaintext(text: str, extractor_name: str, local_testing: bool) -> list[Result]:
    """Extract data from the given source given a plaintext, newline-delimited
    list of words."""
    keys = text.splitlines()
    return robo.extract_list(extractor_name, keys, local_testing)
