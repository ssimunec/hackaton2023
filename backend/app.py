import os
from flask import Flask, render_template, request,jsonify
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from detector import PersonDetector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = "./uploads"
app.config['MAX_CONTENT_PATH'] = 999999999999

person_detector = PersonDetector()

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
 

if __name__ == '__main__':
   app.run(debug = True, port=8080)