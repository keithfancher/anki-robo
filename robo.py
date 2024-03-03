#!/usr/bin/env python3


import json
import sys

import robo


def main():
    if len(sys.argv) == 2:
        search_key = sys.argv[1]
        result = robo.extract_one("linguee-fr", search_key, local_testing=True)
        print(json.dumps(result))
    else:
        print("Usage: robo.py [SEARCH_KEY]")


if __name__ == "__main__":
    main()
