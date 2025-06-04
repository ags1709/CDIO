import cv2
import numpy as np
import imutils
from datetime import date

cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# today = date.today()
imgCounter = 0
frameCounter = 0
batch = 1
while True:
    ret, frame = cap.read()
    # Capture frame-by-frame
    
    if not ret:
        print("Failed to grab frame")
        break

   
    # Display the resulting frame
    cv2.imshow('Webcam Feed', frame)

    # Take screen shots every tenth frame automatically
    # if frameCounter % 10 == 0:
    #     imgName = f"customData/dataset1/Screenshots/_picture_{imgCounter}.png"
    #     cv2.imwrite(imgName, frame)
    #     print("Screenshot taken")
    #     imgCounter += 1

    key = cv2.waitKey(1)

    # Press 'q' to exit
    if key & 0xFF == ord('q'):
        break

    elif key & 0xFF == ord('s'):
        # imgName = f"customData/{date.today}_picture_{imgCounter}.png"
        imgName = f"test/batch{batch}_picture{imgCounter}.png"

        cv2.imwrite(imgName, frame)
        print("Screenshot taken")
        imgCounter += 1
    frameCounter += 1

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()