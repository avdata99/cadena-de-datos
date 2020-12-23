# crear video con la onda del audio de fondo y una imagen
# https://stackoverflow.com/questions/34029575/showfreqs-and-showwaves-over-background-image
TEXTO="Cadena de datos con Pablo De Grande. Episodio 36"
TTF_FILE="/usr/share/fonts/truetype/ttf-bitstream-vera/Vera.ttf"
FONT_SIZE=30
FONT_COLOR=black
ANCHO=1142
ANCHO_WAVE1=310
ANCHO_WAVE2=310
ALTO_WAVE1=2
ALTO_WAVE2=350
ALTO_IMAGEN=672
ALTO=ALTO_WAVE1 + ALTO_WAVE2 + ALTO_IMAGEN
SAMPLESXCOLUMN=3
COLOR_ONDA=00AAAA
# Modo de la onda:
# point: Draw a point for each sample.
# line: Draw a vertical line for each sample.
# p2p: Draw a point for each sample and a line between them.
# cline: Draw a centered vertical line for each sample.
WAVE_MODE="cline"
FILTER="[0:a]showfreqs=mode=bar:ascale=lin:fscale=lin:s=${ANCHO_WAVE1}x${ALTO_WAVE1}[sf]; \
        [0:a]showwaves=s=${ANCHO_WAVE2}x${ALTO_WAVE2}:mode=${WAVE_MODE}:n=${SAMPLESXCOLUMN}:colors=${COLOR_ONDA}[sw]; \
        [sf][sw]vstack[fg]; \
        [1:v]scale=${ANCHO}:-1,crop=iw:${ALTO_IMAGEN}[bg]; \
        [bg][fg]overlay=shortest=1:format=auto,format=yuv420p,drawtext=fontfile=$TTF_FILE:fontsize=${FONT_SIZE}:fontcolor=${FONT_COLOR}:x=5:y=5:text='$TEXTO'[out]"

echo $FILTER
echo "*************************************"
cmd="ffmpeg -i audio.mp3 \
    -loop 1 -y \
    -i imagen.png \
    -filter_complex \"$FILTER\" \
    -map '[out]' \
    -map 0:a \
    -c:v libx264 \
    -preset fast \
    -crf 18 -c:a libopus \
    video.mkv"

echo "*************************************"
echo $cmd
eval $cmd

# https://trac.ffmpeg.org/wiki/Waveform
# https://ffmpeg.org/ffmpeg-filters.html#showwaves