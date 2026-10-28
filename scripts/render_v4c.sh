#!/bin/bash
set -e
cd /home/node/.openclaw/workspace/efsm-openclaw-fuzari
FF=bin/ffmpeg
BG=jobs/job-001/assets/bg_premium.jpg
M=jobs/job-001/masks
R=jobs/job-001/renders

# filtro de composição: sujeito com grade de cor (cool + contraste) preservando alpha
compose() { # $1=seg $2=dur
  $FF -y -loop 1 -t $2 -framerate 30 -i $BG -framerate 30 -i $M/${1}_frames/%04d.png \
    -filter_complex "\
[0:v]scale=1080:1920,setsar=1[bg];\
[1:v]scale=1080:1920,setsar=1,split[subrgb][subalpha];\
[subrgb]format=rgb24,eq=contrast=1.10:saturation=0.94:brightness=-0.02,colorbalance=bs=0.07:bm=0.05:rm=-0.02[subgraded];\
[subalpha]alphaextract[amask];\
[subgraded][amask]alphamerge[sub];\
[bg][sub]overlay=0:0:format=auto[v]" \
    -map "[v]" -r 30 -c:v libx264 -preset fast -crf 14 -pix_fmt yuv420p $R/${1}_comp.mp4 2>&1 | tail -1
}

echo "=== compondo seg1 (5.4s) ===" && compose seg1 5.4
echo "=== compondo seg2 (6.8s) ===" && compose seg2 6.8
echo "=== compondo seg3 (7.7s) ===" && compose seg3 7.7

echo "=== render final V4 ==="
$FF -y \
  -i $R/seg1_comp.mp4 -i $R/seg2_comp.mp4 -i $R/seg3_comp.mp4 \
  -i jobs/job-001/audio/bg_music.mp3 \
  -i jobs/job-001/input/IMG_6302.MOV \
  -i jobs/job-001/input/IMG_6303.MOV \
  -i jobs/job-001/input/IMG_6305.MOV \
  -filter_complex_script jobs/job-001/filter_v4b.txt \
  -map "[vout]" -map "[aout]" \
  -c:v libx264 -preset medium -crf 20 -profile:v high -pix_fmt yuv420p \
  -c:a aac -b:a 160k -ar 48000 \
  -movflags +faststart \
  $R/v004_premium.mp4 2>&1 | tail -6

echo "RENDER V4 (fix) CONCLUÍDO"
