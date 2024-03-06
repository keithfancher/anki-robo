import robo.extractors as extractors
from robo.types import Result, ResultSummary


def extract_one(extractor_name: str, key: str, local_testing: bool) -> list[Result]:
    """Fetch the given `Extractor` by name and use it to extract data for the
    given search key. If `local_testing` is `True`, attempt to use local test
    data instead of hitting a remote source."""
    extract = extractors.get_extractor(extractor_name)
    return extract(key.strip(), local_testing)


def extract_list(
    extractor_name: str, keys: list[str], local_testing: bool
) -> ResultSummary:
    """Fetch the given `Extractor` by name and use it to extract data for the
    given list of search keys. If `local_testing` is `True`, attempt to use
    local test data instead of hitting a remote source."""
    results_summary = empty_summary()
    extract = extractors.get_extractor(extractor_name)
    for key in keys:  # TODO: parallism, etc.
        # Note that each `extract` result is itself a list. We want to simply
        # append all the list results into a single, flat list.
        k = key.strip()
        r = extract(k, local_testing)
        results_summary.append(k, r)
    return results_summary


def empty_summary() -> ResultSummary:
    return ResultSummary(results=[], results_success=set(), results_not_found=set())
