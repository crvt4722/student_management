import cv2
import numpy
import os

id = input('ID:')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)
cnt = 0
while True:

    # Camera
    red,frame = cap.read()

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray)

    if not os.path.exists('dataSet'):
        os.makedirs('dataSet')

    for (x,y,w,h) in faces:
        if w > 160 and h > 160:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Store image to file.
            cnt += 1
            cv2.imwrite('dataSet/User.' + id + '.' + str(cnt) + '.jpg', gray[y:y + h, x:x + w])


    cv2.imshow('Detecting face',frame)
    cv2.waitKey(1)

    # Exit if the number of image is greater than 200.
    if cnt > 200:
        break

cap.release()
cv2.destroyAllWindows()