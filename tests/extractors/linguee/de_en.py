import ankirobo.extractors.linguee.shared as linguee
from ankirobo.types import Result

schiff_results = [
    linguee.make_linguee_result(
        input="schiff",
        translation="ship, vessel, aisle",
        part_of_speech="noun, neuter",
        other_forms="",
        ex_sentence="Das Schiff verließ den Hafen am frühen Morgen.",
        ex_sentence_translation="The ship left the port early in the morning.",
    )
]

sorgfaltig_results = [
    linguee.make_linguee_result(
        input="sorgfältig",
        translation="careful, thorough, diligent, accurate, painstaking",
        part_of_speech="adjective",
        other_forms="",
        ex_sentence="Dieses umfangreiche Projekt erfordert sorgfältige Planung.",
        ex_sentence_translation="This extensive project requires careful planning.",
    )
]

suchen_results = [
    linguee.make_linguee_result(
        input="suchen",
        translation="seek, look, find, look for, search, search for sth.",
        part_of_speech="verb",
        other_forms="",
        ex_sentence="Er beschloss, unter einem Baum Schutz zu suchen, als es zu regnen anfing.",
        ex_sentence_translation="He decided to seek shelter under a tree when it began to rain.",
    )
]

extractor_name = linguee.DE_EN

# A mapping of term -> expected output
expected_results: dict[str, list[Result]] = {
    "schiff": schiff_results,
    "sorgfältig": sorgfaltig_results,
    "suchen": suchen_results,
}
