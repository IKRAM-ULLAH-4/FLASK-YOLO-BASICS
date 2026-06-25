from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename
from pathlib import Path

from .detector import detect_objects

main = Blueprint("main", __name__)

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_FOLDER = BASE_DIR / "app" / "static" / "uploads"
RESULT_FOLDER = BASE_DIR / "app" / "static" / "results"

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
RESULT_FOLDER.mkdir(parents=True, exist_ok=True)


@main.route("/", methods=["GET", "POST"])
def home():

    result_image = None
    detections = []

    if request.method == "POST":

        file = request.files.get("image")

        if file and file.filename:

            filename = secure_filename(file.filename)

            filepath = UPLOAD_FOLDER / filename

            file.save(str(filepath))

            try:

                result_image, detections = detect_objects(str(filepath))

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