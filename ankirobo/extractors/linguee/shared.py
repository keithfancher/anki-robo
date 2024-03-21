import ankirobo.extractors.helpers.web as web
from ankirobo.types import Extractor, Result

# Extractor names
DE_EN = "linguee-de-en"
ES_EN = "linguee-es-en"
FR_EN = "linguee-fr-en"


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

        # First fetch all returned terms. This might include related
        # terms/definitions in addition to what we're searching for, so we
        # further filter it down before returning.
        all_terms = soup.select("div#dictionary div.lemma.featured")
        all_parsed_terms = [data_from_term(key, term) for term in all_terms]
        return get_term_match(key, all_parsed_terms)

    return extract


def get_term_match(key: str, results: list[Result]) -> list[Result]:
    """First look for data that matches the search term exactly. (Which we must
    do because Linguee will NOT always give back exact matches first?!) If
    there's no exact match, fall back to first result."""
    if not results:
        return []

    exact_matches = [x for x in results if x["term"] == key]
    if exact_matches:
        return [exact_matches[0]]
    else:
        return [results[0]]


def make_linguee_result(
    term: str,
    translation: str,
    part_of_speech: str,
    other_forms: str,
    ex_sentence: str,
    ex_sentence_translation: str,
) -> Result:
    """A simple wrapper to ensure I only have to change these key names in one
    place, in the event they need to change. Again."""
    return {
        "term": term,
        "translation": translation,
        "part_of_speech": part_of_speech,
        "other_forms": other_forms,
        "example_sentence": ex_sentence,
        "example_sentence_translation": ex_sentence_translation,
    }


def data_from_term(key: str, term) -> Result:
    result_term = get_result_term(term)

    # All the "common" corresponding translations. These are usually the ones
    # with example sentences as well.
    translations = get_translations(term)

    part_of_speech = web.safe_string(term.select_one("span.tag_wordtype"))

    # Other forms of the word that might exist. For example: "hilarant" has
    # "hilarante, hilarants", etc.
    # Note use of `strings` here, plural. There's a whole tree of elements and
    # we just want the contained text.
    other_forms = web.safe_strings(
        term.select_one("h2.line.lemma_desc > span.tag_forms")
    )

    # List of tuples in the form: (target-language sentence, sentence translation)
    example_sentence_pairs: list[tuple[str, str]] = example_sentences(term)

    example_sentence: str = ""
    example_sentence_translation: str = ""
    if example_sentence_pairs:
        # Just getting the FIRST example sentence pair for now. Later, we can
        # decide how to provide multiple options.
        example_sentence = example_sentence_pairs[0][0]
        example_sentence_translation = example_sentence_pairs[0][1]

    return make_linguee_result(
        term=result_term,
        translation=", ".join(translations),
        part_of_speech=part_of_speech,
        other_forms="".join(other_forms).strip(),
        ex_sentence=example_sentence,
        ex_sentence_translation=example_sentence_translation,
    )


def get_result_term(term) -> str:
    """Get the actual term result, which can sometimes differ slightly from the
    search key. (For example with French, searching "écrouler" yields results
    for "s'écrouler". And with German, searching "schiff" yields "Schiff".)"""
    raw_term_links = term.select("span.tag_lemma > a.dictLink")

    # Each word in a result phrase is potentially its own link with its own placeholders.
    link_list: list[str] = []
    for link in raw_term_links:
        remove_placeholders(link)
        link_list += web.safe_strings(link)

    result_term = " ".join(link_list)
    return normalize_whitespace(result_term)


def remove_placeholders(tag) -> None:
    """Remove "placeholders" from a given tag, altering the `tag` param in
    place. For example, the parts in parens below:
       pister (qqch./qqn.)
       mettre (qqch.) en valeur"""
    # Just removing for now. They're unneeded, and they mess up uniqueness in
    # the "term" field. But if we decide to pull them out and use them, use
    # `extract` or `replace_with` below instead of `decompose`.
    placeholders = tag.find("span", class_="placeholder")
    if placeholders:
        placeholders.decompose()


def normalize_whitespace(s: str) -> str:
    """Remove any amount of whitespace between words in a string, then replace
    with a single space."""
    spl = s.split()
    return " ".join(spl)


def get_translations(term) -> list[str]:
    """Get a list of possible translations for the term. For example, if the
    search key is "tormenta", this function might return ["storm", "thunderstorm"]."""
    raw_translation_results = term.select("a.dictLink.featured")
    results = []
    for translation_phrase in raw_translation_results:
        # Note use of `safe_strings` (plural) here. It's possible there's a
        # tree of elements and containing text here for a single translation
        # phrase. BS gives us a list of strings and we join for our final phrase.
        phrase_words = web.safe_strings(translation_phrase)
        phrase = "".join(phrase_words)
        if phrase:
            results.append(phrase)
    return results


def example_sentences(term) -> list[tuple[str, str]]:
    """Get a list of all the "curated" example sentences Linguee provides. This
    does NOT include the "unchecked" example sentences they source from random
    places on the internet."""
    example_lines_selector = (
        "div.translation.sortablemg.featured > div.example_lines > div.example.line"
    )

    example_lines = term.select(example_lines_selector)
    example_sentence_pairs: list[tuple[str, str]] = list(
        map(example_pair_from_line, example_lines)
    )

    return example_sentence_pairs


def example_pair_from_line(example_line) -> tuple[str, str]:
    """Returns a tuple consisting of one example sentence in the target
    language (e.g. French, if you're looking up a French word) and its
    translation."""
    ex_sentence = web.safe_string(example_line.find("span", class_="tag_s"))
    ex_sentence_translation = web.safe_string(example_line.find("span", class_="tag_t"))
    return (ex_sentence.strip(), ex_sentence_translation.strip())
