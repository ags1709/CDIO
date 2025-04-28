import cv2
import socket
from robotMovement.distanceBetweenObjects import calculateDistance
from robotMovement.angleOfRotationCalculator import calculateAngleOfRotation
from robotMovement.movementController import calculateSpeedAndRotation
from robotMovement.calculateRobotPosition import calculateRobotPositionFlexible
from ultralytics import YOLO
import math
from imageRecognition.detect import ObjectDetection

def main():
    # Set connection to robot
    # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client_socket.connect(("192.168.137.73", 12358))

    od = ObjectDetection("imageRecognition/yolov8_20250424.pt", 2)
    
    # States for state machine
    SEARCH_BALLS = "SEARCH_BALLS"
    TO_INTERMEDIARY = "TO_INTERMEDIARY"
    TO_GOAL = "TO_GOAL"
    
    state = SEARCH_BALLS
    # intermediaryPointReached = False

    # Main loop. Runs entire competition program.
    while True:
        # use model to detect objects
        detectedObjects = od.detectAll()
        
        # This is the two points used to identify the robots position. 
        robotPos = calculateRobotPositionFlexible(detectedObjects["frontLeftCorner"], detectedObjects["frontRightCorner"], detectedObjects["backLeftCorner"], detectedObjects["backRightCorner"])

        robotDistance = None
        robotAngle = None
        vomit = False
        targetBall = None

        # Use state machine
        if state == SEARCH_BALLS:
            if detectedObjects.get("whiteBalls") and len(detectedObjects["whiteBalls"]) > 0:
                targetBall = min(detectedObjects["whiteBalls"], key=lambda ball: calculateDistance(robotPos[0], ball))
            elif detectedObjects.get("orangeBalls") and len(detectedObjects["orangeBalls"]) > 0:
                targetBall = min(detectedObjects["orangeBalls"], key=lambda ball: calculateDistance(robotPos[0], ball))

            # Calculate distance and angle to the selected ball
            if targetBall and robotPos[0] is not None and robotPos[1] is not None:
                robotDistance = calculateDistance(robotPos[0], targetBall)
                robotAngle = calculateAngleOfRotation(robotPos[0], robotPos[1], targetBall)

            # If no balls are present, move to intermediary point in preperation for turning in balls.
            if not detectedObjects["whiteBalls"] and not detectedObjects["orangeBalls"]:
                state = TO_INTERMEDIARY

        elif state == TO_INTERMEDIARY:
            intermediaryPoint = (detectedObjects["goals"][1][0] - 300, detectedObjects["goals"][1][1])
            # Have robots middle point reach the intermediary point as it makes for better arrival at goal.
            robotMiddle = ((robotPos[0][0] + robotPos[1][0]) / 2, (robotPos[0][1] + robotPos[1][1]) / 2)

            robotDistance = calculateDistance(robotMiddle, intermediaryPoint)
            robotAngle = calculateAngleOfRotation(robotPos[0], robotPos[1], intermediaryPoint)    

            if robotDistance <= 10 and -0.2 < robotAngle < 0.2:
                state = TO_GOAL
                # intermediaryPointReached = True
        
        elif state == TO_GOAL:
            # NOTE: This turns in balls in the small goal. This assumes that the small goal is on the right side of the camera
            goalPos = detectedObjects["goals"][1]

            robotDistance = calculateDistance(robotPos[0], goalPos)
            robotAngle = calculateAngleOfRotation(robotPos[0], robotPos[1], goalPos)
            if robotDistance <= 100 and robotAngle < 0.2 and robotAngle > -0.2:
                vomit = True
            else: 
                vomit = False
        
        robotMovement = calculateSpeedAndRotation(robotDistance, robotAngle, state)

        # Send data to robot
        # client_socket.sendall(f"{round(robotMovement[0])}#{round(robotMovement[1])}#False#{vomit}\n".encode())


        if cv2.waitKey(1) & 0xFF == ord('q'):
            od.close()
            break


if __name__ == "__main__":
    main()
