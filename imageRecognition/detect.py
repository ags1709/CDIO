import cv2
from ultralytics import YOLO
from imageRecognition.positionEstimator import estimateGoals, estimateGoalNormals, estimateCross, estimatePlayArea, estimatePlayAreaIntermediate, analyze_point_with_polygon, CrossInfo, is_point_in_polygon
from imageRecognition.positionEstimator import estimatePositionFromSquare
from imageRecognition.positionEstimator import tuple_toint
from robotMovement.calculateRobotPosition import correctPerspective
import enum
from robotMovement.tools import tuple_toint

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
    def detectAll(self) -> tuple[cv2.typing.MatLike, dict[str, any], CrossInfo, tuple]:
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
        cap = frame.copy() # RAW CAPTURE! unedited

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
        cross_id = [k for k, v in self.model.names.items() if v == "cross"][0]
        crossinfo = estimateCross(result, cap, frame, cross_id)
        playarea = estimatePlayArea(result, cap, frame)
        goals = estimateGoals(playarea, frame)
        goalNormals = estimateGoalNormals(playarea, frame)
        playAreaIntermediate = estimatePlayAreaIntermediate(result, playarea, frame, margin=165) #pa_tl = playarea of top left... etc
        
        corners = [box.xyxy[0].cpu().numpy().astype(int) for box in boxes if 5 <= box.cls[0] <= 8]
        side_lengths = [max(coords[2] - coords[0], coords[3] - coords[1]) for coords in corners]
        largest_corner_sidelength = max(side_lengths) if len(side_lengths) > 0 else 0
        
        for box in boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = f"{names[cls_id]} {conf:.2f}"

            xyxy = box.xyxy[0].cpu().numpy().astype(int)
            x1, y1, x2, y2 = xyxy

            # If this is a corner, but it's too thin, ignore it and draw a thin red rectangle instead
            if 5 <= cls_id <= 8 and min(x2 - x1, y2 - y1) < largest_corner_sidelength - 10:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                continue

            # Draw box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # Draw label
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            # print(self.model.names)
            
            # Save position or box (Depending on which is appropriate) of all detected things
            if cls_id == 0:
                whiteBalls.append(estimatePositionFromSquare(x1, y1, x2, y2))
            elif cls_id == 1:
                orangeBalls.append(estimatePositionFromSquare(x1, y1, x2, y2))
            elif cls_id == 2:
                egg = ((x1, y1), (x2, y2))
            # elif cls_id == 3:
            #     playfield = ((x1,y1), (x2, y2))
            elif cls_id == 3:
                cross = ((x1, y1), (x2, y2))
            elif cls_id == 4:
                backRightCorner = estimatePositionFromSquare(x1, y1, x2, y2)
                cv2.circle(frame, tuple_toint(correctPerspective(backRightCorner)), 10, (0,0,255), 10)
            elif cls_id == 5:
                frontRightCorner = estimatePositionFromSquare(x1, y1, x2, y2)
                cv2.circle(frame, tuple_toint(correctPerspective(frontRightCorner)), 10, (0,0,255), 10)
            elif cls_id == 6:
                frontLeftCorner = estimatePositionFromSquare(x1, y1, x2, y2)
                cv2.circle(frame, tuple_toint(correctPerspective(frontLeftCorner)), 10, (0,0,255), 10)
            elif cls_id == 7:
                backLeftCorner = estimatePositionFromSquare(x1, y1, x2, y2)
                cv2.circle(frame, tuple_toint(correctPerspective(backLeftCorner)), 10, (0,0,255), 10)



        # A dictionary mapping names of objects we want to a list of their positions, each position being a tuple with 2 points
        # The points being respectively the upperleft and bottomright corner of their bounding box. Each point is itself a tuple of 2 integers.
        # NOTE: goals are stored differently to everything else. goals are stored as a tuple with its x coordinate, and the y coordinate being the middle of the goal.
        positions = {"whiteBalls": whiteBalls, "orangeBalls": orangeBalls,"playfield": playfield, "cross": cross, "egg": egg, "frontLeftCorner": frontLeftCorner, \
             "frontRightCorner": frontRightCorner, "backLeftCorner": backLeftCorner, "backRightCorner": backRightCorner, "goals": goals, "goalNormals": goalNormals}
        
        # Filter robot position
        if frontLeftCorner is not None and is_point_in_polygon(frontLeftCorner, playarea):
            positions["frontLeftCorner"] = frontLeftCorner
        else:
            positions["frontLeftCorner"] = None

        if frontRightCorner is not None and is_point_in_polygon(frontRightCorner, playarea):
            positions["frontRightCorner"] = frontRightCorner
        else:
            positions["frontRightCorner"] = None

        if backLeftCorner is not None and is_point_in_polygon(backLeftCorner, playarea):
            positions["backLeftCorner"] = backLeftCorner
        else:
            positions["backLeftCorner"] = None

        if backRightCorner is not None and is_point_in_polygon(backRightCorner, playarea):
            positions["backRightCorner"] = backRightCorner
        else:
            positions["backRightCorner"] = None


        if len(whiteBalls) == 0 and len(orangeBalls) == 0:
            print("No balls detected, skipping position filtering")
            return frame, positions, crossinfo, playAreaIntermediate
        else:
            # Filter white balls inside playarea
            filtered_white_balls = []
            for ball in whiteBalls:
                # Check if the ball is inside the playarea
                if is_point_in_polygon(ball, playarea):
                    filtered_white_balls.append(ball)
            positions["whiteBalls"] = filtered_white_balls

            # Filter orange balls inside playarea
            filtered_orange_balls = []
            for ball in orangeBalls:
                # Check if the ball is inside the playarea
                if is_point_in_polygon(ball, playarea):
                    filtered_orange_balls.append(ball)
            positions["orangeBalls"] = filtered_orange_balls
        
        
        # Show live output
        
        return frame, positions, crossinfo, playAreaIntermediate

