
from flask import Flask, flash, redirect, render_template, request, session, abort,Response
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__, template_folder='./templates')
import cv2
import keyboard
import numpy as np

import time
import os
from datetime import datetime
import pygame
import pygame.camera
import dlib
import math
import imutils
from imutils import face_utils
import ASMfitting as ASM 	
from Code.utils import BMIPredictor

globcap = cv2.VideoCapture(0)
# globcap.set(cv2.CAP_PROP_FPS, 2)
photos = UploadSet('photos', IMAGES)
haar_face_cascade = cv2.CascadeClassifier('./Data/haarcascade_frontalface_default.xml')

app.config['UPLOADED_PHOTOS_DEST'] = 'images'
configure_uploads(app, photos)
#from SimpleCV import Image, Camera
  # Check if camera opened successfully
if (globcap.isOpened() == False):
	print("Unable to read camera feed")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
# frame_width = int(globcap.get(3))
# frame_height = int(globcap.get(4))
# vid_rec_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
# frame_cnt= 0
# vid_rec_time=vid_rec_time[:-8]
globexercise='bicepcurl'
if os.path.exists('images/' + "face.jpg") is True:
	os.remove('images/' + "face.jpg")

def livedisplay(event=0):

	

	while True:

	        ret, im =globcap.read()

	        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

	        faces = haar_face_cascade.detectMultiScale(gray, scaleFactor=1.2);
	        for(x,y,w,h) in faces:
	            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
	            # print(gray[y:y+h,x:x+w].shape)
	           
	        cv2.imwrite('./test-images/face.jpg', im)
	        yield (b'--frame\r\n'
	                   b'Content-Type: image/jpeg\r\n\r\n' + open('./test-images/face.jpg', 'rb').read() + b'\r\n')


def facecapture():
	captime = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
	filenm = 'testimg'+str(captime)+'.jpg'
	filepath = './Data/'+ filenm 
	dispfile = "./static/"+filenm 
	ret, im = globcap.read()
	gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	features, coords = ASM.ASMfitting(im, gray , dispfile, filepath)
	print(features)

	bmi_predictor = BMIPredictor()
	VGGbmi = bmi_predictor.predict(filepath)
	print(VGGbmi)

	

	# cv2.imwrite(filepath, im)

	# cv2.imwrite(dispfile, im)
	cv2.destroyAllWindows()
	globcap.release()
	return filepath, filenm,dispfile




@app.route("/",methods=['GET', 'POST'])
@app.route("/home",methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route("/captureimage", methods=['GET','POST'])
def captureimage():
	return render_template('captureimage.html')




@app.route("/showBMI", methods=['GET','POST'])
def showBMI():
	filepath, filename,dispfile = facecapture()
	print (filepath)
	return render_template('showBMI.html', imgfilenm = filename, result = dispfile)

@app.route('/upload', methods=['POST','GET'])
def upload_file():
	if request.method == 'POST' and 'photo' in request.files:
		filename=photos.save(request.files['photo'])
		imagename="/images/"+request.files['photo'].filename
        #print(imagename)
		#print("photo",request.files['photo'].filename)
	return 	render_template('showBMI.html',result=imagename)



# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         ret, im =cam.read()
#         cv2.imwrite('./static/emotion.jpg', im)
#         cv2.destroyAllWindows()
#         return render_template('emotionRecog.html')
#     else:
#         return render_template('new.html')


@app.route('/video_rec')
def video_rec():
    #os.remove('images/' + "face.jpg")
	return Response(livedisplay(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run()


 # # @app.route('/questions/<int:question_id>'):
	 # def find_question(question_id):
	 #    return ('you asked for question{0}'.format(question_id))
