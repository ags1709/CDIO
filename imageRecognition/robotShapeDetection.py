import cv2
import numpy as np
import imutils

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        if len(approx) == 3:
            shape = "Triangle"

        elif len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)

            shape = "Square" if ar >= 0.95 and ar <= 1.05 else "Rectangle"

        elif len(approx) == 5:
            shape = "Pentagon"

        else:
            shape = "Circle"

        return shape

cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
# Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to grab frame")
        break

    
    resized = cv2.resize(frame, (1280, 720))
    ratio = frame.shape[0] / float(resized.shape[0])
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    # blurred = cv2.GaussianBlur(gray, (5,5),0)
    thresh = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)[1]
    # cv2.imshow('Webcam Feed', thresh)
    # cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()

    i = 0
    for c in cnts:

        if i == 0:
            i = 1
            continue

        M = cv2.moments(c)
        # if M["m00"] != 0:
        #     cX = int(M["m10"] / M["m00"] * ratio)
        #     cY = int(M["m01"] / M["m00"] * ratio)
        shape = sd.detect(c)

        c = c.astype(float)
        c *= ratio
        c = c.astype(int)
        cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
        # cv2.putText(frame, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
   
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