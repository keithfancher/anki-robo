import robo.extractor.web as web


def extract(key: str) -> dict[str, str]:
    url = "https://www.linguee.com/french-english/translation/fl%C3%A2ner.html"
    web.get_page_data(url)
    return {}
