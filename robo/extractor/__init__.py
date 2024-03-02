from dataclasses import dataclass


@dataclass
class Result:
    key: str
    data: list[dict]  # TODO: obviously not real


class Extractor:
    def extract(self, key: str) -> Result:
        pass
