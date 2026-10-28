#!/bin/bash
set -e
cd /home/node/.openclaw/workspace/efsm-openclaw-fuzari
bin/ffmpeg -y \
  -loop 1 -framerate 30 -i jobs/job-001/assets/bg_premium.jpg \
  -framerate 30 -i jobs/job-001/masks/seg1_frames/%04d.png \
  -framerate 30 -i jobs/job-001/masks/seg2_frames/%04d.png \
  -framerate 30 -i jobs/job-001/masks/seg3_frames/%04d.png \
  -i jobs/job-001/audio/bg_music.mp3 \
  -i jobs/job-001/input/IMG_6302.MOV \
  -i jobs/job-001/input/IMG_6303.MOV \
  -i jobs/job-001/input/IMG_6305.MOV \
  -filter_complex_script jobs/job-001/filter_v4.txt \
  -map "[vout]" -map "[aout]" \
  -c:v libx264 -preset medium -crf 20 -profile:v high -pix_fmt yuv420p \
  -c:a aac -b:a 160k -ar 48000 \
  -movflags +faststart \
  jobs/job-001/renders/v004_premium.mp4 2>&1 | tail -15
echo "RENDER V4 CONCLUÍDO"
