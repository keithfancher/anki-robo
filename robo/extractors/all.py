import robo.extractors.linguee.shared as linguee
from robo.types import Extractor, InvalidExtractorName

# Map from: extractorName -> extract function
extractors: dict[str, Extractor] = {
    linguee.ES_EN: linguee.make_extractor(("spanish", "english")),
    linguee.FR_EN: linguee.make_extractor(("french", "english")),
}


def get_extractor(name: str) -> Extractor:
    if name in extractors:
        return extractors[name]
    else:
        # Or could just return None? But that just passes the buck on this
        # logic, really. Again: my kingdom for a monad!
        raise InvalidExtractorName


def get_extractor_names() -> list[str]:
    return sorted(set(extractors.keys()))
