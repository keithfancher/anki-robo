import robo.extractors.linguee.french_english as linguee_fr_en
from robo.types import Extractor, InvalidExtractorName

# Map from: extractorName -> extract function
extractors: dict[str, Extractor] = {
    linguee_fr_en.NAME: linguee_fr_en.extract,
}


def get_extractor(name: str) -> Extractor:
    if name in extractors:
        return extractors[name]
    else:
        # Or could just return None? But that just passes the buck on this
        # logic, really. Again: my kingdom for a monad!
        raise InvalidExtractorName


def get_extractor_names() -> set[str]:
    return set(extractors.keys())
