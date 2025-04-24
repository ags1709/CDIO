import cv2
from ultralytics import YOLO
import positionEstimator


class ObjectDetection():
    
    def __init__(self, model, capture_index):
        self.model = YOLO(model)
        self.cap = cv2.VideoCapture(capture_index)
        if not self.cap.isOpened():
            print("Error: Could not open camera with index 2.")
            exit()
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
    def close(self):
            # Cleanup
            self.cap.release()
            cv2.destroyAllWindows()

    # Detection loop
    def detectAll(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to grab frame.")
            raise Exception("Failed to grab grame.")

        # Run YOLO detection on the frame
        results = self.model(frame, conf=0.5)

        # Draw detections
        for result in results:
            boxes = result.boxes
            names = self.model.names

            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                label = f"{names[cls_id]} {conf:.2f}"

                xyxy = box.xyxy[0].cpu().numpy().astype(int)
                x1, y1, x2, y2 = xyxy

                # Draw box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # Draw label
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # ALL OF OUR CUSTOM DETECTION GOES HERE:
                goals = positionEstimator.estimateGoals(result, frame)
                

        # Show live output
        cv2.imshow("YOLOv8 Live Detection", frame)


if __name__ == "__main__":
    od = ObjectDetection("npjrecog/yolov8_20250424.pt", 2)
    while True:
        od.detectAll()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
