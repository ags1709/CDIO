import cv2
import socket
from robotMovement.distanceBetweenObjects import calculateDistance
from robotMovement.angleOfRotationCalculator import calculateAngleOfRotation
from robotMovement.movementController import calculateSpeedAndRotation
from robotMovement.calculateRobotPosition import calculateRobotPositionFlexible
from ultralytics import YOLO
import math
from imageRecognition.detect import ObjectDetection, DetectionMode

def main():
    # Set connection to robot
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.settimeout(2.5)
        client_socket.connect(("192.168.137.205", 12358))
        client_socket.settimeout(None) # Set blocking mode
    except Exception as e:
        print("Error connecting to socket")

    #od = ObjectDetection(model="imageRecognition/yolov8_20250424.pt", capture_index=2)
    od = ObjectDetection(model="imageRecognition/yolov8_20250424.pt", image="test/testimg.png")

    # Main loop. Runs entire competition program.
    while True:
        # use model to detect objects
        detectedObjects = od.detectAll()
        
        # This is the two points used to identify the robots position. 
        robotPos = calculateRobotPositionFlexible(detectedObjects["frontLeftCorner"], detectedObjects["frontRightCorner"], detectedObjects["backLeftCorner"], detectedObjects["backRightCorner"])
        print(f"Detected objects: {detectedObjects}")

        robotDistance = None
        robotAngle = None
        vomit = False
        targetBall = None

        if detectedObjects.get("whiteBalls") and len(detectedObjects["whiteBalls"]) > 0:
            targetBall = min(detectedObjects["whiteBalls"], key=lambda ball: calculateDistance(robotPos[0], ball))
            print("Targeting NEAREST WHITE ball")
        elif detectedObjects.get("orangeBalls") and len(detectedObjects["orangeBalls"]) > 0:
            targetBall = min(detectedObjects["orangeBalls"], key=lambda ball: calculateDistance(robotPos[0], ball))
            print("No white balls found. Targeting NEAREST ORANGE ball.")

        # Calculate distance and angle to the selected ball
        if targetBall and robotPos[0] is not None and robotPos[1] is not None:
            robotDistance = calculateDistance(robotPos[0], targetBall)
            robotAngle = calculateAngleOfRotation(robotPos[0], robotPos[1], targetBall)

        if not detectedObjects["whiteBalls"] and not detectedObjects["orangeBalls"]:
            robotDistance = calculateDistance(robotPos[0], detectedObjects["goals"][1])
            robotAngle = calculateAngleOfRotation(robotPos[0], robotPos[1], detectedObjects["goals"][1])
            if robotDistance <= 100 and robotAngle < 0.2 and robotAngle > -0.2:
                vomit = True
            else: 
                vomit = False
        
        robotMovement = calculateSpeedAndRotation(robotDistance, robotAngle)

        # Send data to robot
        try:
            client_socket.sendall(f"{round(robotMovement[0])}#{round(robotMovement[1])}#False#{vomit}\n".encode())
        except Exception:
            print("client not connected")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            od.close()
            break

        if (od.mode == DetectionMode.IMAGE): # Only run once with image
            while True:
                cv2.waitKey(100)

if __name__ == "__main__":
    main()
