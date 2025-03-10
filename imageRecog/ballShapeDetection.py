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
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to grab frame")
        break


    # lowerOrange = (7, 255, 217)
    # upperOrange = (21, 255, 254)
    lowerOrange = (5, 150, 150)
    upperOrange = (25, 255, 255)

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # frame = imutils.resize(frame, width=600)
    frame = cv2.resize(frame, (1280, 720))
    blurred = cv2.GaussianBlur(frame, (9,9),0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lowerOrange, upperOrange)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    # cv2.imshow("test", frame)
    # cv2.imshow("test", blurred)
    # cv2.imshow("test", hsv)


    
    # thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    
    # cv2.imshow("Grayscale", gray)
    # cv2.imshow("blurred", blurred)
    # cv2.imshow("Thresholded", thresh)

    # contours, _ = cv2.findContours(blurred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)  
    center = None

    if len(cnts)>0:
        minRadius = 1
        # c = max(cnts, key=cv2.contourArea)
        validContours = [c for c in cnts if cv2.minEnclosingCircle(c)[1] > minRadius]
        if validContours:
            c = max(validContours, key=cv2.contourArea)
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > 0:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
    
    # cv2.imshow("Test", mask)

    # for cnt in contours:
    #     perimeter = cv2.arcLength(cnt, True)
    #     approx = cv2.approxPolyDP(cnt, 0.04 * perimeter, True)
    #     area = cv2.contourArea(cnt)
    
    # cv2.drawContours(frame, [cnts], -1, (0, 0, 255), 2)

    # if len(approx) > 1 and area > 100:
    #     (x,y), radius = cv2.minEnclosingCircle(cnt)
    #     radius = int(radius)

    #     if 1 < radius < 100:
    #         cv2.circle(frame, (int(x), int(y)), radius, (0, 255, 0), 2)
    #         cv2.putText(frame, "Ball", (int(x) - 10, int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

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

