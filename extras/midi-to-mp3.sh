#!/bin/bash
echo "Convirtiendo MIDIs a MP3"

for filename in *.mid; do
    echo "Convirtiendo $filename a MP3"
    timidity $filename -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k $filename.mp3
done

