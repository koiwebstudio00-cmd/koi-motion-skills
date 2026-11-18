# Transcribe la voz y la alinea con el guion: cada palabra del guion recibe su tiempo.
# Las palabras que Whisper entiende mal (suele pasar con las marcas) se interpolan con las vecinas.
# Uso: <python con whisper> align.py <voz.mp3> <guion.txt> [salida.json]
# El guion puede tener etiquetas de ElevenLabs entre corchetes: se ignoran.
import difflib
import json
import os
import re
import sys
import unicodedata

import whisper


def norm(word):
    word = unicodedata.normalize("NFD", word.lower())
    word = "".join(c for c in word if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", word)


voice, guion = sys.argv[1], sys.argv[2]
out = sys.argv[3] if len(sys.argv) > 3 else "assets/build/words.json"
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
raw = re.sub(r"\[[^\]]*\]", " ", open(guion, encoding="utf-8").read())
script = raw.split()
model = whisper.load_model("small")
result = model.transcribe(voice, language="es", word_timestamps=True, initial_prompt=" ".join(script))
heard = [w for s in result["segments"] for w in s["words"]]
print("escuchado:", result["text"][:300])

keys_s = [norm(w) for w in script]
keys_h = [norm(w["word"]) for w in heard]
times = [None] * len(script)
for block in difflib.SequenceMatcher(None, keys_s, keys_h, autojunk=False).get_matching_blocks():
    for k in range(block.size):
        h = heard[block.b + k]
        times[block.a + k] = (round(float(h["start"]), 3), round(float(h["end"]), 3))
matched = sum(t is not None for t in times)

i = 0
while i < len(times):
    if times[i] is not None:
        i += 1
        continue
    j = i
    while j < len(times) and times[j] is None:
        j += 1
    left = times[i - 1][1] if i else 0.0
    right = times[j][0] if j < len(times) else left + 0.4 * (j - i)
    step = (right - left) / (j - i)
    for k in range(i, j):
        times[k] = (round(left + (k - i) * step, 3), round(left + (k - i + 1) * step, 3))
    i = j

with open(out, "w", encoding="utf-8") as f:
    json.dump([{"w": w, "s": t[0], "e": t[1]} for w, t in zip(script, times)], f, ensure_ascii=False, indent=0)
print(f"alineadas {matched}/{len(script)} palabras; termina en {times[-1][1]} s")
