from dataclasses import dataclass
from typing import cast

import ankirobo.extractors.api as api
from ankirobo.types import Result

NAME = "jotoba-jp-en"

# Default settings. Required for POSTing to the Jotoba API. See:
# https://github.com/WeDontPanic/Jotoba/blob/dev/lib/types/src/api/app/search/query.rs#L37
# ...which is the Rust representation of this object.
JOTOBA_SETTINGS = {
    "user_lang": "en-US",
    "show_english": True,
    "page_size": 5,  # We only need a result or two, probably...
    "show_example_sentences": True,
    "sentence_furigana": False, # Seems to have no effect
}

# Sample `curl` call to hit this API:
# ```
# curl -X POST "https://jotoba.de/api/app/words" \
#  -H "accept: application/json" \
#  -H "content-type: application/json" \
#  -d '{"query_str":"ぴかぴか", "settings": {"user_lang": "en-US", "show_english": true, "page_size": 5, "show_example_sentences": true, "sentence_furigana": false}}'
# ```
#
# Note that this is NOT the "official" public API which is documented here:
# https://jotoba.de/docs.html
# That one ^ is missing certain data we need, like JLPT level and a "curated"
# example sentence.
#
# The API we're using here is (I believe) an internal API, so it could likely
# change without notice. That said, it has all the data we need!


def extract(key: str, local_testing: bool) -> list[Result]:
    url = "https://jotoba.de/api/app/words"
    data = {"query_str": key, "settings": JOTOBA_SETTINGS}

    response = api.api_post(key, url, data, local_testing, "jotoba")
    if not isinstance(response, dict):
        return []

    # I thought type-narrowing would apply here? But it doesn't seem to? Hence cast:
    response = cast(dict, response)
    if "content" in response and "words" in response["content"]:
        words = response["content"]["words"]
    else:
        words = []

    if words:
        # We only care about the top result:
        parsed_word = parse_word(words[0])
        return [to_result(parsed_word)]
    else:
        return []


@dataclass
class Word:
    term: str
    translation: str
    example_sentence: str
    example_sentence_translation: str
    tags: list[str]


@dataclass
class Sense:
    glosses: str
    example_sentence: list[str]  # or maybe a tuple?


@dataclass
class MergedSenses:
    translation: str
    example_sentence: str
    example_sentence_translation: str


def to_result(word: Word) -> Result:
    return {
        "term": word.term,
        "translation": word.translation,
        "example_sentence": word.example_sentence,
        "example_sentence_translation": word.example_sentence_translation,
        "tags": " ".join(word.tags),
    }


def parse_word(word: dict) -> Word:
    term = word.get("reading", "")

    tags: list[str] = []
    if "jlpt_lvl" in word:
        tags.append("jlpt_n" + str(word["jlpt_lvl"]))
    if "is_common" in word and word["is_common"]:
        tags.append("common")

    senses = word.get("senses", [])
    parsed_senses = list(map(parse_sense, senses))
    merged_senses = merge_senses(parsed_senses)

    return Word(
        term=term,
        translation=merged_senses.translation,
        example_sentence=merged_senses.example_sentence,
        example_sentence_translation=merged_senses.example_sentence_translation,
        tags=tags,
    )


def merge_senses(senses: list[Sense]) -> MergedSenses:
    """Given a list of all the "senses" of a word, combine/extract the data we
    need into a flat structure."""
    meanings: list[str] = []
    sentences: list[tuple[str, str]] = []

    # Collect all the "glosses" into a single string field, with each numbered
    # and newline-separated. Also stash away example sentences for us to select
    # from later.
    for index, sense in enumerate(senses, start=1):
        meanings.append(f"{index}. {sense.glosses}")
        if len(sense.example_sentence) == 2:
            sentences.append((sense.example_sentence[0], sense.example_sentence[1]))

    translation = "\n".join(meanings)

    example_sentence = ""
    example_sentence_translation = ""
    if sentences:
        # For now, only fetching the first example sentence pair:
        first_sentence_tuple = sentences[0]
        example_sentence = first_sentence_tuple[0]
        example_sentence_translation = first_sentence_tuple[1]

    return MergedSenses(
        translation=translation,
        example_sentence=example_sentence,
        example_sentence_translation=example_sentence_translation,
    )


def parse_sense(sense: dict) -> Sense:
    glosses = ""
    if "glosses" in sense:
        glosses = ", ".join(sense["glosses"])
    example_sentence = []
    if "example_sentence" in sense:
        example_sentence = sense["example_sentence"]

    return Sense(glosses=glosses, example_sentence=example_sentence)
