# anki-robo extractors

Each anki-robo extractor is described in detail in the sections below.

## Jotoba

| Name | Data source | Type | Rate limits |
|------|-------------|------|-------------|
|`jotoba-jp-en` | [Jotoba](https://jotoba.de/) | Japanese -> English | Unknown |

### Additional notes

The extractor adds a tag for a term's JLPT level and the `common` tag if it's
a common word.

The Jotoba API returns terms/phrase/sentences with furigana in a specific
format which isn't very useful for Anki cards. At the moment, the Jotoba
extractor simply splits the `term` and `example_sentence` data into two
fields: one with *no* furigana readings and one with readings *only*. (See
"Sample data" below for a concrete example.)

I may decide to convert Jotoba's provided furigana into the "bracket syntax"
supported by the [Anki Japanese plugin](https://ankiweb.net/shared/info/3918629684).
However, there are many other plugins/standards, and nearly all of them allow
you to automatically bulk-generate readings for your own cards. So I may just
let those tools do their job.

An (incomplete) list of Anki Japanese plugins, each which does things in a
slightly different way:

- [Japanese Support](https://ankiweb.net/shared/info/3918629684): I think of
  this as the "official" plugin, but I don't actually know how official it is.
- [JapaneseFurigana](https://ankiweb.net/shared/info/678316993): can generate
  readings using "bracket" syntax or `ruby` tags.
- [AJT Japanese](https://ankiweb.net/shared/info/1344485230): can generate
  readings as well as pitch accents.
- [SimpleFurigana](https://ankiweb.net/shared/info/1444055400): can generate
  readings using "bracket" syntax or `ruby` tags.

### Sample data

```json
{
  "term": "嵐",
  "term_reading": "あらし",
  "translation": "1. storm, tempest\n2. uproar, hullabaloo, storm (e.g. of protest), winds (e.g. of change)\n3. pile of 3 cards of the same value in oicho-kabu",
  "example_sentence": "この風は嵐の印だ。",
  "example_sentence_reading": "このかぜはあらしのしるしだ。",
  "example_sentence_translation": "This wind is a sign of a storm.",
  "tags": "jlpt_n3 common"
}
```

## Linguee

| Name | Data source | Type | Rate limits |
|------|-------------|------|-------------|
| `linguee-de-en` | [Linguee](https://www.linguee.com/german-english/) | German -> English | **Aggressive!** See note below. |
| `linguee-es-en` | [Linguee](https://www.linguee.com/spanish-english/) | Spanish -> English | **Aggressive!** See note below. |
| `linguee-fr-en` | [Linguee](https://www.linguee.com/french-english/) | French -> English | **Aggressive!** See note below. |

### Additional notes

Linguee supports many different languages. Each of the above Linguee
extractors shares the same code and data format.

Linguee does *not* provide an API, so all of the Linguee extractors must
scrape linguee.com to fetch their data. Note that Linguee has **very
aggressive rate limits** -- if you need to fetch data for more than 25-30
terms at a time, it's likely your IP will be blocked, at least temporarily.
Watch out!

For example sentences, this extractor uses only the "curated" sentences
provided alongside the definition. Linguee also provides sentences from "the
wild", but they have no guarantee of correctness and are often sourced from
complex sources like user manuals, etc.

I have prioritized languages for which Linguee provides good example
sentences. (Which is why, for example, Linguee/Japanese support is missing.
Luckily there are [other extractors](#jotoba) for Japanese!)

### Sample data

```json
{
  "input": "hilarant",
  "translation": "hilarious",
  "part_of_speech": "adjective, masculine",
  "other_forms": "(hilarante f sl, hilarants m pl, hilarantes f pl)",
  "example_sentence": "Il me fait rire avec des histoires hilarantes.",
  "example_sentence_translation": "He makes me laugh with hilarious stories."
}
```
