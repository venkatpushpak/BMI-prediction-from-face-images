import numpy as np
import cv2
import time
import dlib
import math
import imutils
from imutils import face_utils
import pandas as pd

import os, os.path

images = []
data =pd.DataFrame()
def midpoint(p1, p2):
    return ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)


def intersectionpt(p1,p2,p3,p4):


    # line p1 p2
    a1 = p2[1] - p1[1]
    b1 = p1[0] - p2[0]
    c1 = a1*(p1[0]) + b1*(p1[1])


    #line p3 p4

    a2 = p4[1] - p3[1]
    b2 = p3[0] - p4[0]
    c2 = a2*(p3[0])+ b2*(p3[1])


    #determinant

    determinant = a1*b2 - a2*b1

    if (determinant == 0) :

        #The lines are parallel. This is simplified
        # by returning a pair of FLT_MAX
        print('The points are parallel')
        return (0,0)
    else:
        mx = (b2*c1 - b1*c2)/determinant;
        my = (a1*c2 - a2*c1)/determinant;
        return (mx, my);




def testprint(p1):
    print('x:',p1[0],'y:',p1[1])

def ASMfitting(imgin):
    global data
    detector = dlib.get_frontal_face_detector() #Face detector
    predictor = dlib.shape_predictor('../Data/dlibShapepredictor/shape_predictor_68_face_landmarks.dat') #Landmark identifier

    frame = cv2.imread(imgin)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    reqpoints = [0,4,8,12,16,17,18,20,21,22,23,25,26,36,37,38,39,42,43,44,45,66]
    coords = {}
    # data = pd.DataFrame(columns = ('image-name','0','4','8','12','16','17','18','20','21','22','23','25','26','36','37','38','39','42','43','44','45','66' ))


    detection = detector(gray, 1)
    #print("detection",len(detection))
    if len(detection)!=0:
        for d in detection:
            shape  = predictor(gray, d)
            shape1 = face_utils.shape_to_np(shape)
            (x, y, w, h) = face_utils.rect_to_bb(d)
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            for i,(x, y) in enumerate(shape1):
                # data.append({'image-name': str(imgin)},ignore_index=True)
                if(i in reqpoints):
                    strkey = "P"+ str(i)
                    point = (x,y)
                    # cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)
                    # coords.append(point)
                    if strkey in coords:
                        print("point already exist")
                    else :
                        coords[strkey] = point

        N3 = midpoint(coords['P18'],coords['P20'])
        N4 = midpoint(coords['P23'],coords['P25'])
        lefteyemid = midpoint(coords['P37'],coords['P38'])
        righteyemid = midpoint(coords['P43'],coords['P44'])
        N1 = midpoint(lefteyemid,righteyemid)
        coords['Plfteyemid'] = lefteyemid
        coords['Prghteyemid'] = righteyemid
        # print('N1 :', N1)
        coords['N3'] = N3
        coords['N4'] = N4
        coords['N1'] = N1

        N2 = intersectionpt(coords['P36'],coords['N3'],coords['P45'],coords['N4'])
        #print('N2:', N2)
        coords['N2'] = N2

        del coords['P37']
        del coords['P38']
        del coords['P43']
        del coords['P44']

        #print(coords)




        for key, value in coords.items():
            # print(key ,':', value[0] ,':', value[1], '\n' )
            if(str(key[0]) == 'P'):
                cv2.circle(frame, (int(value[0]), int(value[1])), 2, (0, 0, 255), -1)
            else:
                cv2.circle(frame, (int(value[0]), int(value[1])), 2, (0, 255, 0), -1)



        coords['Image-name'] = str(imgin)
        df = pd.DataFrame(coords)
        #data.append(df)
        data=data.append(df,ignore_index=True)
        #print(data)



        # print( 'N3:' , N3)
        # testprint(coords['P18'])
        # print('accessing x'. )
        #cv2.imshow("Output", frame)
        #cv2.imwrite("fittedtst.jpeg",frame)
        # print(data)
        # print(coords)
        cv2.waitKey(0)
    #data.to_csv('data.csv')

            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #         break



def readImages():
        global images
        #imgs = []
        path = "../test-images"
        valid_images = [".jpg",".gif",".png",".tga",".bmp",".jpeg"]
        for f in os.listdir(path):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in valid_images:
                continue
            images.append(os.path.join(path,f))
        #print(images)

readImages()
print(images)

for i in range(0,len(images)):
   ASMfitting(images[i])
#ASMfitting(images[0])
print(data)
data.to_csv('data.csv')
