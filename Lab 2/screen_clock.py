import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep
from astral import Astral
import datetime
from datetime import date

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

city_name = 'New York'
a = Astral()
a.solar_depression = 'civil'
city = a[city_name]
sun = city.sun(date=date.today(), local=True)
headline = ""
food = ""
imageName = ""
now = datetime.datetime.now()
datestr = now.strftime("%B %d, %Y")

def getTime(time):
    seq = time.strftime("%Y%m%d%H%M%S")[-6:]
    now_h = seq[0:2]
    now_m = seq[2:4]
    now_s = seq[4:]
    return [now_h, now_m, now_s]

def compTime(now, com):
    if (now[0] > com[0]):
        return True
    elif (now[0] == com[0]):
        if (now[1] > com[1]):
            return True
        elif (now[1] == com[1]):
            if (now[2] > com[2]):
                return True
    return False

def displayBinary(l):
    res = ""
    for ele in l:
        if ele  == 1:
            res = res + "* "
        else:
            res = res + "- "
    return res

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py 
    currTime = strftime("%H:%M:%S")
    now_t = getTime(datetime.datetime.now())
    hour = int(now_t[0])
    minute = int(now_t[1])
    second = int(now_t[2])
    hour_binary = displayBinary([int(i) for i in list('{0:0b}'.format(hour))])
    minute_binary = displayBinary([int(i) for i in list('{0:0b}'.format(minute))])
    second_binary = displayBinary([int(i) for i in list('{0:0b}'.format(second))])
    evening_t = getTime(sun['sunset'])
    if (compTime(now_t, evening_t)):
        headline = "Good evening, New York!"
        food = "Don't forget your dinner!"
        imageName = "ny_evening.jpeg"
    elif (compTime(now_t, getTime(sun['noon']))):
        headline = "Good afternoon, New York!"
        food = "Don't forget your lunch!"
        imageName = "ny_afternoon.jpeg"
    else:
        headline = "Good morning, New York!"
        food = "Don't forget your breakfast!"
        imageName = "ny_morning.jpeg"
    proportion_day = (int(now_t[0]) * 60 * 60 + int(now_t[1]) * 60 + int(now_t[2])) / 86400 * 100
    proportion_day_str = "You have completed " + str(int(proportion_day)) + "% of today. Congrats!"
    if (not buttonA.value) and buttonB.value:
        draw.text((10, 40), proportion_day_str[:19], font=font, fill="#F4C2C2")
        draw.text((10, 65), proportion_day_str[19:], font=font, fill="#F3C2C2")
        disp.image(image, rotation)
    elif (not buttonB.value) and buttonA.value:
        draw.text((10,50), food, font=font, fill="#91B500")
        disp.image(image, rotation)
    elif (not buttonA.value) and (not buttonB.value):
        draw.text((20,20), hour_binary, font=font_time, fill="#808080")
        draw.text((20,50), minute_binary, font=font_time, fill="#808080")
        draw.text((20,80), second_binary, font=font_time, fill="#808080")
        disp.image(image, rotation)
    else:
        draw.text((0, 0), headline, font=font, fill="#89CFF0")
        draw.text((0, 25), datestr, font=font, fill="#89CFF0")
        draw.text((0, 60), currTime, font=font_time, fill="#808080")
        disp.image(image, rotation)
