import robo.extractor.web as web


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
def extract(key: str) -> dict[str, str]:
    url = "https://www.linguee.com/french-english/translation/fl%C3%A2ner.html"
    soup = web.get_page_data(url)

    english_words_results = soup.find_all("a", class_="dictLink featured")
    english_words: list[str] = [r.string for r in english_words_results]

    example_lines_selector = (
        "div.translation.sortablemg.featured > div.example_lines > div.example.line"
    )

    example_lines = soup.select(example_lines_selector)
    example_sentence_pairs: list[tuple[str, str]] = list(
        map(example_pairs_from_line, example_lines)
    )

    # TODO: Return multiple sets of example sentences, probably
    french_sentence: str = ""
    english_sentence: str = ""
    if example_sentence_pairs:
        french_sentence = example_sentence_pairs[0][0]
        english_sentence = example_sentence_pairs[0][1]

    return {
        "input": key,
        "english": ", ".join(english_words),
        "french_sentence": french_sentence,
        "english_sentence": english_sentence,
    }


def example_pairs_from_line(soup) -> tuple[str, str]:
    fr_sentence = soup.find("span", class_="tag_s").string
    en_sentence = soup.find("span", class_="tag_t").string
    return (fr_sentence, en_sentence)
