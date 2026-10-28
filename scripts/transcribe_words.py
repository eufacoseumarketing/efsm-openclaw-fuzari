#!/usr/bin/env python3
"""Transcrição com timestamps por palavra (pra kinetic typography)."""
import sys, json
from faster_whisper import WhisperModel

src = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else "words.json"
model_size = sys.argv[3] if len(sys.argv) > 3 else "base"

model = WhisperModel(model_size, device="cpu", compute_type="int8")
segments, info = model.transcribe(src, language="pt", word_timestamps=True)

result = {"language": info.language, "duration": info.duration, "words": []}
for seg in segments:
    for w in seg.words:
        result["words"].append({
            "word": w.word.strip(),
            "start": round(w.start, 3),
            "end": round(w.end, 3),
        })

with open(out, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)

print("✅", len(result["words"]), "palavras →", out)
