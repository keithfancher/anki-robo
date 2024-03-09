import robo.extractors.linguee.shared as linguee
from robo.types import Result

encre_results = [
    linguee.make_linguee_result(
        input="encre",
        translation="ink",
        part_of_speech="noun,\xa0feminine",
        other_forms="",
        ex_sentence="Je préfère écrire à l'encre bleue sur papier blanc.",
        ex_sentence_translation="I prefer to write with blue ink on white paper.",
    )
]

flaner_results = [
    linguee.make_linguee_result(
        input="flâner",
        translation="stroll, wander",
        part_of_speech="verb",
        other_forms="",
        ex_sentence="Elle flânait le long de la plage.",
        ex_sentence_translation="She wandered along the beach.",
    )
]

hilarant_results = [
    linguee.make_linguee_result(
        input="hilarant",
        translation="hilarious",
        part_of_speech="adjective, masculine",
        other_forms="(hilarante f sl, hilarants m pl, hilarantes f pl)",
        ex_sentence="Il me fait rire avec des histoires hilarantes.",
        ex_sentence_translation="He makes me laugh with hilarious stories.",
    )
]

oreiller_results = [
    linguee.make_linguee_result(
        input="oreiller",
        translation="pillow",
        part_of_speech="noun,\xa0masculine",
        other_forms="(plural: oreillers m)",
        ex_sentence="Les oreillers sur mon lit sont très moelleux.",
        ex_sentence_translation="The pillows on my bed are very soft.",
    )
]

pister_results = [
    linguee.make_linguee_result(
        input="pister",
        translation="track sb./sth., trail sb./sth.",
        part_of_speech="verb",
        other_forms="",
        ex_sentence="Le policier a pisté le cambrioleur jusqu'à sa cachette.",
        ex_sentence_translation="The policeman tracked the burglar all the way to his hideout.",
    )
]

tonnerre_results = [
    linguee.make_linguee_result(
        input="tonnerre",
        translation="thunder",
        part_of_speech="noun,\xa0masculine",
        other_forms="",
        ex_sentence="Nous avons entendu un coup de tonnerre au loin.",
        ex_sentence_translation="We heard a crash of thunder far away.",
    )
]

# A mapping of term -> expected output
expected_results: dict[str, list[Result]] = {
    "encre": encre_results,
    "flâner": flaner_results,
    "hilarant": hilarant_results,
    "oreiller": oreiller_results,
    "pister": pister_results,
    "tonnerre": tonnerre_results,
}
