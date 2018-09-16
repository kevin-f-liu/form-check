
from flask import Flask, render_template, request, redirect, make_response
from werkzeug import secure_filename
from flask_bootstrap import Bootstrap
import hashlib
import cv2
import pdfkit
import os
from flask_mail import Mail, Message

# from flask_mail import Mail, Message

import weaknesses

app = Flask(__name__)
mail = Mail(app)

@app.route('/', methods = ['GET', 'POST'])
def upload_file():
   if request.method == "POST":
       return redirect("/uploader")
   return render_template('index.html')

# get tips from data base
def tips_for_exercises(somestring):
    somestring = somestring.lower()
    if "weak" in somestring: 
        tips = []
        new_string = somestring[somestring.find("weak"):]
        if len(new_string) > 0:
            for exercise in weaknesses.weaknesses.keys():
                for bodypart in weaknesses.weaknesses[exercise].keys():
                    if new_string.find(bodypart) > 0:
                        tips.append({bodypart: weaknesses.weaknesses[exercise][bodypart]})
    return tips

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

        vidcap.set(3, 1280)
        vidcap.set(4, 720)

        print(os.path.getsize(vidcap))
        
        success,image = vidcap.read()
        count = 0

        while success:  
            success,image = vidcap.read()
            if count % 25 == 0:
                cv2.imwrite("./static/" + video_hash + "frame%d.jpg" % int(count / 25), image)

            count += 1
        
        tips = tips_for_exercises("After looking at the video of your workout, it seems that you are weak in you quads and hips")

        return render_template('upload.html', video=video_hash, select_value=select_value, count=count, tips=tips)

  return render_template('index.html', error="Please Submit A File!")

@app.route("/uploader/contact/<video_hash>/<select_value>/<count>/<tips>", methods = ['GET', 'POST'])
# @login_required
def contact(video_hash, select_value, count, tips):
    if request.method == 'POST':
        rendered = render_template('upload.html', video=video_hash, select_value=select_value, count=count, tips=tips)
        pdf = pdfkit.from_string(rendered, False)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'

        # rec = request.form('rec')

        msg = Message("Hello",
                    sender="from@example.com",
                    recipients=["to@example.com"])
        with app.open_resource(response) as fp:
            msg.attach(response, "application/pdf", fp.read())

        mail.send(msg)

        return redirect('/')
    return render_template("contacts.html")