# import libraries
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from picamera2 import Picamera2
from time import sleep
import matplotlib
import matplotlib.pyplot as plt
import os
import numpy as np
from openvino.runtime import Core
import cv2


# define the Pi Camera, add matplotlib, define the core and the count
matplotlib.use('GTK3Agg')
ie = Core()
picam2 = Picamera2()
config = picam2.create_preview_configuration()
picam2.configure(config)
count = 0

# define the app
app = Flask(__name__)

# define the upload folder for our images
upload_folder = 'static/images'
app.config['UPLOAD'] = upload_folder
flask_image = "flask_{count}.jpg"
image_path = os.path.join(upload_folder, flask_image)

# define the function to capture images
def capture():
    global count
    count += 1
    picam2.start()
    sleep(3)
    picam2.capture_file(image_path)
    picam2.stop()

# define the function to upload images from our directory and then render the image to our page
@app.route("/", methods = ['GET', 'POST'])
def upload_file():
    if request.method == "POST":
        file = request.files['img']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD'], filename))
        img = os.path.join(app.config['UPLOAD'], filename)
        return render_template('index.html', img=img)
    return render_template('index.html')

# Define the function that will capture our images and upload to our directory
@app.route("/capture", methods=["POST"])
def take_picture():
    capture()
    return render_template('index.html')

# Classify the image based on the image provided
@app.route("/classify")
def classify():
    latest_image = image_path
    model = ie.read_model(model="model/v3-small_224_1.0_float.xml")
    compiled_model = ie.compile_model(model=model, device_name="MYRIAD")
    output_layer = compiled_model.output(0)
    image = cv2.cvtColor(cv2.imread(latest_image), code=cv2.COLOR_BGR2RGB)
    input_image = cv2.resize(src=image, dsize=(224,224))
    input_image = np.expand_dims(input_image, 0)
    result_infer = compiled_model([input_image])[output_layer]
    result_index = np.argmax(result_infer)
    imagenet_classes = open("model/imagenet_2012.txt").read().splitlines()
    imagenet_classes = ['background'] + imagenet_classes
    text = str(imagenet_classes[result_index])
    return text
    

# Run the app 
if __name__ == "__main__":
    app.run(host="0.0.0.0")
