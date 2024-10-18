# flask --app app.py run --debug
import flask
from flask import Flask, request, render_template
import time
import requests

from . import blob_manager

app = Flask(__name__)
with app.app_context():
    blob_manager.setup()


@app.route("/")
def home():
    """ upload page for images """
    return render_template("upload.html")


@app.route("/", methods=['POST'])
def upload_files_example_post():
    """ stores the uploaded image(s) in blob storage"""
    for file in request.files.getlist("photos"):
        blob_manager.upload_blob(file)

    return flask.redirect(flask.url_for("uploads_view"))


@app.route("/uploads_view")
def uploads_view():
    """ Fetch all blob URLS and display all uploaded files"""
    blobs = blob_manager.list_blobs()

    return render_template("uploads_view.html", blobs=blobs)


STORAGE_ACCOUNTS = {
    'US Central': 'https://idontknowwhy1.blob.core.windows.net/centralus/pexels-pixabay-326055.jpg',
    'US East': 'https://idontknowwhy3.blob.core.windows.net/eastus/pexels-pixabay-326055.jpg',
    'Asia India': 'https://idontknowwhy2.blob.core.windows.net/centralindia/pexels-pixabay-326055.jpg',
}

def measure_latency(url):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()

    # Measure the time it took to download the image
    latency = end_time - start_time
    return latency

@app.route("/latency")
def latency():
    latencies = {}

    for location, url in STORAGE_ACCOUNTS.items():
        lat = measure_latency(url)
        latencies[location] = round(lat, 3)  # Measure in seconds

    return render_template('latency.html', latencies=latencies, storage_accounts=STORAGE_ACCOUNTS)


