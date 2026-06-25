# app/routes.py

from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename
import os

from .detector import detect_objects

main = Blueprint("main", __name__)

UPLOAD_FOLDER = "app/static/uploads"
RESULT_FOLDER = "app/static/results"

# Create folders automatically
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)


@main.route("/", methods=["GET", "POST"])
def home():

    result_image = None
    detections = []

    if request.method == "POST":

        file = request.files.get("image")

        if file and file.filename:

            # Ensure folders exist
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            os.makedirs(RESULT_FOLDER, exist_ok=True)

            filename = secure_filename(file.filename)

            filepath = os.path.join(
                UPLOAD_FOLDER,
                filename
            )

            file.save(filepath)

            try:

                result_image, detections = detect_objects(filepath)

                if result_image:
                    result_image = result_image.replace(
                        "app/static/",
                        ""
                    )

            except Exception as e:

                print("Detection Error:", e)

                detections = [{
                    "class": f"ERROR: {str(e)}",
                    "confidence": "-"
                }]

    return render_template(
        "index.html",
        result_image=result_image,
        detections=detections
    )