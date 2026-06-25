from ultralytics import YOLO
from pathlib import Path
import cv2
import os

BASE_DIR = Path(__file__).resolve().parent.parent

RESULT_FOLDER = BASE_DIR / "app" / "static" / "results"

RESULT_FOLDER.mkdir(parents=True, exist_ok=True)

model = YOLO("models/yolov8n.pt")


def detect_objects(image_path):

    results = model.predict(
        source=image_path,
        device="cpu",
        verbose=False
    )

    result = results[0]

    output_path = RESULT_FOLDER / os.path.basename(image_path)

    annotated = result.plot()

    cv2.imwrite(str(output_path), annotated)

    detections = []

    for box in result.boxes:

        cls_id = int(box.cls[0])
        conf = float(box.conf[0])

        detections.append({
            "class": model.names[cls_id],
            "confidence": round(conf, 2)
        })

    return str(output_path), detections