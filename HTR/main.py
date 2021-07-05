import cv2
import pytesseract
from PIL import ImageGrab
import time
import numpy as np
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


##### Detecting ONLY Digits  ######

def detect_only_digit(path):

     img = cv2.imread(path)
     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
     print(pytesseract.image_to_string(img))
     hImg, wImg,_ = img.shape
     conf = r'--oem 3 --psm 6 outputbase digits'
     boxes = pytesseract.image_to_boxes(img,config=conf)
     for b in boxes.splitlines():
          # print(b)
          b = b.split(' ')
          # print(b)
          x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
          cv2.rectangle(img, (x,hImg-y), (w,hImg-h), (50, 50, 255), 2)
          cv2.putText(img,b[0],(x,hImg- y+25),cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,255),2)
     cv2.imshow('img', img)
     cv2.waitKey(0)
     return img

detect_only_digit('data/sewar1.png')








