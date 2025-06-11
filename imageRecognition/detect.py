import cv2
from ultralytics import YOLO
from imageRecognition.positionEstimator import estimateGoals, estimateCross, estimatePlayArea, CrossInfo
from imageRecognition.positionEstimator import estimatePositionFromSquare
import enum

class DetectionMode(enum.Enum):
    CAMERA=0
    IMAGE=1

class ObjectDetection():
    
    # def __init__(self, model, capture_index: int):
    #     self.model = YOLO(model)
    #     self.model.to('cuda')
    #     self.cap = cv2.VideoCapture(capture_index)
    #     self.mode = DetectionMode.CAMERA
    #     if not self.cap.isOpened():
    #         print("Error: Could not open camera with index ", capture_index)
    #         exit()
    #     self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    #     self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    
    def __init__(self, model, detection_mode: DetectionMode, image: str = "", capture_index: int = 0):
        self.model = YOLO(model)
        self.model.to("cuda")
        self.mode = detection_mode
        if detection_mode == DetectionMode.IMAGE:
            self.frame = cv2.imread(image)
            if self.frame is None:
                print("Error: Could not open image @ ", image)
                exit()
            self.frame = cv2.resize(self.frame, (1920, 1080))
        elif detection_mode == DetectionMode.CAMERA:
            self.cap = cv2.VideoCapture(capture_index)
            if not self.cap.isOpened():
                print("Error: Could not open camera with index ", capture_index)
                exit()
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    
        
    def close(self):
            # Cleanup
            if self.mode == DetectionMode.CAMERA:
                self.cap.release()
            cv2.destroyAllWindows()

    # Detection loop
    def detectAll(self) -> tuple[cv2.typing.MatLike, dict[str, any], CrossInfo]:
        if self.mode == DetectionMode.CAMERA:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame.")
                raise Exception("Failed to grab grame.")
        elif self.mode == DetectionMode.IMAGE:
            frame = self.frame.copy()
        else:
            raise Exception("Detection mode not supported: ", self.mode)

        # Run YOLO detection on the frame
        # results = self.model(frame, conf=0.5)
        result = self.model(frame, conf=0.5)[0]

        # Draw detections
        boxes = result.boxes
        names = self.model.names
        
        # ALL OF OUR CUSTOM DETECTION GOES HERE:
        whiteBalls = []
        orangeBalls = []
        egg = None
        playfield = None
        cross = None
        backRightCorner = None
        frontRightCorner = None
        frontLeftCorner = None
        backLeftCorner = None
        goals = estimateGoals(result, frame)
        crossinfo = estimateCross(result, frame)
        playarea = estimatePlayArea(result, frame)
        
        
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
            
            # Save position or box (Depending on which is appropriate) of all detected things
            if cls_id == 0:
                whiteBalls.append(estimatePositionFromSquare(x1, y1, x2, y2))
            elif cls_id == 1:
                orangeBalls.append(estimatePositionFromSquare(x1, y1, x2, y2))
            elif cls_id == 2:
                egg = ((x1, y1), (x2, y2))
            elif cls_id == 3:
                playfield = ((x1, y1), (x2, y2))
            elif cls_id == 4:
                cross = ((x1, y1), (x2, y2))
            elif cls_id == 5:
                backRightCorner = estimatePositionFromSquare(x1, y1, x2, y2)
            elif cls_id == 6:
                frontRightCorner = estimatePositionFromSquare(x1, y1, x2, y2)
            elif cls_id == 7:
                frontLeftCorner = estimatePositionFromSquare(x1, y1, x2, y2)
            elif cls_id == 8:
                backLeftCorner = estimatePositionFromSquare(x1, y1, x2, y2)


        # A dictionary mapping names of objects we want to a list of their positions, each position being a tuple with 2 points
        # The points being respectively the upperleft and bottomright corner of their bounding box. Each point is itself a tuple of 2 integers.
        # NOTE: goals are stored differently to everything else. goals are stored as a tuple with its x coordinate, and the y coordinate being the middle of the goal.
        positions = {"whiteBalls": whiteBalls, "orangeBalls": orangeBalls, "playfield": playfield, "cross": cross, "egg": egg, "frontLeftCorner": frontLeftCorner, \
                     "frontRightCorner": frontRightCorner, "backLeftCorner": backLeftCorner, "backRightCorner": backRightCorner, "goals": goals}
        
        # Show live output
        
        return frame, positions, crossinfo

