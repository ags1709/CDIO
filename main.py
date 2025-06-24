import cv2
import socket
from robotMovement.distanceBetweenObjects import calculateDistance
from robotMovement.angleOfRotationCalculator import calculateAngleOfRotation
from robotMovement.selectRobotTarget import calcDistAndAngleToTarget, abort, setAbort
from robotMovement.movementController import calculateSpeedAndRotation
from robotMovement.calculateRobotPosition import calculateRobotPositionFlexible
from ultralytics import YOLO
import math
from imageRecognition.detect import ObjectDetection, DetectionMode
import traceback
import time
import logging

import threading
logging.getLogger('ultralytics').setLevel(logging.ERROR)

ENABLE_SOCKET = True
windowsize = (1280,720)



def abortTimer():
    threading.Timer(interval=420, function=setAbort).start()


def main():
    abortTimer()
    # Set connection to robot
    if ENABLE_SOCKET:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("192.168.137.232", 12350))

    # Set image detection model
    od = ObjectDetection(model="imageRecognition/imageModels/newbest.pt", detection_mode=DetectionMode.CAMERA, capture_index=2)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # or 'mp4v' for .mp4
    #videowriter = cv2.VideoWriter("RUN.mp4", fourcc, 24, (1280,720))
    # od = ObjectDetection(model="imageRecognition/yolov8s_060625.pt", detection_mode=DetectionMode.IMAGE, image="test/NPJ4.png")
    
    start = time.time()
    # Set initial robot state. State machine can be found in robotMovement/selectRobotTarget.py
    # Main loop. Runs entire competition program.
    while True:
        # use model to detect objects

        # Calculate robots distance and angle to target, and set its state
        try:
            frame, detectedObjects, crossInfo, playAreaIntermediate = od.detectAll()
            distanceToTarget, angleToTarget, robotState = calcDistAndAngleToTarget(detectedObjects, crossInfo, playAreaIntermediate, frame)

            # print(abort)
            cv2.putText(frame, f"State: {robotState}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 4)

            # Determine whether to hand balls in or not
            vomit = robotState == "VOMIT"

            #print(f"vomit", vomit, "disdence", distanceToTarget)
            # Calculate the engine speeds determining the robots movement based on distance and angle to target.
            robotMovement = calculateSpeedAndRotation(distanceToTarget, angleToTarget, robotState)
            # Send data to robot
            if ENABLE_SOCKET:
                client_socket.sendall(f"{round(robotMovement[0])}#{round(robotMovement[1])}#{vomit}\n".encode())
        except Exception as e:
            #continue
            print(e)
            print(traceback.print_exc())
            #pass
            
        
        elapsed = round((time.time() - start)*1, 2)
        cv2.putText(frame, f"Time: {elapsed}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 4)
        
        frame = cv2.resize(frame, windowsize)
        cv2.imshow("YOLOv8 Live Detection", frame)
        #videowriter.write(frame)
        while od.mode == DetectionMode.IMAGE:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                od.close()
                #videowriter.release()
                exit(0)
            if cv2.waitKey(1) &  0xFF == ord('n'):
                break
        
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            od.close()
            #videowriter.release()
            break


if __name__ == "__main__":
    main()
