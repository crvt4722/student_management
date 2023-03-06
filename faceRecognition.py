import cv2
import numpy as np
import os
from PIL import Image
from encode_decode import decodeStudent

data_trained = []
def faceRecognition():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('recognizer/trainingData.yml')

    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    fontface = cv2.FONT_HERSHEY_SIMPLEX

    stu_predict = []
    while True:
        # Camera
        red, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray)
        for (x, y, w, h) in faces:
            if w > 170 and h > 170:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                id, confidence = recognizer.predict(roi_gray)
                stu_code = decodeStudent(id)
                # fullname = userDAO.getFullName(stu_code)
                if confidence < 68:
                    cv2.putText(frame, stu_code, (x + 10, y + h + 30), fontface, 1, (0, 255, 0), 2)
                    stu_predict.append(stu_code)
                else:
                    cv2.putText(frame, 'Unknown', (x + 10, y + h + 30), fontface, 1, (0, 255, 0), 2)

        cv2.imshow('Image', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return max(set(stu_predict), key= stu_predict.count)

def takePhotos(id):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    cap = cv2.VideoCapture(0)
    cnt = 0
    while True:

        # Camera
        red, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray)

        if not os.path.exists('dataSet'):
            os.makedirs('dataSet')

        for (x, y, w, h) in faces:
            if w > 160 and h > 160:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Store image to file.
                cnt += 1
                cv2.imwrite('dataSet/User.' + str(id) + '.' + str(cnt) + '.jpg', gray[y:y + h, x:x + w])

        cv2.imshow('Detecting face', frame)
        cv2.waitKey(1)

        # Exit if the number of image is greater than 200.
        if cnt > 100:
            break

    cap.release()
    cv2.destroyAllWindows()


def trainData():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path = 'dataSet'

    def getImagesWidthID(path):
        # Get image's path in the folder.
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

        print(imagePaths)

        faces = []
        IDs = []

        for imagePaths in imagePaths:
            # if imagePaths in data_trained:
            #     continue

            faceImg = Image.open(imagePaths).convert('L')
            faceNp = np.array(faceImg, 'uint8')
            print(faceNp)

            # Get ID from file path.
            ID = int(imagePaths.split('\\')[1].split('.')[1])
            print(imagePaths, ID)
            faces.append(faceNp)
            IDs.append(ID)

            # cv2.imshow('Training', faceNp)
            cv2.waitKey(1)
            # data_trained.append(imagePaths)

        return faces, IDs

    faces, IDs = getImagesWidthID(path)

    # Train data
    recognizer.train(faces, np.array(IDs))

    # Store training data to file.
    if not os.path.exists('recognizer'):
        os.makedirs('recognizer')

    recognizer.save('recognizer/trainingData.yml')
    cv2.destroyAllWindows()
