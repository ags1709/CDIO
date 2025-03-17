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


    
    # # Green color range
    # lowerGreen = (35, 50, 50)  # Lower bound for green in HSV
    # upperGreen = (85, 255, 255)  # Upper bound for green in HSV
    
    # # Blue color range
    # lowerBlue = (90, 50, 50)  # Lower bound for blue in HSV
    # upperBlue = (130, 255, 255)  # Upper bound for blue in HSV

    # Adjusted Green color range
    lowerGreen = (30, 40, 40)  
    upperGreen = (90, 255, 255)

    # Adjusted Blue color range
    lowerBlue = (85, 40, 40)  
    upperBlue = (135, 255, 255)

    
    frame = cv2.resize(frame, (1280, 720))
    blurred = cv2.GaussianBlur(frame, (9,9),0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    maskGreen = cv2.inRange(hsv, lowerGreen, upperGreen)
    maskBlue = cv2.inRange(hsv, lowerBlue, upperBlue)
    
    maskGreen = cv2.erode(maskGreen, None, iterations=2)
    maskGreen = cv2.dilate(maskGreen, None, iterations=2)

    maskBlue = cv2.erode(maskBlue, None, iterations=2)
    maskBlue = cv2.dilate(maskBlue, None, iterations=2)

    mask = cv2.bitwise_or(maskGreen, maskBlue)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None


    if len(cnts) > 0:
        for c in cnts:
            # Get bounding box around detected colored region
            x, y, w, h = cv2.boundingRect(c)

            # Draw bounding box (blue)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Display text label above the bounding box
            # cv2.putText(frame, "Detected Color", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # if len(cnts)> 0:
    #     minRadius = 1
    #     validContours = [c for c in cnts if cv2.minEnclosingCircle(c)[1] > minRadius]
    #     for c in validContours:
    #                     cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
    #                     cv2.circle(frame, center, 5, (0, 0, 255), -1)




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

