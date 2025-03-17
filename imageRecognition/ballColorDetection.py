import cv2
import numpy as np

class BallDetection:
    def __init__(self):
        self.lowerWhite = (0, 0, 180)
        self.upperWhite = (180, 30, 255)
        self.lowerOrange = (10, 70, 80) 
        self.upperOrange = (65, 255, 255)

    def DetectOrange(self, frame):        
        listOfOrangeBalls = []
        # Orange color for the walls/bounds are around 5-10 for lower and upper
        # lowerOrange = (15, 150, 150)
        # upperOrange = (25, 255, 255)
        # Updated ranges to that might handle differing light conditions better?
        # lowerWhite = (0, 0, 150) 
        # upperWhite = (120, 40, 255)

            
        frame = cv2.resize(frame, (1280, 720))
        blurred = cv2.GaussianBlur(frame, (9,9),0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        maskOrange = cv2.inRange(hsv, self.lowerOrange, self.upperOrange)
        
        maskOrange = cv2.erode(maskOrange, None, iterations=2)
        maskOrange = cv2.dilate(maskOrange, None, iterations=2)



        cntsOrange, _ = cv2.findContours(maskOrange.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # cnts = cv2.findContours(maskWhite, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # cnts = imutils.grab_contours(cnts)
            # center = None

            # if len(cntsOrange) > 0:
            #     for front in cntsOrange:  # front is a single contour now
            #         x, y, w, h = cv2.boundingRect(front)
            #         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if len(cntsOrange)> 0:
            minRadius = 1
            validContours = [c for c in cntsOrange if cv2.minEnclosingCircle(c)[1] > minRadius]
            for c in validContours:
                ((x,y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                listOfOrangeBalls.append(center)

                if radius > minRadius:
                    approx = cv2.approxPolyDP(c, 0.02 * cv2.arcLength(c, True), True)
                    circularity = 4 * np.pi * (cv2.contourArea(c) / (cv2.arcLength(c, True) ** 2))

                    if 0.82 < circularity < 1.5:
                        if M["m00"] > 0:
                                
                            cv2.circle(frame, (int(x), int(y)), int(radius), (20, 255, 255), 2)
                            cv2.circle(frame, center, 5, (20, 255, 255), -1)


        return listOfOrangeBalls
    
    def DetectWhite(self, frame):
        listofWhiteBalls = []

        frame = cv2.resize(frame, (1280, 720))
        blurred = cv2.GaussianBlur(frame, (9,9),0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        maskWhite = cv2.inRange(hsv, self.lowerWhite, self.upperWhite)
        maskWhite = cv2.dilate(maskWhite, None, iterations=2)
        maskWhite = cv2.erode(maskWhite, None, iterations=2)

        cntsWhite, _ = cv2.findContours(maskWhite.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        if len(cntsWhite)> 0:
            minRadius = 1
            validContours = [c for c in cntsWhite if cv2.minEnclosingCircle(c)[1] > minRadius]
            for c in validContours:
                ((x,y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                if(M["m10"] != 0 or M["m00"] != 0 or M["m01"] != 0):
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    listofWhiteBalls.append(center)

                    if radius > minRadius:
                        approx = cv2.approxPolyDP(c, 0.02 * cv2.arcLength(c, True), True)
                        circularity = 4 * np.pi * (cv2.contourArea(c) / (cv2.arcLength(c, True) ** 2))

                        if 0.82 < circularity < 1.5:
                            if M["m00"] > 0:
                                    
                                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 0), 2)
                                cv2.circle(frame, center, 5, (0, 0, 0), -1)
        return listofWhiteBalls