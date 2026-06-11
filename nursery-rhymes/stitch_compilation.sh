#!/usr/bin/env bash
# Stitch 8s nursery-rhyme clips into one 30-60s vertical short.
# USAGE: put your downloaded .mp4 clips in ./input_clips (named so they sort
# in the order you want), then run:  bash stitch_compilation.sh
# Requires ffmpeg.  Output: nursery_rhymes_compilation.mp4
set -euo pipefail
IN_DIR="${1:-input_clips}"
OUT="${2:-nursery_rhymes_compilation.mp4}"
TMP="$(mktemp -d)"; LIST="$TMP/list.txt"; : > "$LIST"
i=0
for f in "$IN_DIR"/*.mp4; do
  i=$((i+1)); n=$(printf "%02d.mp4" "$i")
  if ffprobe -loglevel error -select_streams a -show_entries stream=codec_type -of csv=p=0 "$f" | grep -q audio; then
    ffmpeg -y -loglevel error -i "$f" \
      -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,format=yuv420p[v]" \
      -map "[v]" -map 0:a:0 -c:v libx264 -preset veryfast -crf 20 -c:a aac -ar 48000 -ac 2 -shortest "$TMP/$n"
  else
    ffmpeg -y -loglevel error -i "$f" -f lavfi -t 8 -i anullsrc=channel_layout=stereo:sample_rate=48000 \
      -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,format=yuv420p[v]" \
      -map "[v]" -map 1:a:0 -c:v libx264 -preset veryfast -crf 20 -c:a aac -ar 48000 -ac 2 -shortest "$TMP/$n"
  fi
  echo "file '$TMP/$n'" >> "$LIST"
done
ffmpeg -y -loglevel error -f concat -safe 0 -i "$LIST" -c copy "$OUT"
echo "Done -> $OUT ($(ffprobe -loglevel error -show_entries format=duration -of csv=p=0 "$OUT")s)"
rm -rf "$TMP"
