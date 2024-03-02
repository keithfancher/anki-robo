#!/usr/bin/env python3


import json
import robo.extractors as extractors


def main():
    extract = extractors.get_extractor("linguee-fr")

    key = "flâner"
    result = extract(key)

    print(json.dumps(result))


if __name__ == "__main__":
    main()
