import numpy as np
import cv2


class ObstacleDetection:

    def __init__(self):
        self.lowerOrange = (0, 150, 150)
        self.upperOrange = (10, 255, 255)

    
    def detectObstacle(self, frame):
        listOfObstacles = []

        blurred = cv2.GaussianBlur(frame, (9,9),0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        maskRed = cv2.inRange(hsv, self.lowerOrange, self.upperOrange)

        maskRed = cv2.erode(maskRed, None, iterations=2)
        maskRed = cv2.dilate(maskRed, None, iterations=2)
        cntsRed, _ = cv2.findContours(maskRed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(cntsRed) > 0:
            for c in cntsRed:                                               
                x, y, w, h = cv2.boundingRect(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                listOfObstacles.append([(x,y,x+w,y+h),center])

        return listOfObstacles

