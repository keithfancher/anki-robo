# 🤖 anki-robo

An Anki-card-creation framework. Quickly create [Anki](https://apps.ankiweb.net/)
cards using data from remote sources. (Or any sources, really!)

## Table of contents

- [Warning](#-warning-)
- [What is anki-robo?](#what-is-anki-robo)
- [Who is it for?](#who-is-it-for)
- [Quick-start](#quick-start)
- [Requirements](#requirements)
- [Installation](#installation)
- [Available data sources](#available-data-sources)
- [Future plans / roadmap](#future-plans--roadmap)
- [I'd like to contribute / set up a new data source](#id-like-to-contribute--set-up-a-new-data-source)

## 🚨 Warning 🚨

anki-robo is still **EARLY** in its development. It's beta software, at best.
Use at your own risk!

And of course you should **always remember to back up your Anki deck before
making any changes to it**, whether with this tool or any other. Don't take
any chances with your precious Anki data!

(That said, don't worry: anki-robo does **not** currently make any changes to
your Anki deck directly. It simply outputs Anki-importable CSV files. You're
in complete control of how that data is imported into your decks.)

## What is anki-robo?

anki-robo is (or will be) a few things:

1. 🧩 **A Python library/framework** which provides a common, generic
   interface for extracting data from various sources and creating [Anki
   cards](https://apps.ankiweb.net/) from that data;
2. 💻 **a CLI application** which uses the above framework to extract data
   from a library of pre-configured sources and automatically create Anki
   cards;
3. 🔌 **an Anki plugin** which integrates the above behavior directly into the
   Anki desktop application (but which doesn't exist yet).

In short, anki-robo is an **Anki-card-creation framework**.

## Who is it for?

Do you use Anki? Do you ever make Anki cards? It might be for you.

## Quick-start

The `anki-robo` CLI app takes the name of a *data source* and an *input file*.
The file contains newline-delimited search terms. `anki-robo` will query the
data source with each search term and collect the resulting data into an
Anki-importable format.

First, let's check what data sources are available with the `anki-robo list`
command:

```
$ anki-robo list
jotoba-jp-en
linguee-de-en
linguee-es-en
linguee-fr-en
```

Now, let's say I'm studying French. I keep a running list of words I want to
make Anki cards for later. Here's my list so far:

```
$ cat vocabulaire.txt
hilarant
flâner
encre
oreiller
tonnerre
```

Okay, let's make our cards! We use the `anki-robo get` command. Again, it
takes the name of the data source (`linguee-fr-en`) and the file with my
search terms (`vocabulaire.txt`):

```
$ anki-robo get linguee-fr-en vocabulaire.txt
Extracting data from source `linguee-fr-en` using search keys from file: vocabulaire.txt...
Writing CSV output to ankirobo-linguee-fr-en-1709946408.csv... Complete!
```

The CSV data file will be populated with the words, their definitions, sample
sentences, and plenty of other data for your Anki cards.

Now I can open Anki, import `ankirobo-linguee-fr-en-1709946408.csv` and start
learning my new words! (See the Linguee extractor's [sample
data](extractor-details.md#sample-data-1) to get an idea of what fields are
included in this particular case.)

## Requirements

- Python >= `3.9` (which is also the version currently bundled with Anki)

The following dependencies will be installed automatically if you use `pip` to
install anki-robo:

- `requests`
- `beautifulsoup4`

## Installation

To install the latest stable version of anki-robo from PyPI, use `pip`:

```
$ pip install anki-robo
```

If you'd like to install the bleeding-edge, not-yet-released version, you can
do that too:

```
$ pip install https://github.com/keithfancher/anki-robo/archive/refs/heads/master.tar.gz
```

You can also simply clone the repo and run the included `anki-robo` binary
directly. However, in this case you'll need to manually install anki-robo's
dependencies. The quickest way to do that is to use the included
`requirements.txt` file:

```
$ pip install -r requirements.txt
```

## Available data sources

anki-robo has extractors for the following data sources so far, with more on
the way!

| Name | Source | Type | Info |
|------|--------|------|------|
| `jotoba-jp-en` | [Jotoba](https://jotoba.de/) | Japanese -> English | [Details](extractor-details.md#jotoba)
| `linguee-de-en` | [Linguee](https://www.linguee.com/german-english/) | German -> English | [Details](extractor-details.md#linguee)
| `linguee-es-en` | [Linguee](https://www.linguee.com/spanish-english/) | Spanish -> English | [Details](extractor-details.md#linguee)
| `linguee-fr-en` | [Linguee](https://www.linguee.com/french-english/) | French -> English | [Details](extractor-details.md#linguee)

Click a "Details" link above for more information about using a given
extractor, the type of data returned, etc.

## Future plans / roadmap

- [ ] Option to output an Anki `.apkg` file instead of a `.csv`
- [ ] Accept markdown input (lists and checklists)
- [ ] Media support (audio, images, &c.)
- [ ] Merge results from multiple data sources into a single output set
- [ ] Anki plugin, to use directly from desktop Anki interface
- [ ] More data sources!
- [ ] ...and so on :D

## I'd like to contribute / set up a new data source

Awesome! It's easy, if you've got a little Python experience. Comprehensive
documentation does not exist yet, but here's a quick overview.

The fundamental interface for anki-robo is an `Extractor`. An `Extractor` is
just a function which takes a single string (one search key) and returns a
list of `Result` objects. (There's also a flag for testing -- but don't worry
about that for now.)

The `Result` object is a simple Python dictionary -- essentially a map of
string -> string. This corresponds to "Anki field name -> field data". One
`Result` corresponds to one Anki card.

In other words, an extractor is just a function that look like this:

```python
def extract(key: str) -> list[Result]:
    ...
```

That's it! Under the hood, your extractor can do anything it wants. For
example:

- Scrape web data using [Beautiful
  Soup](https://beautiful-soup-4.readthedocs.io/en/latest/)
- Pull data from a REST API
- Process local files (Ebooks? Text files? &c.)
- ...or whatever else! (Assuming you can implement it in Python.)

You write the code to extract data for a single term, and anki-robo will tie
the pieces together for you.
