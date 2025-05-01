import cv2
import socket
from robotMovement.distanceBetweenObjects import calculateDistance
from robotMovement.angleOfRotationCalculator import calculateAngleOfRotation
from robotMovement.selectRobotTarget import calcDistAndAngleToTarget
from robotMovement.movementController import calculateSpeedAndRotation
from robotMovement.determineAuxiliaryActions import determineAuxiliaryActions
from robotMovement.calculateRobotPosition import calculateRobotPositionFlexible
from ultralytics import YOLO
import math
from imageRecognition.detect import ObjectDetection

def main():
    # Set connection to robot
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("192.168.137.73", 12358))

    # Set image detection model
    od = ObjectDetection("imageRecognition/yolov8_20250424.pt", 2)
    
    # Set initial robot state. State machine can be found in robotMovement/selectRobotTarget.py
    robotState = None

    # Main loop. Runs entire competition program.
    while True:
        # use model to detect objects
        detectedObjects = od.detectAll()

        # Calculate robots distance and angle to target, and set its state
        distanceToTarget, angleToTarget, robotState = calcDistAndAngleToTarget(detectedObjects, robotState)

        # Determine whether to hand balls in or not
        vomit = determineAuxiliaryActions(distanceToTarget, angleToTarget, robotState)

        # Calculate the engine speeds determining the robots movement based on distance and angle to target.
        robotMovement = calculateSpeedAndRotation(distanceToTarget, angleToTarget, robotState)

        # Send data to robot
        client_socket.sendall(f"{round(robotMovement[0])}#{round(robotMovement[1])}#False#{vomit}\n".encode())

        if cv2.waitKey(1) & 0xFF == ord('q'):
            od.close()
            break


if __name__ == "__main__":
    main()
