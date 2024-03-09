import robo
import robo.extractors.linguee.french_english as linguee_fr_en
from robo.types import Result

TESTING = True  # Clearly!


def test_extract():
    # TODO: In THEORY, this can be a generic helper for any extractor. But in
    # practice, unless the assertion lives in this module it seems like we lose
    # all the context. So, e.g., if the test fails, pytest will not show the
    # diff between the two objects unless we leave the assertion in this
    # module. Be great to figure out why that is...
    for key, expected_result in expected_results.items():
        result = robo.extract_one(linguee_fr_en.NAME, key, TESTING)
        assert result == expected_result, f"extracted data mismatch for term: {key}"


encre_results = [
    {
        "input": "encre",
        "english": "ink",
        "word_type": "noun,\xa0feminine",
        "other_forms": "",
        "english_sentence": "I prefer to write with blue ink on white paper.",
        "french_sentence": "Je préfère écrire à l'encre bleue sur papier blanc.",
    },
]


flaner_results = [
    {
        "input": "flâner",
        "english": "stroll, wander",
        "word_type": "verb",
        "other_forms": "",
        "english_sentence": "She wandered along the beach.",
        "french_sentence": "Elle flânait le long de la plage.",
    }
]

hilarant_results = [
    {
        "input": "hilarant",
        "english": "hilarious",
        "word_type": "adjective, masculine",
        "other_forms": "(hilarante f sl, hilarants m pl, hilarantes f pl)",
        "english_sentence": "He makes me laugh with hilarious stories.",
        "french_sentence": "Il me fait rire avec des histoires hilarantes.",
    },
]

oreiller_results = [
    {
        "input": "oreiller",
        "english": "pillow",
        "word_type": "noun,\xa0masculine",
        "other_forms": "(plural: oreillers m)",
        "english_sentence": "The pillows on my bed are very soft.",
        "french_sentence": "Les oreillers sur mon lit sont très moelleux.",
    },
]

pister_results = [
    {
        "input": "pister",
        "english": "track sb./sth., trail sb./sth.",
        "word_type": "verb",
        "other_forms": "",
        "english_sentence": "The policeman tracked the burglar all the way to his hideout.",
        "french_sentence": "Le policier a pisté le cambrioleur jusqu'à sa cachette.",
    },
]


tonnerre_results = [
    {
        "input": "tonnerre",
        "english": "thunder",
        "word_type": "noun,\xa0masculine",
        "other_forms": "",
        "english_sentence": "We heard a crash of thunder far away.",
        "french_sentence": "Nous avons entendu un coup de tonnerre au loin.",
    },
]


# A mapping of term -> expected output
expected_results: dict[str, list[Result]] = {
    "encre": encre_results,
    "flâner": flaner_results,
    "hilarant": hilarant_results,
    "oreiller": oreiller_results,
    "pister": pister_results,
    "tonnerre": tonnerre_results,
}
