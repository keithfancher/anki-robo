import robo.extractors.web as web
from robo.types import Result

NAME: str = "linguee-fr-en"


# TODO: pull out functionality shared by ALL linguee pages/languages. Share!
def extract(key: str, local_testing: bool) -> list[Result]:
    url = f"https://www.linguee.com/french-english/translation/{key}.html"
    soup = web.get_page_data(
        key, url, local_testing, "linguee/french_english", encoding="ISO-8859-15"
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


def data_from_term(key: str, term) -> dict[str, str]:
    # All the "common" corresponding english words. These are usually the ones
    # with example sentences as well.
    english_words_results = term.select("a.dictLink.featured")
    english_words: list[str] = [r.string for r in english_words_results]

    word_type = web.safe_string(term.select_one("span.tag_wordtype"))

    # Note use of `strings` here, plural. There's a whole tree of elements and
    # we just want the contained text.
    #
    # TODO: Better split apart and format these other forms.
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
    fr_sentence = example_line.find("span", class_="tag_s").string
    en_sentence = example_line.find("span", class_="tag_t").string
    return (fr_sentence, en_sentence)
