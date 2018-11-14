from flask import Flask, flash, redirect, render_template, request, session, abort,Response
 
app = Flask(__name__, template_folder='./templates')



import cv2
import numpy as np
import time
from datetime import datetime
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
from pose import Pose, Part, PoseSequence
from evaluate import evaluate_pose
globcap = cv2.VideoCapture(0)
globcap.set(cv2.CAP_PROP_FPS, 2)
   
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



def video_recorder(exercise,event=0):
  
# Create a VideoCapture object
  global globexercise
  globexercise=exercise
  record_strttime = time.time()
  count =0 


  vid_path = '../Data/inputs/'+str(exercise)+'/'+str(exercise)+str(vid_rec_time)+'.avi'
  full_vid_path = '../Data/fullvideos/'+str(exercise)+'/'+str(exercise)+str(vid_rec_time)+'.avi'
  print(vid_path)
  out = cv2.VideoWriter(vid_path,cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
  fullout = cv2.VideoWriter(full_vid_path,cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
  # yield vid_path
  while(True):
    
    ret, frame = globcap.read()
   
    if ret == True:
      count =count+1 
       
      # Write the frame into the file 'output.avi'
      if(time.time()> record_strttime+10 and time.time() < record_strttime + 25):
        fullout.write(frame)
        out.write(frame)
        if(count%5 == 0):
          cv2.putText(frame, "recording", (10, 20),  cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
        global frame_cnt
        frame_cnt = frame_cnt+1
        
        # print('count',count)

      # Display the resulting frame    
      # cv2.imshow('frame',frame)

    cv2.imwrite('face.jpg', frame)
    cv2.waitKey(1)==27
    # frame_cnt=count
    yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('face.jpg', 'rb').read() + b'\r\n')
  out.release()
  # globcap.release()
  # print('count :',count)
  



def eval_feedback(exercise):
  # import cv2
  video_in = '../Data/inputs/'+str(exercise)+'/'+str(exercise)+str(vid_rec_time)+'.avi'
  print('video in:',str(video_in))
  w, h = model_wh('432x368')
  model='mobilenet_thin'
  resize_out_ratio=4.0
  e = TfPoseEstimator(get_graph_path(model), target_size=(w, h))
  pose_path = '../Data/outputs/'+str(exercise)+'/'+str(exercise)+str(vid_rec_time)+'.avi'
  poseout = cv2.VideoWriter(pose_path,cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
  cap = cv2.VideoCapture(video_in)

  num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  print('num_frames',num_frames, frame_cnt)
  all_keypoints = np.zeros((frame_cnt,18,3))

  if cap.isOpened() is False:
    print("Error opening video stream or file")
  while cap.isOpened():
    print("cap opened")
    ret_val, image = cap.read()
    print(ret_val)
    if(ret_val==True):
        # humans = e.inference(image)
        humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=resize_out_ratio)
        # if not args.showBG:
        #     image = np.zeros(image.shape)
        image,npkeypoints = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
        for i in range(frame_cnt):
          all_keypoints[i]=npkeypoints.reshape(18,3)

        poseout.write(image)
    elif(ret_val == False):
      cap.release()
  

  print(all_keypoints[0])
  npfilename = '../Data/numpys/'+str(exercise)+'/'+str(exercise)+vid_rec_time+'.npy'
  # nptest_file = np.load('bicepcurl.npy')
  np.save(npfilename,all_keypoints)
  pose_seq= PoseSequence(all_keypoints)
  (correct, feedback) = evaluate_pose(pose_seq, exercise)
  if correct:
    evaluation = 'Exercise performed correctly:'
    print(evaluation)
  else:
    evaluation = 'Exercise could be improved:'
    print(evaluation)
  print(feedback)
  cap.release()
  poseout.release()
  return correct,feedback,evaluation
  # return 0



def pose_vid_Read():
  posevid_path = '../Data/outputs/'+str(globexercise)+'/'+str(globexercise)+str(vid_rec_time)+'.avi'
  cap=cv2.VideoCapture(posevid_path)
  while cap.isOpened():
    # print("cap opened")
    ret_val, frame = cap.read()
    # print(ret_val)
    if(ret_val==True):
      cv2.imwrite('pose.jpg', frame)
      delay(time.time())
 
      yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('pose.jpg', 'rb').read() + b'\r\n')
     
    elif(ret_val==False):
      cap=cv2.VideoCapture(posevid_path)

def delay(timeinp):
  # print('difference',int(time.time())-timeinp) 
  while (True):
    difference = time.time()-timeinp
    if(difference > 0.1 ):
      break
  return 0
    

  
@app.route("/",methods=['GET', 'POST'])
@app.route("/home",methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route("/bicepcurl", methods=['GET','POST'])
def bicepcurlrecord():
	return render_template('bicepcurl.html')

@app.route("/frontraise", methods=['GET','POST'])
def frontraise():
	return render_template('frontraise.html')


@app.route("/shouldershrug", methods=['GET','POST'])
def shouldershrug():
	return render_template('shoulder.html')


@app.route("/shoulderpress", methods=['GET','POST'])
def shoulderpress():
	return render_template('shoulderpress.html')




@app.route("/feedback/<exercise>", methods=['GET','POST'])
def feedback(exercise):
  globcap.release()
  correct,feedback,evaluation = eval_feedback(exercise)
  ht_exer = 'Exercise'
  if(exercise == 'bicep_curl'):
    ht_exer = 'Bicep Curl'
  elif(exercise == 'shoulder_shrug'):
    ht_exer = 'Shoulder Shrug'
  elif(exercise == 'shoulder_press'):
    ht_exer = 'Shoulder Press'
  elif(exercise == 'front_raises'):
    ht_exer = 'Front Raises'
  # eval_feedback(exercise)
  # return render_template('feedback.html')
  return render_template('feedback.html', eval=evaluation, feedback=feedback, exercise=ht_exer)


@app.route('/video_rec/<exercise>')
def video_rec(exercise):
	return Response(video_recorder(exercise),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/pose_vid')
def pose_vid():
  return Response(pose_vid_Read(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run()


 # # @app.route('/questions/<int:question_id>'): 
	 # def find_question(question_id):  
	 #    return ('you asked for question{0}'.format(question_id))