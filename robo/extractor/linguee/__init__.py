from dataclasses import dataclass


@dataclass
class Result:
    key: str
    data: [dict]  # TODO: obviously not real


class Extractor:
    def extract(key: str) -> Result:
        pass
