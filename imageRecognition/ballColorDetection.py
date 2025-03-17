import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()
imgCounter = 0
listOfBalls = []
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to grab frame")
        break


    # Orange color for the walls/bounds are around 5-10 for lower and upper
    lowerOrange = (15, 150, 150)
    upperOrange = (25, 255, 255)

    lowerWhite = (0, 0, 180)
    upperWhite = (180, 30, 255)


    # Updated ranges to that might handle differing light conditions better?
    # lowerOrange = (10, 70, 80) 
    # upperOrange = (65, 255, 255)

    # lowerWhite = (0, 0, 150) 
    # upperWhite = (120, 40, 255)

    
    frame = cv2.resize(frame, (1280, 720))
    blurred = cv2.GaussianBlur(frame, (9,9),0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    maskOrange = cv2.inRange(hsv, lowerOrange, upperOrange)
    maskWhite = cv2.inRange(hsv, lowerWhite, upperWhite)
    
    maskOrange = cv2.erode(maskOrange, None, iterations=2)
    maskOrange = cv2.dilate(maskOrange, None, iterations=2)

    maskWhite = cv2.erode(maskWhite, None, iterations=2)
    maskWhite = cv2.dilate(maskWhite, None, iterations=2)

    mask = cv2.bitwise_or(maskOrange, maskWhite)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    if len(cnts)> 0:
        minRadius = 1
        validContours = [c for c in cnts if cv2.minEnclosingCircle(c)[1] > minRadius]
        for c in validContours:
            ((x,y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            listOfBalls.append(center)

            if radius > minRadius:
                approx = cv2.approxPolyDP(c, 0.02 * cv2.arcLength(c, True), True)
                circularity = 4 * np.pi * (cv2.contourArea(c) / (cv2.arcLength(c, True) ** 2))

                if 0.82 < circularity < 1.5:
                    if M["m00"] > 0:
                        
                        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                        cv2.circle(frame, center, 5, (0, 0, 255), -1)


    # Display the resulting frame
    cv2.imshow('Webcam Feed', frame)

    key = cv2.waitKey(1)

    # Press 'q' to exit
    if key & 0xFF == ord('q'):
        break

    elif key & 0xFF == ord('s'):
        imgName = "data/opencv_frame_{}.png".format(imgCounter)
        cv2.imwrite(imgName, frame)
        print("Screenshot taken")
        imgCounter += 1

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()

