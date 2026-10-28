#!/usr/bin/env python3
"""Gera captions.json (linhas + palavras corrigidas) a partir de words.json."""
import json, sys

src = "/tmp/openclaw/fabrizio/words.json"
dst = "/tmp/openclaw/fabrizio/remotion/public/captions.json"

CORRECTIONS = {
    "milídeis": "mil líderes",
    "semanamente": "semanalmente",
    "vão": "vou",
}

with open(src, encoding="utf-8") as f:
    data = json.load(f)

words = []
for w in data["words"]:
    word = CORRECTIONS.get(w["word"], w["word"])
    start = round(w["start"], 3)
    end = round(w["end"], 3)
    if end - start < 0.12:  # palavra com duração zerada/ruim
        end = round(start + 0.18, 3)
    words.append({"word": word, "start": start, "end": end})

# chunk em linhas: quebra em gap > 0.35s ou > 6 palavras
lines = []
cur = []
prev_end = None
for w in words:
    if prev_end is not None and (w["start"] - prev_end > 0.35 or len(cur) >= 6):
        lines.append(cur)
        cur = []
    cur.append(w)
    prev_end = w["end"]
if cur:
    lines.append(cur)

out = {
    "lines": [
        {
            "start": ln[0]["start"],
            "end": ln[-1]["end"],
            "words": ln,
        }
        for ln in lines
    ]
}

import os
os.makedirs(os.path.dirname(dst), exist_ok=True)
with open(dst, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

print("✅", len(out["lines"]), "linhas →", dst)
for ln in out["lines"]:
    print(f'  [{ln["start"]:5.2f}-{ln["end"]:5.2f}]', " ".join(x["word"] for x in ln["words"]))
