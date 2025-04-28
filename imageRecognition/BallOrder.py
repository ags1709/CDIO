import numpy as np
import cv2
from imageRecognition.ballDetection import BallDetection


class BallOrder:
    def __init__(self):
        self.detector = BallDetection()
        self.pickupballs = []
        self.ballcheck = 20 # Check if the ball is picked up or not. the check is in pixels

    def is_same_ball(self, center1, center2):
        # Check if two centers are within the correct distance
        return np.linalg.norm(np.array(center1) - np.array(center2)) < self.ballcheck


    def updatePickupBalls(self, currentball):
        updateballs = [] # Create a new list to store the updated balls

        for current in currentball:
            found = False
            for pickup in self.pickupballs:
                if self.is_same_ball(current[0:2], pickup[0:2]):
                    found = True
                    break

            if not found:
                updateballs.append(current)

        return updateballs # Return the updated list of balls
        
    def addToBallOrder(self, frame):
        orangeBalls = self.detector.DetectOrange(frame)
        whiteBalls = self.detector.DetectWhite(frame)
        
        ballOrder = []

        for box, center in whiteBalls:
            ballOrder.append((center[0], center[1], 'white'))

        for box, center in orangeBalls:
            ballOrder.append((center[0], center[1], 'orange'))

        ballOrder = sorted(ballOrder, key=lambda b: b[0])  # Move outside loops

        ballOrder = self.updatePickupBalls(ballOrder)


        whiteOrdered = [ball for ball in ballOrder if ball[2] != 'orange'] # Arrange white balls first

        orangeOrdered = [ball for ball in ballOrder if ball[2] == 'orange'] # Arrange orange balls second

        finalOrder = whiteOrdered + orangeOrdered
 
        return finalOrder, print("Ball Order: ", finalOrder) # Return the ordered list of balls
