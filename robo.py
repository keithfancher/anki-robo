#!/usr/bin/env python3


import sys

import app.main as app


def main():
    if len(sys.argv) == 2:
        extractor = "linguee-fr"
        r = app.from_text_file(sys.argv[1], extractor, local_testing=True)
        print(r)
    else:
        print("Usage: robo.py [FILE_NAME]")


if __name__ == "__main__":
    main()
