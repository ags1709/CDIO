import cv2
from imageRecognition.ballColorDetection import BallDetection
from imageRecognition.robotColorDetection import RobotDetection

def main():
    cap = cv2.VideoCapture(2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    ball_detector = BallDetection()
    robot_detector = RobotDetection()  
    # robot_detector = RobotColorDetection

    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Failed to grab frame")
            break
        
        orangeballs = ball_detector.DetectOrange(frame) 
        whiteballs = ball_detector.DetectWhite(frame) 
        frontrobots = robot_detector.RobotFrontDetection(frame) 
        backrobots = robot_detector.BackRobotDetection(frame) 

        for ball in orangeballs:
            cv2.circle(frame, ball, 2, (0, 165, 255), 2)  # Draw for each orange ball
        for white in whiteballs: 
            cv2.circle(frame, white, 2, (0, 0, 0), 2)  # Draw for each orange ball 

        for robot in frontrobots:
            if isinstance(robot, tuple) and len(robot) == 2:  # Ensure it's a tuple with two elements
                x, y = robot
                cv2.rectangle(frame, (x - 15, y - 15), (x + 15, y + 15), (0, 255, 0), 2)  
            else:
                print("Unexpected format in frontrobots:", robot)

        for robot in backrobots:
            if isinstance(robot, tuple) and len(robot) == 2:  # Ensure it's a tuple with two elements
                x, y = robot
                cv2.rectangle(frame, (x - 15, y - 15), (x + 15, y + 15), (255, 0, 0), 2)  
            else:
                print("Unexpected format in backrobots:", robot)

        print("Orange Balls detected:", orangeballs)
        print("White Balls detected:", whiteballs)
        print("Front Robots detected:", frontrobots)
        print("Back Robots detected:", backrobots)
        
        cv2.imshow("Frame", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
