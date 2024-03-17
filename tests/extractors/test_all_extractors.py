from ankirobo import extract_one
from tests.testdata.all import all_expected_results


# Note that the call to `assert` *seems* to need to happen in an actual `test`
# function (like this one), or `pytest` doesn't give us all the useful
# diffing/context in failure cases.
def test_all_extractors():
    testing = True  # Clearly!
    for extractor_name, expected_result_set in all_expected_results.items():
        for search_key, expected_result in expected_result_set.items():
            result = extract_one(extractor_name, search_key, testing)
            assert (
                result == expected_result
            ), f"Extracted data mismatch for extractor `{extractor_name}`, search key `{search_key}`"
