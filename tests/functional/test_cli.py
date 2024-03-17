# "Functional" tests, which exercise pretty much the entire application via the
# CLI interface. Note that the remote calls are still mocked out here -- not
# quite "end-to-end".

import io
from contextlib import redirect_stdout
from pathlib import Path
from typing import Callable

import ankirobo.cli.main as cli


def test_cli_get():
    # Equivalent to: `./ankirobo get -t -s linguee-fr-en tests/functional/test-terms-fr`
    test_input_path = Path("tests/functional/test-terms-fr")
    cli_args = ["get", "-t", "-s", "linguee-fr-en", str(test_input_path)]

    expected_output = """#separator:Comma
#tags:AnkiRobo linguee-fr-en
#deck:AnkiRobo
#columns:input,translation,part_of_speech,other_forms,example_sentence,example_sentence_translation
hilarant,hilarious,"adjective, masculine","(hilarante f sl, hilarants m pl, hilarantes f pl)",Il me fait rire avec des histoires hilarantes.,He makes me laugh with hilarious stories.
flâner,"stroll, wander",verb,,Elle flânait le long de la plage.,She wandered along the beach.
encre,ink,"noun, feminine",,Je préfère écrire à l'encre bleue sur papier blanc.,I prefer to write with blue ink on white paper.
oreiller,pillow,"noun, masculine",(plural: oreillers m),Les oreillers sur mon lit sont très moelleux.,The pillows on my bed are very soft.
tonnerre,thunder,"noun, masculine",,Nous avons entendu un coup de tonnerre au loin.,We heard a crash of thunder far away.
"""

    # Redirect stdout so we can assert against results:
    stdout = get_stdout(lambda: cli.main(cli_args))

    # The actual output contains "other stuff", but we only want to compare the
    # CSV data. Split on newlines and fetch the tail end of the output.
    csv_lines = 9  # len(valid_input_keys) + len(csv_header)
    stdout_tail = stdout.splitlines()[-csv_lines:]
    assert stdout_tail == expected_output.splitlines()


def test_cli_get_one():
    # Equivalent to: `./ankirobo one -t linguee-fr-en flâner`
    cli_args = ["one", "-t", "linguee-fr-en", "flâner"]

    expected_output = r"""[
  {
    "input": "fl\u00e2ner",
    "translation": "stroll, wander",
    "part_of_speech": "verb",
    "other_forms": "",
    "example_sentence": "Elle fl\u00e2nait le long de la plage.",
    "example_sentence_translation": "She wandered along the beach."
  }
]
"""
    # Redirect stdout so we can assert against results:
    stdout = get_stdout(lambda: cli.main(cli_args))

    assert stdout == expected_output


def get_stdout(f: Callable) -> str:
    """Run the given function, capturing any output sent to stdout. Return that
    output as a str."""
    cap = io.StringIO()
    with redirect_stdout(cap):
        f()
    return cap.getvalue()
