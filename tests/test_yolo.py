from ultralytics import YOLO

# Load pretrained YOLO model
model = YOLO("yolov8n.pt")

# Run inference
results = model.predict(
    source="road.jpg",
    device=0,
    conf=0.25
)

for result in results:
    for box in result.boxes:
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])

        print({
            "object": model.names[class_id],
            "confidence": round(confidence, 2)
        })