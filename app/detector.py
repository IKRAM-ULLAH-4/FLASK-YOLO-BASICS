from ultralytics import YOLO
import cv2
import os

model = YOLO("models/yolov8n.pt")

def detect_objects(image_path):

    results = model.predict(
        source=image_path,
        device="cpu",
        verbose=False
    )

    result = results[0]

    output_path = os.path.join(
        "app/static/results",
        os.path.basename(image_path)
    )

    annotated = result.plot()

    cv2.imwrite(output_path, annotated)

    detections = []

    for box in result.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])

        detections.append({
            "class": model.names[cls_id],
            "confidence": round(conf, 2)
        })

    return output_path, detections