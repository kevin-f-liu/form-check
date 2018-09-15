
from flask import Flask, render_template, request, redirect
from werkzeug import secure_filename
from flask_bootstrap import Bootstrap
import hashlib
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
     if video:
        video_hash = str(int(hashlib.sha1(str(video).encode()).hexdigest(), 16) % (10 ** 8))
        f.save(secure_filename(video))
        select_value = request.form.get('select_value')

        vidcap = cv2.VideoCapture(video)

        success,image = vidcap.read()
        count = 0
        while success:  
            success,image = vidcap.read()
            if count % 25 == 0:
                cv2.imwrite("./static/" + video_hash + "frame%d.jpg" % int(count / 25), image)

            count += 1
        return render_template('upload.html', video=video_hash, select_value=select_value, count=count)
  return render_template('index.html', error="Please Submit A File!")