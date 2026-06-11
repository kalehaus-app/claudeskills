#!/usr/bin/env bash
# Builds a ~32s vertical nursery-rhyme short from 4 clips.
# Run this on your OWN machine (the cloud session can't reach the Higgsfield CDN).
# Requires: ffmpeg, curl.   Output: nursery_30s_short.mp4
set -euo pipefail
urls=(
"https://d8j0ntlcm91z4.cloudfront.net/user_3C5niICYToBtuRckDNTBnm68Okj/hf_20260611_175525_2b0a4db8-f69d-44dd-943a-ff932f783f06.mp4"  # Wheels on the Bus (animals)
"https://d8j0ntlcm91z4.cloudfront.net/user_3C5niICYToBtuRckDNTBnm68Okj/hf_20260611_180132_7048504d-a7bd-4699-bba1-df145073f59b.mp4"  # Itsy Bitsy Spider
"https://d8j0ntlcm91z4.cloudfront.net/user_3C5niICYToBtuRckDNTBnm68Okj/hf_20260611_180136_94e41f41-4a67-4afa-a377-f983424d0ebd.mp4"  # Five Little Ducks
"https://d8j0ntlcm91z4.cloudfront.net/user_3C5niICYToBtuRckDNTBnm68Okj/hf_20260611_180726_2b83312a-fe87-4e9d-9e2c-fba074d0dec3.mp4"  # Bingo
)
TMP="$(mktemp -d)"; LIST="$TMP/list.txt"; : > "$LIST"; i=0
for u in "${urls[@]}"; do
  i=$((i+1)); raw="$TMP/raw_$i.mp4"; out="$TMP/$(printf '%02d.mp4' "$i")"
  curl -fsSL "$u" -o "$raw"
  ffmpeg -y -loglevel error -i "$raw" \
    -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,format=yuv420p[v]" \
    -map "[v]" -map 0:a:0 -c:v libx264 -preset veryfast -crf 20 -c:a aac -ar 48000 -ac 2 -shortest "$out"
  echo "file '$out'" >> "$LIST"
done
ffmpeg -y -loglevel error -f concat -safe 0 -i "$LIST" -c copy nursery_30s_short.mp4
echo "Done -> nursery_30s_short.mp4 ($(ffprobe -loglevel error -show_entries format=duration -of csv=p=0 nursery_30s_short.mp4)s)"
rm -rf "$TMP"
