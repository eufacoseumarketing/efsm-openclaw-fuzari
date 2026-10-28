#!/bin/bash
set -e
cd /home/node/.openclaw/workspace/efsm-openclaw-fuzari
FF=bin/ffmpeg
BG=jobs/job-001/assets/bg_premium.jpg
M=jobs/job-001/masks
R=jobs/job-001/renders

echo "=== verificando máscaras ==="
for s in 1 2 3; do
  n=$(ls $M/seg${s}_frames/*.png 2>/dev/null | wc -l)
  echo "seg$s: $n frames"
done

echo "=== compondo seg1 (5.4s) ==="
$FF -y -loop 1 -t 5.4 -framerate 30 -i $BG -framerate 30 -i $M/seg1_frames/%04d.png \
  -filter_complex "[0:v]scale=1080:1920,setsar=1[bg];[1:v]scale=1080:1920,setsar=1[sub];[bg][sub]overlay=0:0:format=auto[v]" \
  -map "[v]" -r 30 -c:v libx264 -preset fast -crf 14 -pix_fmt yuv420p $R/seg1_comp.mp4 2>&1 | tail -2

echo "=== compondo seg2 (6.8s) ==="
$FF -y -loop 1 -t 6.8 -framerate 30 -i $BG -framerate 30 -i $M/seg2_frames/%04d.png \
  -filter_complex "[0:v]scale=1080:1920,setsar=1[bg];[1:v]scale=1080:1920,setsar=1[sub];[bg][sub]overlay=0:0:format=auto[v]" \
  -map "[v]" -r 30 -c:v libx264 -preset fast -crf 14 -pix_fmt yuv420p $R/seg2_comp.mp4 2>&1 | tail -2

echo "=== compondo seg3 (7.7s) ==="
$FF -y -loop 1 -t 7.7 -framerate 30 -i $BG -framerate 30 -i $M/seg3_frames/%04d.png \
  -filter_complex "[0:v]scale=1080:1920,setsar=1[bg];[1:v]scale=1080:1920,setsar=1[sub];[bg][sub]overlay=0:0:format=auto[v]" \
  -map "[v]" -r 30 -c:v libx264 -preset fast -crf 14 -pix_fmt yuv420p $R/seg3_comp.mp4 2>&1 | tail -2

echo "=== composição ok, render final V4 ==="
$FF -y \
  -i $R/seg1_comp.mp4 \
  -i $R/seg2_comp.mp4 \
  -i $R/seg3_comp.mp4 \
  -i jobs/job-001/audio/bg_music.mp3 \
  -i jobs/job-001/input/IMG_6302.MOV \
  -i jobs/job-001/input/IMG_6303.MOV \
  -i jobs/job-001/input/IMG_6305.MOV \
  -filter_complex_script jobs/job-001/filter_v4b.txt \
  -map "[vout]" -map "[aout]" \
  -c:v libx264 -preset medium -crf 20 -profile:v high -pix_fmt yuv420p \
  -c:a aac -b:a 160k -ar 48000 \
  -movflags +faststart \
  $R/v004_premium.mp4 2>&1 | tail -8

echo "RENDER V4 CONCLUÍDO"
