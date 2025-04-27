import cv2
from ultralytics import YOLO
from imageRecognition.positionEstimator import estimateGoals


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
        # results = self.model(frame, conf=0.5)
        result = self.model(frame, conf=0.5)[0]

        # Draw detections
        boxes = result.boxes
        names = self.model.names
        
        # ALL OF OUR CUSTOM DETECTION GOES HERE:
        whiteBalls = []
        orangeBalls = []
        egg = []
        playfield = []
        cross = []
        backRightCorner = []
        frontRightCorner = []
        frontLeftCorner = []
        backLeftCorner = []
        goals = estimateGoals(result, frame)
        
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
            
            # Add box to its corresponding list
            if cls_id == 0:
                whiteBalls.append(((x1, y1), (x2, y2)))
            elif cls_id == 1:
                orangeBalls.append(((x1, y1), (x2, y2)))
            elif cls_id == 2:
                egg.append(((x1, y1), (x2, y2)))
            elif cls_id == 3:
                playfield.append(((x1, y1), (x2, y2)))
            elif cls_id == 4:
                cross.append(((x1, y1), (x2, y2)))
            elif cls_id == 5:
                backRightCorner.append(((x1, y1), (x2, y2)))
            elif cls_id == 6:
                frontRightCorner.append(((x1, y1), (x2, y2)))
            elif cls_id == 7:
                frontLeftCorner.append(((x1, y1), (x2, y2)))
            elif cls_id == 8:
                backLeftCorner.append(((x1, y1), (x2, y2)))


        # A dictionary mapping names of objects we want to a list of their positions, each position being a tuple with 2 points
        # The points being respectively the upperleft and bottomright corner of their bounding box. Each point is itself a tuple of 2 integers.
        # NOTE: goals are stored differently to everything else. goals are stored as a tuple with its x coordinate, and the y coordinate being the middle of the goal.
        positions = {"whiteBalls": whiteBalls, "orangeBalls": orangeBalls, "playfield": playfield, "cross": cross, "egg": egg, "frontLeftCorner": frontLeftCorner, \
                     "frontRightCorner": frontRightCorner, "backLeftCorner": backLeftCorner, "backRightCorner": backRightCorner, "goals": goals}
        
        # Show live output
        cv2.imshow("YOLOv8 Live Detection", frame)
        return positions

