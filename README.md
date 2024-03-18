# anki-robo

## 🚨 Warning!

anki-robo is **VERY EARLY** in its development. It's alpha software, at best.
Use at your own risk!

And of course you should **always remember to back up your Anki deck before
making any changes to it**, whether with this tool or any other. Don't take
any chances with your precious Anki data!

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

## Do I need to know how to program to use it?

Nope! You only need to write code if you plan to contribute an "extractor" for
a new data source.

## How does it work?

1. Pass the `anki-robo` CLI application a list of search keys (vocabulary
   words, for example).
2. anki-robo will query one of its data sources with each of the provided
   keys, process the data, and output an Anki-friendly `.csv` file.
3. Import this file into Anki and you've got your new cards!

In the future, there will be an option to output a pre-made deck as an `.apkg`
file, or to integrate directly with Anki itself to create cards.

## What data sources are available?

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

## Let's see it in action

Sure thing! Keep in mind that it's early in its development, so features are
still limited.

For this example, let's say I'm studying French. I've got a list where I keep
track of new words I come across, with the goal of making an Anki card for
each new word. Here's my list:

```
$ cat vocabulaire.txt
hilarant
flâner
encre
oreiller
tonnerre
```

But making Anki cards is *tedious*. Let's see if anki-robo can help. First,
let's see what data sources are available. The `anki-robo list` command shows
all of our configured data sources:

```
$ ./anki-robo list
jotoba-jp-en
linguee-de-en
linguee-es-en
linguee-fr-en
```

As you can see, it's still a very short list! But lucky for us, [Linguee
French/English](https://www.linguee.com/french-english/) is on it.

Next, we can use the `anki-robo get` command to fetch data from Linguee and
output a `.csv` for us, with all the data for our new cards:

```
$ ./anki-robo get linguee-fr-en vocabulaire.txt

Extracting data from source `linguee-fr-en` using search keys from file: vocabulaire.txt...

[etc... trimming full output in the name of space]

Writing CSV output to ankirobo-linguee-fr-en-1709946408.csv... Complete!
```

Now I can open Anki, import `ankirobo-linguee-fr-en-1709946408.csv` and start
learning my new words! (See the Linguee extractor's [sample
data](extractor-details.md#sample-data-1) to get an idea of what fields are
included.)

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
