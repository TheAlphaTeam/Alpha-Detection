import cv2
import re
from PIL import ImageGrab, Image
import pytesseract
import numpy as np
import pyttsx3
import time
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk
from textblob import TextBlob
import playsound
import random
from gtts import gTTS
import os


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

image_txt = ''
edited_img = ''
global_path = ''
trans_txt = ''

HTR = Tk()
HTR.iconbitmap('slogo.ico')
HTR.title("AD")

bg = ImageTk.PhotoImage(file="data/wp.jpg")
canvas = Canvas(HTR, width=700, height=600)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg, anchor="nw")

img = PhotoImage(file="data/logo.png")
canvas.create_image(200,60, anchor=NW, image=img)


def browse_button_char():
    detect_Char(global_path)


def browse_button_digit():
    detect_only_digit(global_path)


def browse_button_translate():
    translate(global_path)


def browse_button():
    filename = filedialog.askopenfile()
    print(filename)
    read_words(filename.name)


def read():
    speak(image_txt)


def speak_arabic():
    speak_ar(trans_txt)


def show_img():
    cv2.imshow('Detected words', edited_img)
    cv2.waitKey(0)



# def window():
#     newWindow = Toplevel(HTR)
#     newWindow.iconbitmap('slogo.ico')
#     newWindow.title("AD")
#     bg = ImageTk.PhotoImage(file="data/wp.jpg")
#     canvas = Canvas(newWindow, width=500, height=600)
#     canvas.pack(fill="both", expand=True)
#     canvas.create_image(0, 0, image=bg, anchor="nw")
#
#     digit = Button(newWindow, height=1, width=15, text="Digit Detect ", command=browse_button_digit, bg='#FB405A', fg='#f2f2f2')
#     digit.config(font=("serf bold", 15))
#     digit.place(relx=0.15, rely=0.15, relwidth=.7, relheight=0.05)
#     char = Button(newWindow, height=1, width=15, text="Character Detect", command=browse_button_char, bg='#FB405A', fg='#f2f2f2')
#     char.config(font=("serf bold", 15))
#     char.place(relx=0.15, rely=0.3, relwidth=.7, relheight=0.05)
#     word = Button(newWindow, text="Word Detect", command=browse_button_word_detect, bg='#FB405A', fg='#f2f2f2')
#     word.config(font=("serf bold", 15))
#     word.place(relx=0.15, rely=0.45, relwidth=.7, relheight=0.05)
#
#     voice = Button(newWindow, text="Read & Listen", command=browse_button_speak, bg='#FB405A', fg='#f2f2f2')
#     voice.config(font=("serf bold", 15))
#     voice.place(relx=0.15, rely=0.75, relwidth=.7, relheight=0.05)
#
#     newWindow.mainloop()





##### Detecting ONLY Digits  ####


