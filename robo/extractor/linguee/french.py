from robo.extractor import Extractor, Result
import robo.extractor.web as web


class LingueeFrench(Extractor):
    def extract(key: str) -> Result:
        url = "https://www.linguee.com/french-english/translation/fl%C3%A2ner.html"
        web.get_data(url)
        return []
