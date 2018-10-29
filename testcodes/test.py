import Paths
import globals
from globals import ClassifierFiles
import numpy as np
import cv2
import time
import dlib
import math
import eyeCoordinates
import mouthCoordinates
from globals import Threshold
from globals import yawnFolder
import os
import openface
VIDEO_PATHS = []


readVideo('v.avi')#test video of faces



def readVideo(video):
    global no,yes
    video_capture = cv2.VideoCapture(video)
    detector = dlib.get_frontal_face_detector() #Face detector
    predictor = dlib.shape_predictor(ClassifierFiles.shapePredicter) #Landmark identifier
    face_aligner = openface.AlignDlib(ClassifierFiles.shapePredicter)

    u = 0
    while True:
        ret, frame = video_capture.read()
        if frame != None:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            # clahe_image = clahe.apply(gray)

            detections = detector(frame, 1) #Detect the faces in the image

            for k,d in enumerate(detections): #For each detected face
                shape = predictor(frame, d) #Get coordinates
                vec = np.empty([68, 2], dtype = int)
                coor = []
                for i in range(1,68): #There are 68 landmark points on each face
                    #cv2.circle(frame, (shape.part(i).x, shape.part(i).y), 1, (0,0,255), thickness=1)
                    coor.append([shape.part(i).x, shape.part(i).y])
                    vec[i][0] = shape.part(i).x
                    vec[i][1] = shape.part(i).y

                #RightEye and LeftEye coordinates
                rightEye = eyeCoordinates.distanceRightEye(coor)
                leftEye = eyeCoordinates.distanceLeftEye(coor)
                eyes = (rightEye + leftEye)/2

                #Mouth coordinates
                mouth = mouthCoordinates.distanceBetweenMouth(coor)

                print(eyes,mouth)
                #prints both eyes average distance
                #prints mouth distance
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



if __name__ == '__main__': 
    VIDEO_PATHS = Paths.videosPaths()
    init()
