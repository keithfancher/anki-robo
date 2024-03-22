import tests.extractors.jotoba as jotoba
import tests.extractors.linguee.de_en as linguee_de_en
import tests.extractors.linguee.es_en as linguee_es_en
import tests.extractors.linguee.fr_en as linguee_fr_en
from ankirobo import Result

# Map from search key -> expected extraction results.
# (Note: `TypeAlias` not added till python 3.10!)
ExpectedResultSet = dict[str, list[Result]]

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
