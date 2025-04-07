import cv2
import socket
from imageRecognition.ballDetection import BallDetection
from imageRecognition.robotDetection import RobotDetection
from imageRecognition.drawBoundingBoxes import drawBoxes
from distanceBetweenObjects import calculateDistance
from angleOfRotationCalculator import calculateAngleOfRotation
from movementController import calculateSpeedAndRotation
from imageRecognition.obstacleDetection import ObstacleDetection
from ultralytics import YOLO
# from col import get_color_name

# Real main for running competition program

def main():
    cap = cv2.VideoCapture(2)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)
    
    # model = YOLO("yolov8_multi_gpu.pt")  # Use 'yolov8n.pt' for the smallest, fastest model
    # modelResults = model(frame)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    ball_detector = BallDetection()                         
    robot_detector = RobotDetection()
    obstacle_detector = ObstacleDetection()
    # robot_detector = RobotColorDetection

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("192.168.138.130", 12358))  # Connect to server
    
    counter=0
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Failed to grab frame")
            break
        
        
        
        orangeballs = ball_detector.DetectOrange(frame.copy()) 
        # whiteballs = ball_detector.DetectWhite(frame.copy()) 
        # balls = ball_detector.detectBalls(frame.copy())
        
        frontrobots = robot_detector.RobotFrontDetection(frame.copy()) 
        backrobots = robot_detector.BackRobotDetection(frame.copy())
        obstacles = obstacle_detector.detectObstacle(frame.copy())

        # -------------------------------
        # Calculate goal position

        # Find the obstacle with the biggest x value which will almost certainly be the boundary
        largestObstacle = max(obstacles, key=lambda obstacle: obstacle[0][2])
        # get the bounding box of obstacle
        x1, y1, x2, y2 = largestObstacle[0]
        # figure out which side the goals are on, x or y
        if abs(x1 - x2) > abs(y1 - y2):
            # goals are along y axis
            yGoal = abs(y1-y2)/2 + y1
            xGoal = x1
        else:
            # goals are along x axis
            yGoal = y1
            xGoal = abs(x1-x2)/2 + x1
        goalPosition = (xGoal, yGoal)

        # --------------------------------
        
        robotToBallDistance = None
        robotToBallAngle = None
        if frontrobots and orangeballs:
            robotToBallDistance = calculateDistance(frontrobots[0][1], orangeballs[0][1])
        if frontrobots and backrobots and orangeballs:
            robotToBallAngle = calculateAngleOfRotation(frontrobots[0][1], backrobots[0][1], orangeballs[0][1])

        robotMovement = calculateSpeedAndRotation(robotToBallDistance, robotToBallAngle)
        
        # client_socket.sendall(f"{round(robotMovement[0])}#{round(robotMovement[1])}\n".encode())

        counter+=1
        
        cv2.imshow("Frame", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
