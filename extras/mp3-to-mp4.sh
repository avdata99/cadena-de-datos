# https://askubuntu.com/questions/868283/ffmpeg-mp3-jpg-mp4-howto-make-video-smaller

ffmpeg -loop 1 -framerate 1 -i ruso03.png -i ruso.mp3 \
-c:v libx264 -preset veryslow -crf 0 -c:a copy -shortest ruso.mkv


ffmpeg -loop 1 -framerate 1 -i s01e16-runixo.jpg -i s01e16-runixo.mp3 \
-c:v libx264 -preset veryslow -crf 0 -c:a copy -shortest s01e16-runixo.mkv

# mp4 to mp3
ffmpeg -i s01e04-tony.mp4 s01e04-tony.mp3