import cv2

class RobotDetection:
    def __init__(self):
        # Adjusted Green color range
        self.lowerGreen = (30, 40, 40)  
        self.upperGreen = (90, 255, 255)

        # Adjusted Blue color range
        self.lowerBlue = (85, 40, 40)  
        self.upperBlue = (135, 255, 255)

    def RobotFrontDetection(self, frame):
        frontRobotList = []
        blurred = cv2.GaussianBlur(frame, (9,9),0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        maskGreen = cv2.inRange(hsv, self.lowerGreen, self.upperGreen)
        maskGreen = cv2.erode(maskGreen, None, iterations=2)
        maskGreen = cv2.dilate(maskGreen, None, iterations=2)
        cntsFront, _ = cv2.findContours(maskGreen.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        if len(cntsFront) > 0:
            for front in cntsFront:
                x, y, w, h = cv2.boundingRect(front)
                M = cv2.moments(front)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                frontRobotList.append(center)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) 
                
        return frontRobotList, 

    def BackRobotDetection(self, frame):
        backRobotList = []
        blurred = cv2.GaussianBlur(frame, (9,9),0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        maskBlue = cv2.inRange(hsv, self.lowerBlue, self.upperBlue)
        


        maskBlue = cv2.erode(maskBlue, None, iterations=2)
        maskBlue = cv2.dilate(maskBlue, None, iterations=2)
        cntsBack, _ = cv2.findContours(maskBlue.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        if len(cntsBack) > 0:
            for back in cntsBack:  # front is a single contour now
                x, y, w, h = cv2.boundingRect(back)
                M = cv2.moments(back)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                backRobotList.append(center)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)


                # Display text label above the bounding box
                # cv2.putText(frame, "Detected Color", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # if len(cnts)> 0:
        #     minRadius = 1
        #     validContours = [c for c in cnts if cv2.minEnclosingCircle(c)[1] > minRadius]
        #     for c in validContours:
        #                     cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        #                     cv2.circle(frame, center, 5, (0, 0, 255), -1)
        return backRobotList