echo "Hello! What is your zipcode?" | festival --tts
arecord -D hw:3,0 -f cd -c1 -r 48000 -d 5 -t wav recorded_mono.wav
python3 test_words.py recorded_mono.wav
