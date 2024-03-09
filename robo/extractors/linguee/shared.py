import robo.extractors.web as web
from robo.types import Extractor, Result

# Extractor names
FR_EN = "linguee-fr-en"


# TODO: remove specific references to "french" and "english" in the actual
# extractor code, make generic/language-agnostic.
def make_extractor(language_pair: tuple[str, str]) -> Extractor:
    """Generates a Linguee extractor for any language pair which Linguee
    supports. For example, `("french", "english")` for an extractor used to
    look up French words."""
    url_lang = "-".join(language_pair)  # e.g. "french-english"
    test_data_dir = "_".join(language_pair)  # e.g. "french_english"
    url_base = f"https://www.linguee.com/{url_lang}/translation"

    def extract(key: str, local_testing: bool) -> list[Result]:
        url = f"{url_base}/{key}.html"
        soup = web.get_page_data(
            key, url, local_testing, f"linguee/{test_data_dir}", encoding="ISO-8859-15"
        )
        if not soup:
            return []

        term_matches = soup.select("div#dictionary div.lemma.featured")
        if term_matches:
            # Get only the first matching term. This prevents situations where,
            # e.g., if you search "encre", you also get "encrer" in the results.
            first_match = term_matches[0]
            return [data_from_term(key, first_match)]
        else:
            return []

    return extract


def data_from_term(key: str, term) -> dict[str, str]:
    # All the "common" corresponding english words. These are usually the ones
    # with example sentences as well.
    english_words = get_english_words(term)

    # aka "part of speech":
    word_type = web.safe_string(term.select_one("span.tag_wordtype"))

    # Note use of `strings` here, plural. There's a whole tree of elements and
    # we just want the contained text.
    other_forms = web.safe_strings(
        term.select_one("h2.line.lemma_desc > span.tag_forms")
    )

    # List of tuples in the form: (French sentence, English sentence)
    example_sentence_pairs: list[tuple[str, str]] = example_sentences(term)

    french_sentence: str = ""
    english_sentence: str = ""
    if example_sentence_pairs:
        # Just getting the FIRST example pair for now. Later, we can decide how
        # to provide multiple options.
        french_sentence = example_sentence_pairs[0][0]
        english_sentence = example_sentence_pairs[0][1]

    return {
        "input": key,
        "english": ", ".join(english_words),
        "word_type": word_type,
        "other_forms": "".join(other_forms).strip(),
        "french_sentence": french_sentence,
        "english_sentence": english_sentence,
    }


def get_english_words(term) -> list[str]:
    english_words_results = term.select("a.dictLink.featured")
    results = []
    for english_phrase in english_words_results:
        # Note use of `safe_strings` (plural) here. It's possible there's a
        # tree of elements and containing text here for a single English
        # phrase. BS gives us a list of strings and we join for our final phrase.
        phrase_words = web.safe_strings(english_phrase)
        phrase = "".join(phrase_words)
        if phrase:
            results.append(phrase)
    return results


def example_sentences(term) -> list[tuple[str, str]]:
    example_lines_selector = (
        "div.translation.sortablemg.featured > div.example_lines > div.example.line"
    )

    example_lines = term.select(example_lines_selector)
    example_sentence_pairs: list[tuple[str, str]] = list(
        map(example_pair_from_line, example_lines)
    )

    return example_sentence_pairs


def example_pair_from_line(example_line) -> tuple[str, str]:
    fr_sentence = web.safe_string(example_line.find("span", class_="tag_s"))
    en_sentence = web.safe_string(example_line.find("span", class_="tag_t"))
    return (fr_sentence, en_sentence)
