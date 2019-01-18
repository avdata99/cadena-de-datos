# crear video con la onda del audio de fondo
ffmpeg -i s01e06-mirofsky.1m.mp3 \
    -filter_complex "[0:a]showwaves=s=400x400:mode=cline,format=yuv420p[v]" \
    -map "[v]" \
    -map 0:a -c:v libx264 \
    -c:a copy \
    s01e06-mirofsky.1m.mp4 

# overlay solo con una imagen
ffmpeg -i input -i background.png -filter_complex "[0:a]showwavespic=s=640x240[fg];[1:v][top]overlay=format=auto" -frames:v 1 output.png

# crear video con la onda del audio de fondo y una imagen
# https://stackoverflow.com/questions/34029575/showfreqs-and-showwaves-over-background-image
TEXTO="Esteban Mirofsy en Cadena de datos"
TTF_FILE="/usr/share/fonts/truetype/ttf-bitstream-vera/Vera.ttf"
FONT_SIZE=30
FONT_COLOR=black
ANCHO=962
ALTO_WAVE=200
ALTO_IMAGEN=328
ALTO=ALTO_WAVE + ALTO_IMAGEN
FILTER="[0:a]showfreqs=mode=line:ascale=log:fscale=log:s=${ANCHO}x${ALTO_IMAGEN}[sf]; \
        [0:a]showwaves=s=${ANCHO}x${ALTO_WAVE}:mode=line[sw]; \
        [sf][sw]vstack[fg]; \
        [1:v]scale=${ANCHO}:-1,crop=iw:${ALTO}[bg]; \
        [bg][fg]overlay=shortest=1:format=auto,format=yuv420p,drawtext=fontfile=$TTF_FILE:fontsize=${FONT_SIZE}:fontcolor=${FONT_COLOR}:x=10:y=10:text='$TEXTO'[out]"

echo $FILTER
echo "*************************************"
cmd="ffmpeg -i s01e06-mirofsky.1m.mp3 \
    -loop 1 \
    -i ~/mirofsky.png \
    -filter_complex \"$FILTER\" \
    -map '[out]' \
    -map 0:a \
    -c:v libx264 \
    -preset fast \
    -crf 18 -c:a libopus \
    s01e06-mirofsky.1m.mkv"

echo "*************************************"
echo $cmd
eval $cmd

ffmpeg -i s01e06-mirofsky.1m.mp3 \
    -loop 1 \
    -i ~/mirofsky.png \
    -filter_complex "[0:a]showfreqs=mode=line:ascale=log:fscale=log:s=800x400[sf]; \
                     [0:a]showwaves=s=800x200:mode=line[sw]; \
                     [sf][sw]vstack[fg]; \
                     [1:v]scale=800:-1,crop=iw:[bg]; \
                     [bg][fg]overlay=shortest=1:format=auto,format=yuv420p,drawtext=fontfile=/usr/share/fonts/truetype/ttf-bitstream-vera/Vera.ttf:fontsize=45:fontcolor=white:x=10:y=10:text='Esteban Mirofsy en Cadena de datos'[out]" \
    -map '[out]' \
    -map 0:a \
    -c:v libx264 \
    -preset fast \
    -crf 18 -c:a libopus \
    s01e06-mirofsky.1m.mkv

https://trac.ffmpeg.org/wiki/Waveform

https://ffmpeg.org/ffmpeg-filters.html#showwaves

size, s
Specify the video size for the output. For the syntax of this option, check the (ffmpeg-utils)"Video size" section in the ffmpeg-utils manual. Default value is 600x240.

mode
Set display mode. Available values are:
‘point’ Draw a point for each sample.
‘line’ Draw a vertical line for each sample.
‘p2p’ Draw a point for each sample and a line between them.
‘cline’ Draw a centered vertical line for each sample.

Default value is point.