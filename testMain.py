import traceback
import cv2
import socket
from robotMovement.determineAuxiliaryActions import determineAuxiliaryActions
from robotMovement.distanceBetweenObjects import calculateDistance
from robotMovement.angleOfRotationCalculator import calculateAngleOfRotation
from robotMovement.movementController import calculateSpeedAndRotation
from robotMovement.calculateRobotPosition import calculateRobotPositionFlexible
from ultralytics import YOLO
import math
from imageRecognition.detect import ObjectDetection, DetectionMode
from robotMovement.selectRobotTarget import calcDistAndAngleToTarget

def main():
    # Set connection to robot
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.settimeout(2.5)
        #client_socket.connect(("192.168.137.205", 12358))
        client_socket.settimeout(None) # Set blocking mode
    except Exception as e:
        print("Error connecting to socket")

    od = ObjectDetection(model="imageRecognition/ImageModels/best.pt", detection_mode=DetectionMode.IMAGE, image="test/RobotOutsidePlayAreapicture0.png")
    #od = ObjectDetection(model="imageRecognition/yolov8_20250424.pt", detection_mode=DetectionMode.CAMERA, capture_index=2)

    # Main loop. Runs entire competition program.
        # use model to detect objects

        # Calculate robots distance and angle to target, and set its state
    try:
        frame, detectedObjects, crossInfo, playAreaIntermediate = od.detectAll()
        distanceToTarget, angleToTarget, robotState = calcDistAndAngleToTarget(detectedObjects, crossInfo, playAreaIntermediate, frame)

        cv2.putText(frame, f"State: {robotState}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 4)
        
        vomit = determineAuxiliaryActions(distanceToTarget, angleToTarget, robotState)
        print(f"vomit", vomit, "distance", distanceToTarget)
        robotMovement = calculateSpeedAndRotation(distanceToTarget, angleToTarget, robotState)

        # Show the result
        cv2.imshow("Result", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        od.close()

    except Exception as e:
        print(e)
        print(traceback.print_exc())
            #pass
        # Calculate distance and angle to the selected ball
        # if targetBall and robotPos[0] is not None and robotPos[1] is not None:
        #     robotDistance = calculateDistance(robotPos[0], targetBall)
        #     robotAngle = calculateAngleOfRotation(robotPos[0], robotPos[1], targetBall)

        # if not detectedObjects["whiteBalls"] and not detectedObjects["orangeBalls"]:
        #     robotDistance = calculateDistance(robotPos[0], detectedObjects["goals"][1])
        #     robotAngle = calculateAngleOfRotation(robotPos[0], robotPos[1], detectedObjects["goals"][1])
        #     if robotDistance <= 100 and robotAngle < 0.2 and robotAngle > -0.2:
        #         vomit = True
        #     else: 
        #         vomit = False
        
        # robotMovement = calculateSpeedAndRotation(robotDistance, robotAngle)

        # Send data to robot
    if cv2.waitKey(1) & 0xFF == ord('q'):
        od.close()

    if (od.mode == DetectionMode.IMAGE): # Only run once with image
        while True:
            cv2.waitKey(100)

if __name__ == "__main__":
    main()
