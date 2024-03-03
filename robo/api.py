import robo.extractors as extractors
from robo.extractor import Result


def extract_one(extractor_name: str, key: str, local_testing: bool) -> list[Result]:
    extract = extractors.get_extractor(extractor_name)
    return extract(key, local_testing)


# TODO!
def extract_list(extractor_name: str, key: str, local_testing: bool) -> list[Result]:
    return []
