
from ultralytics import YOLO

# Load the model once when the application starts
model = YOLO("yolov8n.pt")


def detect_objects(image_path: str):
    results = model.predict(
        source=image_path,
        device=0,
        conf=0.25,
        verbose=False
    )

    detections = []

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            detections.append({
                "object": model.names[class_id],
                "confidence": round(confidence, 3)
            })

    return detections