def detect_only_digit(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    print(pytesseract.image_to_string(img))
    hImg, wImg, _ = img.shape
    conf = r'--oem 3 --psm 6 outputbase digits'
    boxes = pytesseract.image_to_boxes(img, config=conf)
    for b in boxes.splitlines():
        b = b.split(' ')
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (50, 50, 255), 2)
        cv2.putText(img, b[0], (x, hImg - y + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)
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
    txt = ''
    for a, b in enumerate(boxes.splitlines()):
        if a != 0:
            b = b.split()
            if len(b) == 12:
                txt += f' {b[11]}'
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                cv2.putText(img, b[11], (x, y - 4), cv2.FONT_HERSHEY_SIMPLEX, .7, (50, 50, 255), 2)
                cv2.rectangle(img, (x, y), (x + w, y + h), (50, 50, 255), 2)
    print(txt)
    cv2.imshow('Detected words', img)
    cv2.waitKey(0)

    return img, txt


def read_words(path):
    global global_path
    global image_txt
    global edited_img
    global_path = path
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hImg, wImg, _ = img.shape
    boxes = pytesseract.image_to_data(img)
    txt = ''
    for a, b in enumerate(boxes.splitlines()):
        if a != 0:
            b = b.split()
            if len(b) == 12:
                txt += f' {b[11]}'
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                cv2.putText(img, b[11], (x, y - 4), cv2.FONT_HERSHEY_SIMPLEX, .7, (50, 50, 255), 2)
                cv2.rectangle(img, (x, y), (x + w, y + h), (50, 50, 255), 2)
    edited_img = img
    image_txt = txt
    root=Toplevel(HTR)
    root.title("AD")
    root.geometry("800x600")
    root.iconbitmap('slogo.ico')
    T = Text(root,height=25, width=150,font=("Helvetica",18))
    T.insert(END, txt)
    T.pack()
    speker = Button(T,height=1, width=15, text="Listen", command=read, bg='#FB405A', fg='#f2f2f2')
    speker.config(font=("serf bold", 12))
    speker.place(relx=0.55, rely=0.85)
    translate = Button(T, height=1, width=15, text="Translate", command=browse_button_translate, bg='#FB405A', fg='#f2f2f2')
    translate.config(font=("serf bold", 12))
    translate.place(relx=0.75, rely=0.85)
    show = Button(T, height=1, width=15, text="show Image", command=show_img, bg='#FB405A', fg='#f2f2f2')
    show.config(font=("serf bold", 12))
    show.place(relx=0.05, rely=0.85)
    digit = Button(T, height=1, width=15, text="Digit Detect ", command=browse_button_digit, bg='#FB405A',fg='#f2f2f2')
    digit.config(font=("serf bold", 12))
    digit.place(relx=0.25, rely=0.85)
    root.mainloop()


def translate(path):
    global trans_txt
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    boxes = pytesseract.image_to_data(img)
    txt = ''
    for a, b in enumerate(boxes.splitlines()):
        if a != 0:
            b = b.split()
            if len(b) == 12:
                txt += f' {b[11]}'

    blob = TextBlob(txt)

    newWindow = Toplevel(HTR)
    newWindow.iconbitmap('slogo.ico')
    newWindow.title("AD")
    T =Text(newWindow, height=15, width=40,font=("Helvetica",18))
    T.pack()
    T.insert('1.0',f'{blob.translate(to="ar")}')
    trans_txt = f'{blob.translate(to="ar")}'
    speker = Button(T,height=1, width=15, text="Listen", command=speak_arabic, bg='#FB405A', fg='#f2f2f2')
    speker.config(font=("serf bold", 12))
    speker.place(relx=0.6, rely=0.85)
    print('TR',blob.translate(to='ar'))
    newWindow.mainloop()



#### Webcam Capture  ####

iter_img=0
def web_cam_capture(path=0):
    cap = cv2.VideoCapture(path)
    cap.set(3, 1200)
    cap.set(4, 480)
    while True:
        _, img = cap.read()
        cv2.imwrite("data/new_picture.jpg", img)
        hImg, wImg, _ = img.shape
        x1, y1, w1, h1 = 0, 0, hImg, wImg
        img_text = pytesseract.image_to_string(img)
        boxes = pytesseract.image_to_boxes(img)
        for b in boxes.splitlines():
            b = b.split(' ')
            x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
            cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (50, 50, 255), 2)
            cv2.putText(img, img_text, (x1 + int(w1 / 40), y1 + int(h1 / 40)), cv2.FONT_HERSHEY_SIMPLEX, .7,
                        (50, 50, 255), 2)
        cv2.imshow("Result", img)
        time.sleep(.5)
        if cv2.waitKey(1) & 0xFF == ord('c') or cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            read_words("data/new_picture.jpg")
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
newVoiceRate = 125
engine.setProperty('rate', newVoiceRate)


def speak_ar(string):
    tts = gTTS(text=string, lang='ar', slow=False)
    r = random.randint(1, 9000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    os.remove(audio_file)


def speak(txt):
    """
    this function which
    converts text to speech
    """
    engine.say(txt)
    engine.runAndWait()


Browse = Button(height=1, width=15, text="Browse Image ", command=browse_button, bg='#FB405A', fg='#f2f2f2')
Browse.config(font=("serf bold", 15))
Browse.place(relx=0.15, rely=0.7)
realtime = Button(height=1, width=15, text="Cam Detect", command=web_cam_capture, bg='#FB405A', fg='#f2f2f2')
realtime.config(font=("serf bold", 15))
realtime.place(relx=0.6, rely=0.7)

HTR.mainloop()
