# app/routes.py

from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename
import os

from .detector import detect_objects

main = Blueprint("main", __name__)

UPLOAD_FOLDER = "app/static/uploads"


@main.route("/", methods=["GET", "POST"])
def home():

    result_image = None
    detections = []

    if request.method == "POST":

        file = request.files["image"]

        if file:

            filename = secure_filename(file.filename)

            filepath = os.path.join(
                UPLOAD_FOLDER,
                filename
            )

            file.save(filepath)

            result_image, detections = detect_objects(filepath)

            result_image = result_image.replace(
                "app/static/",
                ""
            )

    return render_template(
        "index.html",
        result_image=result_image,
        detections=detections
    )