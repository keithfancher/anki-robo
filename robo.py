#!/usr/bin/env python3


import json
import sys

import robo.extractors as extractors


def extract_one(key: str) -> str:
    extract = extractors.get_extractor("linguee-fr")
    local_testing = True
    result = extract(key, local_testing)
    return json.dumps(result)


def main():
    if len(sys.argv) == 2:
        key = sys.argv[1]
        print(extract_one(key))
    else:
        print("Usage: robo.py [SEARCH_KEY]")


if __name__ == "__main__":
    main()
