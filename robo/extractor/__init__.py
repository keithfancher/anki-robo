from dataclasses import dataclass


@dataclass
class Result:
    key: str
    data: list[dict]  # TODO: obviously not real
