#!/usr/bin/env python3


import json
import sys
import robo.extractors as extractors


def extract_one(key: str) -> str:
    extract = extractors.get_extractor("linguee-fr")
    result = extract(key)
    return json.dumps(result)


def main():
    if len(sys.argv) == 2:
        key = sys.argv[1]
        print(extract_one(key))
    else:
        print("Usage: robo.py [SEARCH_KEY]")


if __name__ == "__main__":
    main()
