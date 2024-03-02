#!/usr/bin/env python3


import robo.extractors as extractors


def main():
    extract = extractors.get_extractor("linguee-fr")

    key = "flâner"
    result = extract(key)

    print(str(result))


if __name__ == "__main__":
    main()
