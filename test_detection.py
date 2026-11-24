from services.object_detection import detect_objects

results = detect_objects("bus.jpg")

for item in results:
    print(item)