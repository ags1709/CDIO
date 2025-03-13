from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(data="custom_data.yaml", epochs=50, imgsz=400)