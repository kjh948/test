gtts-cli "$1" -l 'ko' -o tmp.mp3 && play -q tmp.mp3 
rm tmp.mp3
exit
gtts-cli "$1" -l 'ko' | play -t mp3 - \
overdrive 10 \
echo 0.8 0.8 5 0.7 \
echo 0.8 0.7 6 0.7 \
echo 0.8 0.7 10 0.7 \
echo 0.8 0.7 12 0.7 \
echo 0.8 0.88 12 0.7 \
echo 0.8 0.88 30 0.7 \
echo 0.6 0.6 60 0.7 \
gain 8
