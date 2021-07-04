import cv2
import re
import pytesseract
import numpy as np
from PIL import ImageGrab
import pyttsx3
import time

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


###### Detecting Words #######

def detecting_words(path):
    img = cv2.imread(path)
    # img = cv2.medianBlur(img, 5)
    # hImg, wImg, _ = img.shape
    # img = cv2.resize(img, (int(wImg/1.3), int(hImg/1.3)))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    boxes = pytesseract.image_to_data(img)
    for a, b in enumerate(boxes.splitlines()):
        # print(b)
        if a != 0:
            b = b.split()
            if len(b) == 12:
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                cv2.putText(img, b[11], (x, y - 4), cv2.FONT_HERSHEY_SIMPLEX, .7, (50, 50, 255), 2)
                cv2.rectangle(img, (x, y), (x + w, y + h), (50, 50, 255), 2)
    txt = print_whole_text(img)
    cv2.imshow('Detected words', img)
    cv2.waitKey(0)
    # print(txt)
    speak(txt)
    return img, txt


def print_whole_text(img):
    custom_config = r'-l eng+por+grc+tha+kor+spa+jpn+ara+rus --psm 6'
    return pytesseract.image_to_string(img, config=custom_config)


def print_only_digits(img):
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    return pytesseract.image_to_string(img, config=custom_config)


def print_only_char(img):
    custom_config = r'-c tessedit_char_blacklist=0123456789 --psm 6'
    return pytesseract.image_to_string(img, config=custom_config)


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', 'voices[0].id')
newVoiceRate = 145
engine.setProperty('rate', newVoiceRate)


def speak(txt):
    """
    this function which
    converts text to speech
    """
    engine.say(txt)
    engine.runAndWait()


detecting_words('data/hitchhikers-rotated.png')
