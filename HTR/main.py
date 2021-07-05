import cv2
import re
from PIL import ImageGrab, Image
import pytesseract
import numpy as np
import pyttsx3
import time
import tkinter

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


##### Detecting ONLY Digits  ####

def detect_only_digit(path):

     img = cv2.imread(path)
     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
     print(pytesseract.image_to_string(img))
     hImg, wImg,_ = img.shape
     conf = r'--oem 3 --psm 6 outputbase digits'
     boxes = pytesseract.image_to_boxes(img,config=conf)
     for b in boxes.splitlines():
          b = b.split(' ')
          x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
          cv2.rectangle(img, (x,hImg-y), (w,hImg-h), (50, 50, 255), 2)
          cv2.putText(img,b[0],(x,hImg- y+25),cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,255),2)
     cv2.imshow('img', img)
     cv2.waitKey(0)
     return img



#### Detecting Characters ####

def detect_Char(path):

    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hImg, wImg, _ = img.shape
    boxes = pytesseract.image_to_boxes(img)
    for b in boxes.splitlines():
        b = b.split(' ')
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (50, 50, 255), 1)
        cv2.putText(img, b[0], (x, hImg - y + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)
    cv2.imshow('img', img)
    cv2.waitKey(0)

    return img


#### Detecting Words  ####

def detecting_words(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    boxes = pytesseract.image_to_data(img)
    for a, b in enumerate(boxes.splitlines()):
        if a != 0:
            b = b.split()
            if len(b) == 12:
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                cv2.putText(img, b[11], (x, y - 4), cv2.FONT_HERSHEY_SIMPLEX, .7, (50, 50, 255), 2)
                cv2.rectangle(img, (x, y), (x + w, y + h), (50, 50, 255), 2)
    txt = print_whole_text(img)
    cv2.imshow('Detected words', img)
    cv2.waitKey(0)
    return img, txt



#### Webcam Capture  ####

def web_cam_capture(path):

    cap = cv2.VideoCapture(path)
    cap.set(3,1200)
    cap.set(4,480)

    while True:
        time.sleep(1)
        _,img = cap.read()

        hImg, wImg,_ = img.shape
        x1,y1,w1,h1=0,0,hImg,wImg
        img_text=pytesseract.image_to_string(img)
        boxes = pytesseract.image_to_boxes(img)
        for b in boxes.splitlines():
            b = b.split(' ')
            x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
            cv2.rectangle(img, (x,hImg- y), (w,hImg- h), (50, 50, 255), 2)
            cv2.putText(img,img_text,(x1+int(w1/40),y1+int(h1/40)),cv2.FONT_HERSHEY_SIMPLEX,.7,(255,0,0),2)
        cv2.imshow("Result",img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


#### write functions as Text_string ####


def print_only_digits(img):
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    return pytesseract.image_to_string(img, config=custom_config)


def print_only_char(img):
    custom_config = r'-c tessedit_char_blacklist=0123456789 --psm 6'
    return pytesseract.image_to_string(img, config=custom_config)

def print_whole_text(img):
    custom_config = r'-l eng+por+grc+tha+kor+spa+jpn+ara+rus --psm 6'
    return pytesseract.image_to_string(img, config=custom_config)


#### voice over ####

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




if __name__=='__main__':
    detect_only_digit('data/sewar1.png')
    detect_Char('data/S-Z.png')
    detecting_words('data/hitchhikers-rotated.png')
    web_cam_capture(0)