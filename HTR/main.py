import cv2
import pytesseract

import numpy as np
from PIL import ImageGrab,Image
import time

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

#### Webcam Capture

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



web_cam_capture(0)