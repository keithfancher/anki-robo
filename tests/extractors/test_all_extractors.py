from typing import TypeAlias

import robo.extractors.linguee.shared as linguee
import tests.testdata.linguee.french_english.expected as linguee_fr_en
import tests.testdata.linguee.german_english.expected as linguee_de_en
import tests.testdata.linguee.spanish_english.expected as linguee_es_en
from robo import Result, extract_one

# Map from search key -> expected extraction results.
ExpectedResultSet: TypeAlias = dict[str, list[Result]]

# Map from extractor name -> expected result set.
# Simply add a line to this dictionary with your extractor test data.
expected_results: dict[str, ExpectedResultSet] = {
    linguee.DE_EN: linguee_de_en.expected_results,
    linguee.ES_EN: linguee_es_en.expected_results,
    linguee.FR_EN: linguee_fr_en.expected_results,
}


# Note that the call to `assert` *seems* to need to happen in an actual `test`
# function (like this one), or `pytest` doesn't give us all the useful
# diffing/context in failure cases.
def test_all_extractors():
    testing = True  # Clearly!
    for extractor_name, expected_result_set in expected_results.items():
        for search_key, expected_result in expected_result_set.items():
            result = extract_one(extractor_name, search_key, testing)
            assert (
                result == expected_result
            ), f"Extracted data mismatch for extractor `{extractor_name}`, search key `{search_key}`"
