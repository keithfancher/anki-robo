from typing import Callable, TypeAlias

import robo.extractor.linguee.french as linguee_fr

# Extract function takes a search key and returns a dict[str, str].
# TODO: Type aliases/wrappers to make these various string types explicit, probably.
ExtractFunction: TypeAlias = Callable[[str], dict[str, str]]


# Map from: extractorName -> extract function
extractors: dict[str, ExtractFunction] = {
    "linguee-fr": linguee_fr.extract,
}


# TODO: Handle missing keys... somehow.
def get_extractor(name: str) -> ExtractFunction:
    return extractors[name]


def get_extractor_names() -> set[str]:
    return set(extractors.keys())
