#!/bin/bash
# render_v5_final.sh — V5: vídeo ORIGINAL (sem máscara/sem trocar fundo) + grade + motion + transições + legenda + música
# Feedback Zanatto: cortar "pode ir" do comecinho (seg1 = 2.40s) e usar o vídeo original (sem fundo de IA).
set -e
cd /home/node/.openclaw/workspace/efsm-openclaw-fuzari
FF=bin/ffmpeg
R=jobs/job-001/renders
A=jobs/job-001/audio
CAP=jobs/job-001/captions.ass

# segmentos: (nome, take, start, end)
# seg1 start 2.40 (remove "pode ir" — RMS: pode 1.58-1.74 / ir 1.96-2.14 / "esse é" 2.44)
SEG1_START=2.40; SEG1_END=7.90
SEG2_START=1.50; SEG2_END=7.55
SEG3_START=2.55; SEG3_END=8.40

D1=5.50; D2=6.05; D3=5.85
N1=165; N2=182; N3=176

# Passo 1: trim + grade + scale (vídeo original, sem bg/máscara)
compose() { # $1=seg $2=take $3=start $4=end
  $FF -y -i jobs/job-001/input/$2.MOV -vf \
    "trim=$3:$4,setpts=PTS-STARTPTS,scale=1080:1920,setsar=1,eq=contrast=1.10:saturation=0.94:brightness=-0.02,fps=30" \
    -r 30 -an -c:v libx264 -preset fast -crf 14 -pix_fmt yuv420p $R/${1}_comp.mp4 2>&1 | tail -2
}

# Passo 2: zoom (punch in/out)
zoom() { # $1=seg $2=zoom-expr
  $FF -y -i $R/${1}_comp.mp4 -vf \
    "zoompan=z='$2':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30" \
    -r 30 -c:v libx264 -preset fast -crf 15 -pix_fmt yuv420p $R/${1}_zoom.mp4 2>&1 | tail -2
}

# Passo 3: áudio trimado
audio() { # $1=seg $2=take $3=start $4=dur
  $FF -y -i jobs/job-001/input/$2.MOV -ss $3 -t $4 -vn -ac 1 -ar 48000 $A/${1}_voz.wav 2>&1 | tail -1
}

echo "=== [1/3] trim + grade ==="
compose seg1 IMG_6302 $SEG1_START $SEG1_END
compose seg2 IMG_6303 $SEG2_START $SEG2_END
compose seg3 IMG_6305 $SEG3_START $SEG3_END

echo "=== [2/3] zoom (motion) ==="
zoom seg1 "1+0.08*on/$((N1-1))"
zoom seg2 "1.08-0.08*on/$((N2-1))"
zoom seg3 "1+0.10*on/$((N3-1))"

echo "=== [3/3] áudio das vozes ==="
audio seg1 IMG_6302 $SEG1_START $D1
audio seg2 IMG_6303 $SEG2_START $D2
audio seg3 IMG_6305 $SEG3_START $D3

echo "=== [4/4] montagem final (xfade + legenda + música) ==="
$FF -y \
  -i $R/seg1_zoom.mp4 -i $R/seg2_zoom.mp4 -i $R/seg3_zoom.mp4 \
  -i $A/seg1_voz.wav -i $A/seg2_voz.wav -i $A/seg3_voz.wav \
  -i $A/bg_music.mp3 \
  -filter_complex "\
[0:v][1:v]xfade=transition=smoothleft:duration=0.35:offset=5.15[x1];\
[x1][2:v]xfade=transition=smoothup:duration=0.35:offset=10.85[vx];\
[vx]subtitles=$CAP:fontsdir=$HOME/.fonts,format=yuv420p[vout];\
[3:a][4:a]acrossfade=d=0.35:c1=tri:c2=tri[a01];\
[a01][5:a]acrossfade=d=0.35:c1=tri:c2=tri[avoz];\
[avoz]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[avozn];\
[6:a]volume=0.15,afade=t=in:st=0:d=0.8,afade=t=out:st=14.6:d=2.0,aresample=48000[amus];\
[avozn][amus]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[aout]" \
  -map "[vout]" -map "[aout]" \
  -c:v libx264 -preset medium -crf 20 -profile:v high -pix_fmt yuv420p \
  -c:a aac -b:a 160k -ar 48000 \
  -movflags +faststart \
  $R/v005_original.mp4 2>&1 | tail -12

echo "=== QA ==="
$FF -v error -i $R/v005_original.mp4 -f null - 2>&1 | tail -3 && echo "OK: v005_original.mp4"
$FF -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of default=noprint_wrappers=1 $R/v005_original.mp4
$FF -v error -select_streams a:0 -show_entries stream=codec_name,sample_rate,channels -of default=noprint_wrappers=1 $R/v005_original.mp4
echo "RENDER V5 FINAL CONCLUÍDO"
