from robo.extractor import Extractor, Result
import robo.extractor.web as web


class LingueeFrench(Extractor):
    def extract(self, key: str) -> Result:
        url = "https://www.linguee.com/french-english/translation/fl%C3%A2ner.html"
        web.get_page_data(url)
        return Result("", [])
