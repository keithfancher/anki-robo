import robo.extractor.linguee.french as linguee_fr
from robo.types import Extractor

# Map from: extractorName -> extract function
extractors: dict[str, Extractor] = {
    linguee_fr.NAME: linguee_fr.extract,
}


# TODO: Handle missing keys... somehow.
def get_extractor(name: str) -> Extractor:
    return extractors[name]


def get_extractor_names() -> set[str]:
    return set(extractors.keys())
