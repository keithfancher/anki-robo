import robo.extractors.linguee.french as linguee_fr
from robo.types import Extractor, InvalidExtractorName

# Map from: extractorName -> extract function
extractors: dict[str, Extractor] = {
    linguee_fr.NAME: linguee_fr.extract,
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
