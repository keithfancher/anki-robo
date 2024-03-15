import ankirobo.extractors.web as web
from ankirobo.types import Result

NAME = "jotoba-jp-en"


def extract(key: str, local_testing: bool) -> list[Result]:
    url = f"https://jotoba.com/search/0/{key}?l=en-US"

    soup = web.get_page_data(key, url, local_testing, "jotoba")
    print(soup) # TODO
    if not soup:
        return []

    # TODO: use `find` instead of select? BS docs say selectors will be slower than BS API
    word_entries = soup.select("div#mainBody div.word-entry")
    print(word_entries) # TODO
    if not word_entries:
        return []

    return [data_from_word_entry(word_entries[0])]


def data_from_word_entry(soup) -> Result:
    entry_head = soup.find("div", class_="entry-head")
    result_term_raw = web.safe_strings(entry_head.select_one("h1 > ruby.quick"))
    result_term = "".join(result_term_raw)

    # TODO: get tags from entry head as well ("common" and jlpt level)

    senses = soup.find_all("div", class_="sense")

    first_sense = parse_sense(senses[0])  # TODO parse all and merge

    return {
        "term": result_term,
        "translation": first_sense["translation"],
        "example_sentence": first_sense["example_sentence"],
        "example_sentence_translation": first_sense["example_sentence_translation"],
        "tags": "",
    }


def parse_sense(soup) -> dict[str, str]:
    translation_num = web.safe_string(soup.select_one("div.glosses > div.count"))
    translation = web.safe_string(
        soup.select_one("div.glosses > div.translation > div.tl")
    )

    example_sentence_raw = soup.find("div", class_="example-sentence")
    example_sentence_jp_raw = example_sentence_raw.find("ruby", class_="quick")
    example_sentence_translation_raw = example_sentence_jp_raw.find_next_sibling("div")

    example_sentence_jp = "".join(
        web.safe_strings(example_sentence_raw.find("ruby", class_="quick"))
    )
    example_sentence_translation = web.safe_string(example_sentence_translation_raw)

    return {
        "translation": translation_num + " " + translation,
        "example_sentence": example_sentence_jp,
        "example_sentence_translation": example_sentence_translation,
    }
