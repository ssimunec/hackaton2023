import os
from flask import Flask, render_template, request,jsonify
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from detector import PersonDetector
from flask_cors import CORS

from faceanalytics import FaceAnalytics
from utils import crop_image, save_image

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = "./uploads"
app.config['MAX_CONTENT_PATH'] = 999999999999

person_detector = PersonDetector()

@app.route('/')
def root_route():
   return jsonify({"status": True})

@app.route('/upload')
def upload():
   return render_template('./upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join('./uploads', secure_filename(f.filename)))
      return 'file uploaded successfully'


@app.route('/detect', methods = ['POST'])
def detect():
   json_request = request.json
   image_file_name = json_request["image"]

   source_image_path = os.path.join('./uploads', image_file_name)

   inference_result = person_detector.run(source_image_path)

   if(len(inference_result)):
      response = {
         "type": inference_result[0][0],
         "position": inference_result[0][1],
         "status": True
      }
   else:
      response = {
         "type": None,
         "position": None,
         "status": False
      } 

   return jsonify(response)

@app.route('/faceanalytics', methods = ['POST'])
def faceanalytics():
   json_request = request.json
   position = json_request["position"]

   image_file_name = json_request["image"]

   source_image_path = os.path.join('./uploads', image_file_name)

   cropped_image = crop_image(position, source_image_path)

   cropped_image_path = os.path.join('./uploads_process', image_file_name)

   save_image(cropped_image, cropped_image_path)

   inference_result = FaceAnalytics().run(source_image_path)

   if(len(inference_result)):
      response = {
         "type": "person",
         "age": inference_result[0][0],
         "gender": inference_result[0][1],
         "sentiment": inference_result[0][2],
         "status": True
      }
   else:
      response = {
         "type": None,
         "age": None,
         "gender": None,
         "sentiment": None,
         "status": False
      } 

   return jsonify(response)
 

if __name__ == '__main__':
   app.run(debug = True, port=8080,host="0.0.0.0")