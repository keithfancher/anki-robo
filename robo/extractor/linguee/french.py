import robo.extractor.web as web
from robo.extractor import Result

# URLs?
# Probably explicitly french/english:
# https://www.linguee.com/french-english/translation/fl%C3%A2ner.html
#
# Above works even for bad results:
# https://www.linguee.com/french-english/translation/asdfasdf.html
# And misspellings: ("Did you mean 'flâner'?")
# https://www.linguee.com/french-english/translation/flaner.html
#
# Could mistakenly find English words, we want only French:
# https://www.linguee.com/english-french/search?source=auto&query=tonnerre


# TODO: pull out functionality shared by ALL linguee pages/languages. Share!
def extract(key: str) -> list[Result]:
    # url = f"https://www.linguee.com/french-english/translation/{key}.html"
    # soup = web.get_page_data(url) # TODO!
    soup = web.get_local_page_data(key, "linguee/french", "ISO-8859-15")

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
