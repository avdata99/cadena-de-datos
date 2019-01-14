# https://askubuntu.com/questions/868283/ffmpeg-mp3-jpg-mp4-howto-make-video-smaller

ffmpeg -loop 1 -framerate 1 -i ruso03.png -i ruso.mp3 \
-c:v libx264 -preset veryslow -crf 0 -c:a copy -shortest ruso.mkv


ffmpeg -loop 1 -framerate 1 -i se01e03-selvood.jpg -i se01e03-selvood.mp3 \
-c:v libx264 -preset veryslow -crf 0 -c:a copy -shortest se01e03-selvood.mkv
