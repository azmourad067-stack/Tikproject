#!/bin/sh
# Normalise le volume de chaque épisode à -14 LUFS (standard des plateformes), sans réencoder l'image.
cd "$(dirname "$0")/../episodes" || exit 1
for f in ep*.mp4; do
  ffmpeg -v error -y -i "$f" -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k -movflags +faststart "tmp_$f" && mv "tmp_$f" "$f"
  echo "normalisé : $f"
done
