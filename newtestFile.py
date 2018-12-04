
import numpy as np
import cv2
import time
import dlib
import math
import imutils
from imutils import face_utils
import os
import pandas as pd
from shapely.geometry import Polygon
import time


import os, os.path


## GLobal Variables
images = []
data =pd.DataFrame()

def readImages():
        global images
        #imgs = []
        path = "./Release/Data/Images"
        valid_images = [".jpg",".gif",".png",".tga",".bmp",".jpeg"]
        for f in os.listdir(path):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in valid_images:
                continue
            images.append(os.path.join(path,f))
        #print(images)

def midpoint(p1, p2):
    return ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)


def distance(p1,p2):
    return math.sqrt( (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 )

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
        return (mx, my)


def polygonArea(corners):
    n = len(corners) # of corners
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0
    return area


def polygonPerimeter(corners):
    n = len(corners)
    # print('n = ', n)
    perimeter = 0
    for i in range(n):
        # print ('i =', i)
        if(i<n-1):
            perimeter += distance(corners[i],corners[i+1])
        elif (i==n-1):
            perimeter += distance(corners[i], corners[0])

    return abs(perimeter)


# examples
corners = [(2.0, 1.0), (4.0, 5.0), (7.0, 8.0)]




def testprint(p1):
    print('x:',p1[0],'y:',p1[1])

def ASMfitting(imgin):
    global data
    detector = dlib.get_frontal_face_detector() #Face detector
    predictor = dlib.shape_predictor('./Data/dlibShapepredictor/shape_predictor_68_face_landmarks.dat') #Landmark identifier

    frame = cv2.imread(imgin)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    reqpoints = [0,4,8,12,16,17,18,20,21,22,23,25,26,36,37,38,39,42,43,44,45,66]
    coords = {}
    final_features = {}


    detection = detector(gray, 1)

    if len(detection)!=0:


        for d in detection:
            shape  = predictor(gray, d)
            shape1 = face_utils.shape_to_np(shape)
            (x, y, w, h) = face_utils.rect_to_bb(d)
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            for i,(x, y) in enumerate(shape1):
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
        # print('N2:', N2)
        coords['N2'] = N2

        ## deelting eye coordinates

        del coords['P37']
        del coords['P38']
        del coords['P43']
        del coords['P44']

        # print(coords)

        ### printing circles on image for testing


        # for key, value in coords.items():
        #     # print(key ,':', value[0] ,':', value[1], '\n' )
        #     if(str(key[0]) == 'P'):
        #         cv2.circle(frame, (int(value[0]), int(value[1])), 2, (0, 0, 255), -1)
        #     else:
        #         cv2.circle(frame, (int(value[0]), int(value[1])), 2, (0, 255, 0), -1)



        coords['Image-name'] = os.path.basename(imgin)

        ## Calculating necessary features

        cheekbone_width = distance(coords['P0'],coords['P16'])
        jaw_width = distance(coords['P4'],coords['P12'])
        upper_facialheight = distance(coords['P66'],coords['N1'])
        polygon_corners = [coords['P0'],coords['P4'],coords['P8'],coords['P12'],coords['P16']]
        polygon_perimeter = polygonPerimeter(polygon_corners)
        polygon_area = polygonArea(polygon_corners)
        # print('polygon_area:', polygon_area)
        # print('polygon_perimeter:', polygon_perimeter)
        avg_eyesize = ((distance(coords['P36'],coords['P45'])) - (distance(coords['P39'],coords['P42'])))/2
        nw_point = (coords['P0'][0], coords['P8'][1])
        LFH =  distance(coords['P0'],nw_point)
        face_height = distance(coords['P8'],coords['N2'])
        # face_width = cheekbone_width

        # print('cheekbone_width:', cheekbone_width)

        MEH = (distance(coords['P36'], coords['P17'])+ distance(coords['N3'], coords['Plfteyemid']) + distance(coords['P21'], coords['P39']) +
            distance(coords['P22'], coords['P42']) + distance(coords['N4'], coords['Prghteyemid']) + distance(coords['P26'], coords['P45'])) / 6

        # print('MEH:', MEH)

        ## calculating final features

        CJWR =  cheekbone_width / jaw_width
        WHR = cheekbone_width / upper_facialheight
        PAR = polygon_perimeter / polygon_area
        ES = avg_eyesize
        LF_FH = LFH / face_height
        FW_LFH = cheekbone_width / LFH



        final_features['Image-name'] = [os.path.basename(imgin)]
        final_features['CJWR'] = [CJWR]
        final_features['WHR'] = [WHR]
        final_features['PAR'] = [PAR]
        final_features['ES'] = [ES]
        final_features['LF_FH'] = [LF_FH]
        final_features['FW_LFH'] = [FW_LFH]
        final_features['MEH'] = [MEH]


        print(final_features)


        df = pd.DataFrame(final_features)
        data=data.append(df,ignore_index=True)
        # print(data)


        # print(distance([0,0], [0,8]))
        # print(distance([0,8], [0,0]))



        # print( 'N3:' , N3)
        # testprint(coords['P18'])
        # print('accessing x'. )
        # cv2.imshow("Output", frame)
        # cv2.imwrite("fittedtst.jpeg",frame)
        #
        # print(coords)
        # cv2.waitKey(0)
        # data.to_csv('data.csv')
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #         break

    else:
        print("No face detected in ", str(imgin))

        final_features['Image-name'] = [os.path.basename(imgin)]
        final_features['CJWR'] = float('nan')
        final_features['WHR'] = float('nan')
        final_features['PAR'] = float('nan')
        final_features['ES'] = float('nan')
        final_features['LF_FH'] = float('nan')
        final_features['FW_LFH'] = float('nan')
        final_features['MEH'] = float('nan')

        print(final_features)

        df = pd.DataFrame(final_features)
        data=data.append(df,ignore_index=True)







# ASMfitting('../test-images/testimg.jpeg')
# ASMfitting('./test-images/tstimg1.jpeg')


starttime = time.time()

readImages()
print(images)

for i in range(0,len(images)):
   ASMfitting(images[i])
#ASMfitting(images[0])
print(data.head(10))
data.to_csv('./Data/features.csv')

endtime = time.time()

print("time taken to extract :", endtime - starttime)
