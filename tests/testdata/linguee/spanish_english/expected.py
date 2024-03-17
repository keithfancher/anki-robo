import ankirobo.extractors.linguee.shared as linguee
from ankirobo.types import Result

calavera_results = [
    linguee.make_linguee_result(
        input="calavera",
        translation="skull",
        part_of_speech="noun, feminine",
        other_forms="",
        ex_sentence="El barco pirata tenía una bandera negra con una calavera.",
        ex_sentence_translation="The pirate ship had a black flag with a skull on it.",
    )
]

parseguir_results = [
    linguee.make_linguee_result(
        input="perseguir",
        translation="pursue, chase sb./sth., seek sth.",
        part_of_speech="verb",
        other_forms="",
        ex_sentence="Las dos compañías persiguen un objetivo común.",
        ex_sentence_translation="The two companies pursue a common goal.",
    )
]

suscribirse_results = [
    linguee.make_linguee_result(
        input="suscribirse",
        translation="subscribe to sth., subscribe, sign up",
        part_of_speech="verb",
        other_forms="",
        ex_sentence="Los usuarios pueden suscribirse al boletín en el sitio web.",
        ex_sentence_translation="Users can subscribe to the newsletter on the website.",
    )
]

tormenta_results = [
    linguee.make_linguee_result(
        input="tormenta",
        translation="storm, thunderstorm",
        part_of_speech="noun, feminine",
        other_forms="(plural: tormentas f)",
        ex_sentence="La tormenta llenó la alcantarilla de agua.",
        ex_sentence_translation="The storm filled the drain with water.",
    )
]

videojuego_results = [
    linguee.make_linguee_result(
        input="videojuego",
        translation="video game, videogame",
        part_of_speech="noun, masculine",
        other_forms="",
        ex_sentence="El desarrollo de videojuegos requiere mucha creatividad.",
        ex_sentence_translation="The development of video games requires a lot of creativity.",
    )
]

extractor_name = linguee.ES_EN

# A mapping of term -> expected output
expected_results: dict[str, list[Result]] = {
    "calavera": calavera_results,
    "perseguir": parseguir_results,
    "suscribirse": suscribirse_results,
    "tormenta": tormenta_results,
    "videojuego": videojuego_results,
}
