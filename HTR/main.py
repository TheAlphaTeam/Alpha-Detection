import cv2
import pytesseract

import numpy as np
from PIL import ImageGrab,Image
import time

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

###########################################
#### Webcam and Screen Capture Example ######
#############################################
# def captureScreen(bbox=(300,300,1500,1000)):
#     capScr = np.array(ImageGrab.grab(bbox))
#     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
#     return capScr

cap = cv2.VideoCapture(0)
cap.set(3,1200)
cap.set(4,480)

cntr=0
while True:
    time.sleep(1)
    timer = cv2.getTickCount()
    _,img = cap.read()
    cntr=cntr+1
    # img = captureScreen()
    hImg, wImg,_ = img.shape
    x1,y1,w1,h1=0,0,hImg,wImg
    img_text=pytesseract.image_to_string(img)
    boxes = pytesseract.image_to_boxes(img)
    for b in boxes.splitlines():
        #print(b)
        b = b.split(' ')
        #print(b)
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(img, (x,hImg- y), (w,hImg- h), (50, 50, 255), 2)
        cv2.putText(img,img_text,(x1+int(w1/40),y1+int(h1/40)),cv2.FONT_HERSHEY_SIMPLEX,.7,(255,0,0),2)
    # fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
    # print(fps)
    # cv2.putText(img, str(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (20,230,20), 2);
    cv2.imshow("Result",img)
    # cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#

# key = cv2.waitKey(1)
# webcam = cv2.VideoCapture(0)
# while True:
#     try:
#         check, frame = webcam.read()
#         print(check)  # prints true as long as the webcam is running
#         print(frame)  # prints matrix values of each framecd
#         cv2.imshow("Capturing", frame)
#         key = cv2.waitKey(1)
#         if key == ord('s'):
#             cv2.imwrite(filename='saved_img.jpg', img=frame)
#             webcam.release()
#             img_new = cv2.imread('saved_img.jpg', cv2.IMREAD_GRAYSCALE)
#             img_new = cv2.imshow("Captured Image", img_new)
#             cv2.waitKey(1650)
#             cv2.destroyAllWindows()
#             print("Processing image...")
#             img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
#             print("Converting RGB image to grayscale...")
#             gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
#             print("Converted RGB image to grayscale...")
#             print("Resizing image to 28x28 scale...")
#             img_ = cv2.resize(gray, (28, 28))
#             print("Resized...")
#             img_resized = cv2.imwrite(filename='saved_img-final.jpg', img=img_)
#             print("Image saved!")
#
#             break
#         elif key == ord('q'):
#             print("Turning off camera.")
#             webcam.release()
#             print("Camera off.")
#             print("Program ended.")
#             cv2.destroyAllWindows()
#             break
#
#     except(KeyboardInterrupt):
#         print("Turning off camera.")
#         webcam.release()
#         print("Camera off.")
#         print("Program ended.")
#         cv2.destroyAllWindows()
#         break