from flask import Flask, render_template, request, redirect
from werkzeug import secure_filename
import cv2

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def upload_file():
   if request.method == "POST":
       return redirect("/uploader")
   return render_template('index.html')
    
@app.route('/uploader', methods = ['GET', 'POST'])
def uploaded_file():
  if request.method == 'POST':
     f = request.files['file']
     video = f.filename
     f.save(secure_filename(video))
     select_value = request.form.get('select_value')

     vidcap = cv2.VideoCapture(video)
    #  vidcap.set(cv2.CV_CAP_PROP_FPS, 1)
     success,image = vidcap.read()
     count = 0
     while success:
         cv2.imwrite("./templates/frames/frame%d.jpg" % count, image)     # save frame as JPEG file     
         success,image = vidcap.read()
         print('Read a new frame: ', success)
         count += 1
  return render_template('upload.html', select_value=select_value, count=count)