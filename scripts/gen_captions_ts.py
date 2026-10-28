#!/usr/bin/env python3
"""Gera src/captions.ts a partir de captions.json."""
import json

with open("/tmp/openclaw/fabrizio/remotion/public/captions.json", encoding="utf-8") as f:
    data = json.load(f)

lines = []
for ln in data["lines"]:
    words = [(w["word"], w["start"], w["end"]) for w in ln["words"]]
    lines.append(words)

ts = []
ts.append("// Gerado automaticamente a partir de words.json (Whisper word timestamps)")
ts.append("export type CaptionWord = { word: string; start: number; end: number };")
ts.append("export type CaptionLine = { start: number; end: number; words: CaptionWord[] };")
ts.append("")
ts.append("export const captionLines: CaptionLine[] = [")
for words in lines:
    start = words[0][1]
    end = words[-1][2]
    ts.append("  {")
    ts.append(f"    start: {start},")
    ts.append(f"    end: {end},")
    ts.append("    words: [")
    for w, s, e in words:
        ts.append(f'      {{ word: "{w}", start: {s}, end: {e} }},')
    ts.append("    ],")
    ts.append("  },")
ts.append("];")
ts.append("")

with open("/tmp/openclaw/fabrizio/remotion/src/captions.ts", "w", encoding="utf-8") as f:
    f.write("\n".join(ts))

print("✅ captions.ts gerado com", len(lines), "linhas")
