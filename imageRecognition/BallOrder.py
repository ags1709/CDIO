import numpy as np
import cv2
from imageRecognition.ballDetection import BallDetection


class BallOrder:
    def __init__(self):
        self.detector = BallDetection()

    def addToBallOrder(self, frame):
        orangeBalls = self.detector.DetectOrange(frame)
        whiteBalls = self.detector.DetectWhite(frame)
        
        ballOrder = []

        for box, center in whiteBalls:
            ballOrder.append((center[0], center[1], 'white')) # Add white balls to the list

        for box, center in orangeBalls:
            ballOrder.append((center[0], center[1], 'orange')) # Add orange balls to the list
            
            ballOrder = sorted(ballOrder, key=lambda b: b[0])

        whiteOrdered = [ball for ball in ballOrder if ball[2] != 'orange'] # Arrange white balls first

        orangeOrdered = [ball for ball in ballOrder if ball[2] == 'orange'] # Arrange orange balls second

        finalOrder = whiteOrdered + orangeOrdered

        return finalOrder, print("Ball Order: ", finalOrder) # Return the ordered list of balls
