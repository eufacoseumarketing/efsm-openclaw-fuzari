#!/usr/bin/env python3
"""Transcreve áudio/vídeo com faster-whisper (local, CPU).

Uso:
  python3 scripts/transcribe.py <input> [--model base] [--language pt] [--word-timestamps] [--output out.json]
"""
import sys, json, argparse
from faster_whisper import WhisperModel


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--model", default="base")
    ap.add_argument("--language", default=None)
    ap.add_argument("--word-timestamps", action="store_true")
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        args.input,
        language=args.language,
        word_timestamps=args.word_timestamps,
        vad_filter=True,
    )

    result = {
        "language": info.language,
        "language_probability": round(info.language_probability, 4),
        "duration": round(info.duration, 2),
        "segments": [
            {
                "start": round(s.start, 2),
                "end": round(s.end, 2),
                "text": s.text.strip(),
            }
            for s in segments
        ],
    }

    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        print("✅ salvo em", args.output)
    else:
        print(text)


if __name__ == "__main__":
    main()
