arecord -D hw:3,0 -f cd -c1 -r 48000 -d 2 -t wav recorded_mono.wav
python3 speech.py recorded_mono.wav
