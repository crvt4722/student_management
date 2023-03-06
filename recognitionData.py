import cv2
import numpy as np
import os
from PIL import Image

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('recognizer/trainingData.yml')

cap = cv2.VideoCapture(0)
fontface = cv2.FONT_HERSHEY_SIMPLEX

while True:
    # Camera
    red, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray)
    for (x,y,w,h) in faces:
        if w > 170 and h > 170 :
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            id,confidence = recognizer.predict(roi_gray)

            if confidence < 68:
                cv2.putText(frame,str(id),(x+10,y+h+30),fontface,1,(0,255,0),2)
            else:
                cv2.putText(frame,'Unknown',(x+10,y+h+30),fontface,1,(0,255,0),2)

    cv2.imshow('Image',frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()