from typing import TypeAlias

import tests.testdata.jotoba.expected as jotoba
import tests.testdata.linguee.french_english.expected as linguee_fr_en
import tests.testdata.linguee.german_english.expected as linguee_de_en
import tests.testdata.linguee.spanish_english.expected as linguee_es_en
from ankirobo import Result

# Map from search key -> expected extraction results.
ExpectedResultSet: TypeAlias = dict[str, list[Result]]

# Map from extractor name -> expected result set.
# Simply add a line to this dictionary with your extractor test data.
#
# TODO: can we further cut down this boilerplate?
all_expected_results: dict[str, ExpectedResultSet] = {
    jotoba.extractor_name: jotoba.expected_results,
    linguee_de_en.extractor_name: linguee_de_en.expected_results,
    linguee_es_en.extractor_name: linguee_es_en.expected_results,
    linguee_fr_en.extractor_name: linguee_fr_en.expected_results,
}
