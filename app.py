# flask --app app.py run --debug

from . import blob_manager
from flask import Flask, session, request, render_template

app = Flask(__name__)
with app.app_context():
    blob_manager.setup()

@app.route("/")
def home():
    return render_template("upload.html")

@app.route("/", methods=['POST'])
def upload_files_example_post():
    files = ""
    for file in request.files.getlist("photos"):
        blob_url = blob_manager.upload_blob(file)
        if blob_url is None:
            continue
        else:
            files += "<h1>{}</h1><img src={} alt=imagetext /><br/>".format(file.filename, blob_url)
    return "<p>Uploaded: <br />{}</p>".format(files)
