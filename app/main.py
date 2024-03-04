import json

import robo


def from_text_file(filename: str, extractor_name: str, local_testing: bool) -> str:
    with open(filename, "r") as f:
        contents = f.read()
    result = robo.from_plaintext(contents, extractor_name, local_testing)
    return json.dumps(result)
