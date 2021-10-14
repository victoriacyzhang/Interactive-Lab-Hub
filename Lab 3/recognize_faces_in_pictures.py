import face_recognition
import os

def leaveMessage():
    stream = os.popen('arecord -D hw:3,0 -f cd -c1 -r 48000 -d 2 -t wav recorded_mono.wav').read()
    from speech import answer
    if "yes" in answer:
        stream = os.popen('echo "Sounds good. I will start recording now. You have 10 seconds to record." | festival --tts').read()
        stream = os.popen('arecord -D hw:3,0 -f cd -c1 -r 48000 -d 10 -t wav message.wav').read()
        stream = os.popen('echo "Recording is done. I will let them know of the message. Thanks!" | festival --tts').read()
    elif "no" in answer:
        stream = os.popen('echo "That is fine. Thank you. Bye!" | festival --tts').read()
    else:
        stream = os.popen('echo "I am sorry I did not catch that. I will take it as a no. Bye!" | festival --tts').read()
    quit()

stream = os.popen('echo "Knock knock, who is there! Lets verify your identity first. Can I take a photo to confirm who you are? Please answer yes or no." | festival --tts').read()
stream = os.popen('arecord -D hw:3,0 -f cd -c1 -r 48000 -d 2 -t wav recorded_mono.wav').read()
from speech import answer
if "yes" in answer:
    stream = os.popen('echo "Thank you, I will take a picture now!" | festival --tts').read()
elif "no" in answer:
    stream = os.popen('echo "That is fine. Thank you. Bye!" | festival --tts').read()
    quit()
else:
    stream = os.popen('echo "I am sorry I did not catch that. I will take it as a no. Would you like to leave a message? Please answer yes or no." | festival --tts').read()
    leaveMessage()
stream = os.popen('fswebcam --fps 15 -S 8 -r 1280x960 images/image.jpg').read()
stream = os.popen('echo "Photo done. Please give me a moment to analyze them." | festival --tts')
victoria_image = face_recognition.load_image_file("./images/victoria.jpg")
unknown_image = face_recognition.load_image_file("./images/image.jpg")

try:
    victoria_face_encoding = face_recognition.face_encodings(victoria_image)[0]
    unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
except IndexError:
    stream = os.popen('echo "Your face was not in the frame. Verification unsucessful. Would you like to leave a message? Please answer yes or no." | festival --tts').read()
    leaveMessage()

known_faces = [
    victoria_face_encoding,
]

results = face_recognition.compare_faces(known_faces, unknown_face_encoding)
if results[0] == True:
    if os.path.exists("message.wav"):
        stream = os.popen('echo "Verification successful. Welcome home! You have a message from a guest" | festival --tts').read()
        import simpleaudio as sa
        from pydub import AudioSegment
        m = AudioSegment.from_wav('message.wav')
        m = m + 40
        m.export('message.wav', 'wav')
        filename = 'message.wav'
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        play_obj.wait_done()
        stream = os.popen('rm message.wav').read()
    else:
        stream = os.popen('echo "Verification successful. Welcome home! You do not have any messages from guests." | festival --tts').read()

else:
    stream = os.popen('echo "You do not live here. Would you like to leave a message? Please answer yes or no." | festival --tts').read()
    leaveMessage()
