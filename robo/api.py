import robo.extractors as extractors
from robo.extractor import Result


def extract_one(extractor_name: str, key: str, local_testing: bool) -> list[Result]:
    """Fetch the given `Extractor` by name and use it to extract data for the
    given search key. If `local_testing` is `True`, attempt to use local test
    data instead of hitting a remote source."""
    extract = extractors.get_extractor(extractor_name)
    return extract(key, local_testing)


# TODO!
def extract_list(extractor_name: str, key: str, local_testing: bool) -> list[Result]:
    """Fetch the given `Extractor` by name and use it to extract data for the
    given list of search keys. If `local_testing` is `True`, attempt to use
    local test data instead of hitting a remote source."""
    return []
