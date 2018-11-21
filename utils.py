import io
import os
import sys
import pickle
import urllib3 as urllib
import numpy as np
import tensorflow as tf
from PIL import Image

dir_path = os.path.dirname(os.path.realpath(__file__)) # full path to this file
sys.path.append('{}/VGGFace/'.format(dir_path))
from vgg_face import VGGFace

svr_path = 'svr_parameters'
weight_path = 'VGGFace/vgg_face.npy'

def read_image(url):

  http = urllib.PoolManager()

  # url = 'http://www.thefamouspeople.com/singers.php'
  
  try:
    return Image.open(url)
  except IOError:
    fd =  http.request('GET', url)
    image_file = io.BytesIO(fd.read())
    return Image.open(image_file)



def get_data(path):
  img = read_image(path).convert('L')
  max_edge = max(img.size[0], img.size[1])
  black = Image.new('L',(max_edge, max_edge),0)

  black.paste(img, [int(max_edge/2 - img.size[0]/2),
                    int(max_edge/2 - img.size[1]/2),
                    int(max_edge/2 + (img.size[0]+1)/2),
                    int(max_edge/2 + (img.size[1]+1)/2)] )
  img = black.resize((224,224))
  img = np.array(img).astype(np.float32)
  img -= np.mean(img)
  img /= np.std(img)
  img = img.reshape((224,224,1))
  img = np.concatenate([img,img,img],axis = 2)
  return img.reshape((1,224,224,3))

class BMIPredictor(object):

  def __init__(self):
    self.image_ = tf.placeholder(tf.float32, shape = [1,224,224,3])
    print ('Initializing the TensorFlow graph...')
    self.net = VGGFace({'data' : self.image_})
    self.sess = tf.Session()
    print ('Restoring the weights...')
    self.net.load(weight_path,self.sess)
    with open(svr_path, 'rb') as f:
      # u = pickle._Unpickler(f)
      # u.encoding = 'latin1'
      # self.clf = u.load()
      self.clf = pickle.load(f,encoding='latin1')
    print ('Done...')

  def predict(self, path):
    image = get_data(path)
    embedding = self.sess.run(self.net.layers['fc6'], feed_dict = {self.image_: image})
    prediction = self.clf.predict(embedding)
    return prediction[0]
