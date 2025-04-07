import cv2
import numpy as np
import imutils
from datetime import date

cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

today = date.today()
imgCounter = 0
while True:
# Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to grab frame")
        break

   
    # Display the resulting frame
    cv2.imshow('Webcam Feed', frame)

    key = cv2.waitKey(1)

    # Press 'q' to exit
    if key & 0xFF == ord('q'):
        break

    elif key & 0xFF == ord('s'):
        imgName = f"customData/{today}_picture_{imgCounter}.png"
        cv2.imwrite(imgName, frame)
        print("Screenshot taken")
        imgCounter += 1

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()