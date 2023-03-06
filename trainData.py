import cv2
import numpy as np
import os
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()
path  = 'dataSet'

def getImagesWidthID(path):
    # Get image's path in the folder.
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]

    print(imagePaths)

    faces = []
    IDs = []

    for imagePaths in imagePaths:
        faceImg=Image.open(imagePaths).convert('L')
        faceNp = np.array(faceImg,'uint8')
        print(faceNp)

        # Get ID from file path.
        ID = int(imagePaths.split('\\')[1].split('.')[1])
        print(imagePaths,ID)
        faces.append(faceNp)
        IDs.append(ID)

        cv2.imshow('Training',faceNp)
        cv2.waitKey(1)

    return faces,IDs

faces,IDs = getImagesWidthID(path)

# Train data
recognizer.train(faces,np.array(IDs))

# Store training data to file.
if not os.path.exists('recognizer'):
    os.makedirs('recognizer')

recognizer.save('recognizer/trainingData.yml')
cv2.destroyAllWindows()
