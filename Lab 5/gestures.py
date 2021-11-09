
#This example is directly copied from the Tensorflow examples provided from the Teachable Machine.

import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import cv2
import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import random
import qwiic_joystick
import sys

# drawing code start
# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
font_time = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
# drawing code end

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

img = None
webCam = False
if(len(sys.argv)>1 and not sys.argv[-1]== "noWindow"):
   try:
      print("I'll try to read your image");
      img = cv2.imread(sys.argv[1])
      if img is None:
         print("Failed to load image file:", sys.argv[1])
   except:
      print("Failed to load the image are you sure that:", sys.argv[1],"is a path to an image?")
else:
   try:
      print("Trying to open the Webcam.")
      cap = cv2.VideoCapture(0)
      if cap is None or not cap.isOpened():
         raise("No camera")
      webCam = True
   except:
      print("Unable to access webcam.")


# Load the model
model = tensorflow.keras.models.load_model('hand_keras_model.h5', compile=False)
# Load Labels:
labels=[]
f = open("hand_labels.txt", "r")
for line in f.readlines():
    if(len(line)<1):
        continue
    labels.append(line.split(' ')[1].strip())

game = False
readValue = False
gestures = ["rock", "paper", "scissor"]
point = 5
message = ""
message2 = ""
message3 = ""
message4 = ""
while(True):
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    if (point < 1):
        draw.text((10, 50), "You lost, sorry!", font=font, fill="#ffffff")
        disp.image(image, rotation)
        break
    if (point > 10):
        draw.text((10, 50), "You are a winner!", font=font, fill="#ffffff")
        disp.image(image, rotation)
        break
    
    if readValue:
        if webCam:
            ret, img = cap.read()

        rows, cols, channels = img.shape
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        size = (224, 224)
        img =  cv2.resize(img, size, interpolation = cv2.INTER_AREA)
        #turn the image into a numpy array
        image_array = np.asarray(img)

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        # Load the image into the array
        data[0] = normalized_image_array

        # run the inference
        prediction = model.predict(data)
        currGesture = labels[np.argmax(prediction)]
        #print("I think its a:",labels[np.argmax(prediction)])

        if webCam:
            if sys.argv[-1] == "noWindow":
                cv2.imwrite('detected_out.jpg',img)
                continue
            cv2.imshow('detected (press q to quit)',img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                break
        else:
            break

    # drawing code starts
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    if (not buttonA.value) or (not buttonB.value):
        message = "Ready? Setting up..."
        print("hmmm")
        game = True
    if not game:
        message = "Want to play a game?"
        message2 = "Press a button to start."
    elif (game) and (not readValue):
        draw.text((10, 50), "rock, paper, scissor...", font=font, fill="#ffffff")
        disp.image(image, rotation)
        time.sleep(2)
        readValue = True
        continue
        #draw.rectangle((0, 0, width, height), outline=0, fill=0)
    else:
        robotGesture = gestures[random.randint(0,2)]
        if ((currGesture == "rock") and (robotGesture == "rock")) or ((currGesture == "scissor") and (robotGesture == "scissor")) or ((currGesture == "paper") and (robotGesture == "paper")):
            message = "It is a tie! I had a " + robotGesture
            message2 = "You gave: " + currGesture
            message3 = "I gave: " + robotGesture
            message4 = "Points: " + str(point)
        elif (currGesture == "rock") and (robotGesture == "scissor"):
            message = "You won this round!"
            message2 = "You gave: " + currGesture
            message3 = "I gave: " + robotGesture
            point += 1
            message4 = "Points: " + str(point)
        elif (currGesture == "paper") and (robotGesture == "rock"):
            message = "You won this round!"
            message2 = "You gave: " + currGesture
            message3 = "I gave: " + robotGesture
            point += 1
            message4 = "Points: " + str(point)
        elif (currGesture == "scissor") and (robotGesture == "paper"):
            message = "You won this round!"
            message2 = "You gave: " + currGesture
            message3 = "I gave: " + robotGesture
            point += 1
            message4 = "Points: " + str(point)
        else:
            message = "You lost this round:("
            message2 = "You gave: " + currGesture
            message3 = "I gave: " + robotGesture
            point -= 1
            message4 = "Points: " + str(point)
        readValue = False
    draw.text((10, 10), message, font=font, fill="#ffffff")
    draw.text((10, 30), message2, font=font, fill="#ffffff")
    draw.text((10, 50), message3, font=font, fill="#ffffff")
    draw.text((10, 70), message4, font=font, fill="#ffffff")
    disp.image(image, rotation)
    if message3 is not "":
        time.sleep(4)
    message = ""
    message2 = ""
    message3 = ""
    message4 = ""
    #if "to start" not in message:
    #    time.sleep(4)
    # drawing code ends


cv2.imwrite('detected_out.jpg',img)
cv2.destroyAllWindows()
