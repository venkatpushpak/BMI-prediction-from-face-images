
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
globcap = cv2.VideoCapture(0)
globcap.set(cv2.CAP_PROP_FPS, 2)
photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'images'
configure_uploads(app, photos)
#from SimpleCV import Image, Camera
  # Check if camera opened successfully
if (globcap.isOpened() == False):
	print("Unable to read camera feed")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(globcap.get(3))
frame_height = int(globcap.get(4))
vid_rec_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
frame_cnt= 0
# vid_rec_time=vid_rec_time[:-8]
globexercise='bicepcurl'
if os.path.exists('images/' + "face.jpg") is True:
	os.remove('images/' + "face.jpg")

def video_recorder(event=0):

	# Create a VideoCapture object
	#out = cv2.VideoWriter(vid_path,cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
	#global active
#	print("this is webapp")
	#out=cv2.VideoWriter(vid_path,cv2.VideoWriter_fourcc('M','J','P','G'),10,(frame_width,frame_height))
	#out = cv2.VideoWriter(vid_path,cv2.VideoWriter_fourcc('M','J','P','G'),10, (frame_width,frame_height))
	#globexercise=exercise
	record_strttime = time.time()
	count =0


	while(True):
		ret, frame = globcap.read()
		try:
			if keyboard.is_pressed('q'):
					print("you pressed a key")
					break
			else:
				pass
		except:
			break

		cv2.imwrite('images/face.jpg', frame)
		cv2.waitKey(1)==27
		# frame_cnt=count
		yield (b'--frame\r\n'
				   b'Content-Type: image/jpeg\r\n\r\n' + open('images/face.jpg', 'rb').read() + b'\r\n')
	 #out.release()




@app.route("/",methods=['GET', 'POST'])
@app.route("/home",methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route("/captureimage", methods=['GET','POST'])
def bicepcurlrecord():
	return render_template('captureimage.html')




@app.route("/showBMI", methods=['GET','POST'])
def capture_image():
          globcap.release()
          #print("in feedback")
          #Response(video_recorder(exercise,1),mimetype='multipart/x-mixed-replace; boundary=frame')
          return render_template('showBMI.html')

@app.route('/upload', methods=['POST','GET'])
def upload_file():
	if request.method == 'POST' and 'photo' in request.files:
		filename=photos.save(request.files['photo'])
		imagename="/images/"+request.files['photo'].filename
        #print(imagename)
		#print("photo",request.files['photo'].filename)
	return 	render_template('showBMI.html',result=imagename)




@app.route('/video_rec')
def video_rec():
    #os.remove('images/' + "face.jpg")
	return Response(video_recorder(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run()


 # # @app.route('/questions/<int:question_id>'):
	 # def find_question(question_id):
	 #    return ('you asked for question{0}'.format(question_id))
