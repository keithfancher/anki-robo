import robo


def from_text_file(filename: str, extractor_name: str, local_testing: bool) -> str:
    with open(filename, "r") as f:
        contents = f.read()
    results_summary = robo.from_plaintext(contents, extractor_name, local_testing)
    return robo.to_csv(results_summary.results)
