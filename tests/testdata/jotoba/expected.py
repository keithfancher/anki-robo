import ankirobo.extractors.jotoba as jotoba
from ankirobo.types import Result

arukimawaru_results = [
    {
        "term": "歩き回る",
        "term_reading": "あるきまわる",
        "translation": "to walk about, to walk around, to walk to and fro, to pace around, to wander",
        "example_sentence": "私は野原を歩き回るのが好きだ。",
        "example_sentence_reading": "わたしはのはらをあるきまわるのがすきだ。",
        "example_sentence_translation": "I like to roam about the fields.",
        "tags": "common",
    }
]

hachidori_results = [
    {
        "term": "蜂鳥",
        "term_reading": "はちどり",
        "translation": "hummingbird (Trochilidae family)",
        "example_sentence": "ハチドリはチョウと同じくらい小さい鳥です。",
        "example_sentence_reading": "ハチドリはチョウとおなじくらいちいさいとりです。",
        "example_sentence_translation": "A hummingbird is no larger than a butterfly.",
        "tags": "",
    }
]

pikapika_results = [
    {
        "term": "ピカピカ",
        "term_reading": "ピカピカ",
        "translation": "1. with a glitter, with a sparkle\n2. brand new, shiny and new\n3. cleaned (of a plate, etc.), finished",
        "example_sentence": "その車はワックスがかけられてピカピカしている。",
        "example_sentence_reading": "そのくるまはワックスがかけられてピカピカしている。",
        "example_sentence_translation": "The car is waxed and shining.",
        "tags": "jlpt_n2 common",
    }
]

arashi_results = [
    {
        "term": "嵐",
        "term_reading": "あらし",
        "translation": "1. storm, tempest\n2. uproar, hullabaloo, storm (e.g. of protest), winds (e.g. of change)\n3. pile of 3 cards of the same value in oicho-kabu",
        "example_sentence": "この風は嵐の印だ。",
        "example_sentence_reading": "このかぜはあらしのしるしだ。",
        "example_sentence_translation": "This wind is a sign of a storm.",
        "tags": "jlpt_n3 common",
    }
]

extractor_name = jotoba.NAME

# A mapping of term -> expected output
expected_results: dict[str, list[Result]] = {
    "あるきまわる": arukimawaru_results,
    "はちどり": hachidori_results,
    "ぴかぴか": pikapika_results,
    "嵐": arashi_results,
}
