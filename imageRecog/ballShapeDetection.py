import cv2
import numpy as np

cap = cv2.VideoCapture(2)

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


    lower_orange = (7, 255, 217)
    upper_orange = (21, 255, 254)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (9,9),2)

    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    
    # cv2.imshow("Grayscale", gray)
    # cv2.imshow("blurred", blurred)
    # cv2.imshow("Thresholded", thresh)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        perimeter = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.04 * perimeter, True)
        area = cv2.contourArea(cnt)
    
    cv2.drawContours(frame, [cnt], -1, (0, 0, 255), 2)

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

