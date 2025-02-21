from flask import Flask, request, render_template, redirect, url_for, session
from PIL import Image
import os
import tweepy

app = Flask(__name__)
app.secret_key = "your_secret_key"
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Twitter API keys (replace with your own)
CONSUMER_KEY = "your_consumer_key"
CONSUMER_SECRET = "your_consumer_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_TOKEN_SECRET = "your_access_token_secret"

# Authenticate with X API
auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Predefined sizes
IMAGE_SIZES = [(300, 250), (728, 90), (160, 600), (300, 600)]

def resize_image(image_path):
    images = []
    original = Image.open(image_path)
    for size in IMAGE_SIZES:
        resized = original.resize(size)
        new_path = f"{UPLOAD_FOLDER}/{size[0]}x{size[1]}.jpg"
        resized.save(new_path)
        images.append(new_path)
    return images

def post_to_x(image_paths):
    for img_path in image_paths:
        api.update_status_with_media(status="Resized Image", filename=img_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded", 400
        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        resized_images = resize_image(file_path)
        post_to_x(resized_images)
        return "Images resized and posted successfully!"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
