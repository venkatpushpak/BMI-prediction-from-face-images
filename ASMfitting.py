
import numpy as np
import cv2
import time
import dlib
import math
import imutils
from imutils import face_utils
import os




def ASMfitting(imgin):
    
    detector = dlib.get_frontal_face_detector() #Face detector
    predictor = dlib.shape_predictor('./Data/dlibShapepredictor/shape_predictor_68_face_landmarks.dat') #Landmark identifier
    
    frame = cv2.imread(imgin)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    
    detection = detector(gray, 1)
    for d in detection:
        shape  = predictor(gray, d)
        shape1 = face_utils.shape_to_np(shape)
        (x, y, w, h) = face_utils.rect_to_bb(d)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        for (x, y) in shape1:
            cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)
    cv2.imshow("Output", frame)
    cv2.waitKey(0)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break



ASMfitting('./test-images/testimg.jpeg')
# ASMfitting('./test-images/tstimg1.jpeg')
