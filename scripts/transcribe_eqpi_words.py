#!/usr/bin/env python3
import json
from faster_whisper import WhisperModel

SRC = '/home/node/.openclaw/workspace/efsm-openclaw-fuzari/jobs/job-002/input/eqpi_original.mp4'
OUT = '/home/node/.openclaw/workspace/efsm-openclaw-fuzari/jobs/job-002/transcript/eqpi_words_full.json'

model = WhisperModel('base', device='cpu', compute_type='int8')
segments, info = model.transcribe(SRC, language='pt', word_timestamps=True, vad_filter=True)

result = {
    'language': info.language,
    'duration': info.duration,
    'segments': [
        {
            'start': round(s.start, 2),
            'end': round(s.end, 2),
            'text': s.text.strip(),
            'words': [
                {'word': w.word, 'start': round(w.start, 2), 'end': round(w.end, 2)}
                for w in (s.words or [])
            ],
        }
        for s in segments
    ],
}
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print('✅ salvo em', OUT)
