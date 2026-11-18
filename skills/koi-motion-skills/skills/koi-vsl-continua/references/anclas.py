# Busca frases del guion dentro de assets/build/words.json para que los tiempos salgan de la voz.
import json
import re
import unicodedata

WORDS = json.load(open("assets/build/words.json", encoding="utf-8"))


def norm(text):
    text = unicodedata.normalize("NFD", text.lower())
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]", "", text).split()


KEYS = [norm(w["w"])[0] if norm(w["w"]) else "" for w in WORDS]
cursor = [0]


def locate(phrase):
    """Devuelve el rango de palabras de la frase, buscando solo hacia adelante."""
    tokens = norm(phrase)
    for i in range(cursor[0], len(KEYS) - len(tokens) + 1):
        if KEYS[i:i + len(tokens)] == tokens:
            cursor[0] = i
            return i, i + len(tokens)
    raise ValueError(f"no está en el guion: {phrase}")
