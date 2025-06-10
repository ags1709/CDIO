import os
from ultralytics import YOLO
import cv2

# === CONFIGURATION ===
model_path = "ImageModels/best.pt"  # Replace with your actual model path
pictures_folder = "pictures"
labels_folder = "labels"
annotations_folder = "annotations"
#max_images = 100

# === PREPARE OUTPUT FOLDERS ===
os.makedirs(labels_folder, exist_ok=True)
os.makedirs(annotations_folder, exist_ok=True)

# === LOAD MODEL ===
model = YOLO(model_path)

# === GET IMAGES ===
image_files = [f for f in os.listdir(pictures_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
#image_files = image_files[:max_images]

# === PROCESS IMAGES ===
for image_name in image_files:
    image_path = os.path.join(pictures_folder, image_name)
    image = cv2.imread(image_path)
    height, width = image.shape[:2]

    results = model(image)[0]

    label_file_path = os.path.join(labels_folder, os.path.splitext(image_name)[0] + ".txt")

    with open(label_file_path, "w") as f:
        for box in results.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Draw box on image
            label = f"{model.names[cls_id]} {conf:.2f}"
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # Convert to YOLO format
            x_center = ((x1 + x2) / 2) / width
            y_center = ((y1 + y2) / 2) / height
            w = (x2 - x1) / width
            h = (y2 - y1) / height

            f.write(f"{cls_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n")

    # Save annotated image
    annotated_path = os.path.join(annotations_folder, image_name)
    cv2.imwrite(annotated_path, image)

print("Detection complete. Labels and annotations saved.")