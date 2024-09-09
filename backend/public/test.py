import json , time
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import requests
import shutil
import numpy as np
import cv2
import glob
import random
from ultralytics import YOLO
import cv2
from postprocessing import *
import collections,numpy
import tensorflow as tf

model = YOLO("best.pt")
class_list = model.model.names
scale_show = 100

app = Flask(__name__)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response
@app.route('/main', methods=['POST'])
def main():

  request_data = request.get_json()

  image_url = str("upload/"+request_data['url'])
  image_center_points = request_data['center_points']

  print(image_center_points)
  print(request_data['url'])

  frame = cv2.imread(image_url)

  results = model.predict(frame)
  tem_array=numpy.array(results[0].boxes.cls.numpy().astype(int))
  counter = collections.Counter(tem_array)

  labeled_img , center_points = draw_box_people(frame, results[0], class_list,image_center_points)
  display_img = resize_image(labeled_img, scale_show)

  cv2.imwrite('output/'+request_data['url'],display_img)

  percentage_value=0

  for x in results[0].boxes.xywh:
    percentage_value=percentage_value+(x[2]*x[3])/(results[0].orig_shape[0]*results[0].orig_shape[1])*100

  print(percentage_value)
  print(float(percentage_value))
  percentage_value=float(percentage_value)

  json_dump = json.dumps({"percentage_value":str(percentage_value),"center_points":center_points,"success":"true"})

  return json_dump


@app.route('/object', methods=['POST'])
def object():

  request_data = request.get_json()

  image_url = str("upload/"+request_data['url'])
  image_object_points = request_data['object_points']

  print(image_object_points)
  print(request_data['url'])

  frame = cv2.imread(image_url)

  results = model.predict(frame)
  tem_array=numpy.array(results[0].boxes.cls.numpy().astype(int))
  counter = collections.Counter(tem_array)

  labeled_img , object_points = draw_box_object(frame, results[0], class_list,image_object_points)
  display_img = resize_image(labeled_img, scale_show)

  cv2.imwrite('output/'+request_data['url'],display_img)

  percentage_value=0

  for x in results[0].boxes.xywh:
    percentage_value=percentage_value+(x[2]*x[3])/(results[0].orig_shape[0]*results[0].orig_shape[1])*100

  print(percentage_value)
  print(float(percentage_value))
  percentage_value=float(percentage_value)

  json_dump = json.dumps({"percentage_value":str(percentage_value),"object_points":object_points,"success":"true"})

  return json_dump
        

if __name__ == '__main__':
	app.run(host="127.0.0.1", port=8888)