import robo
import robo.extractors.linguee.shared as linguee


# Attempt to exercise as much as possible of the `robo` library's modules.
def test_robo_lib_api():
    extractor_name = linguee.FR_EN
    local_testing = True

    in_list = "encre\nflâner\nasdfblah"

    result_summary = robo.from_plaintext(in_list, extractor_name, local_testing)

    assert result_summary.results_success == set(
        ["encre", "flâner"]
    ), "Incorrect set of success results"
    assert result_summary.results_not_found == set(
        ["asdfblah"]
    ), "Incorrect set of 'not found' results"

    results_csv = robo.to_csv(result_summary.results, extractor_name)
    assert (
        # Note call to `splitlines()` -- we want this comparison to work
        # regardless of newline-type (windows, unix, etc.). Python's default
        # CSV creation uses some funky "excel-compatible" format by default.
        results_csv.splitlines() == expected_csv.splitlines()
    ), "Final CSV output does not match expected result"


expected_csv = """#separator:Comma
#tags:AnkiRobo linguee-fr-en
#deck:AnkiRobo
#columns:input,translation,part_of_speech,other_forms,example_sentence,example_sentence_translation
encre,ink,"noun, feminine",,Je préfère écrire à l'encre bleue sur papier blanc.,I prefer to write with blue ink on white paper.
flâner,"stroll, wander",verb,,Elle flânait le long de la plage.,She wandered along the beach."""
