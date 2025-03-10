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


    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # # Define color ranges (tune these based on lighting)
    # lower_orange = np.array([7, 255, 217])
    # upper_orange = np.array([21, 255, 254])

    # lower_white = np.array([0, 0, 200])
    # upper_white = np.array([180, 50, 255])

    # # Create masks
    # maskOrange = cv2.inRange(hsv, lower_orange, upper_orange)
    # maskWhite = cv2.inRange(hsv, lower_white, upper_white)

    # # Find contours
    # contoursOrange, _ = cv2.findContours(maskOrange, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # contoursWhite, _ = cv2.findContours(maskWhite, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # for cnt in contoursOrange:
    #     if cv2.contourArea(cnt) > 500:  # Filter small noise
    #         x, y, w, h = cv2.boundingRect(cnt)
    #         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 165, 255), 2)
    #         cv2.putText(frame, "Orange Ball", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)

    # for cnt in contoursWhite:
    #     if cv2.contourArea(cnt) > 500:
    #         x, y, w, h = cv2.boundingRect(cnt)
    #         cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
    #         cv2.putText(frame, "White Ball", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

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


# Convert rgb values to hsv. Must be manually printed and changed 
# rgbLightOrange = np.uint8([[[254, 179, 0]]])
# rgbShadowOrange = np.uint8([[[217, 51, 0]]])
# hsvLightOrange = cv2.cvtColor(rgbLightOrange, cv2.COLOR_RGB2HSV)
# hsvShadowOrange = cv2.cvtColor(rgbShadowOrange, cv2.COLOR_RGB2HSV)
# print(f"hsv light orange: {hsvLightOrange}")
# print(f"hsv shadow orange: {hsvShadowOrange}")
# --------------------------------------------------


# while True:
#     ret,frame  = cap.read()

#     if not ret:
#         print("Failed to grep frame")
#         break

#     cv2.imshow("test", frame)

#     k = cv2.waitKey(1)

#     if k%256 == 27:
#         print("Escape hit, closing app")
#         break
    
#     elif k%256 == 32:
#         img_name = "opencv_frame_{}.png".format(imgCounter)
#         cv2.imwrite(imgName, frame)
#         print("Screenshot taken")
#         imgCounter += 1

# cap.release()

# cap.destroyAllWindows()










#  ------------------------------------------------------------------


# def list_available_captures(max_tested=10):
#     available_captures = []
    
#     for i in range(max_tested):
#         cap = cv2.VideoCapture(i)
#         if cap.isOpened():
#             available_captures.append(i)
#             cap.release()  # Release the camera after checking

#     return available_captures

# available_cameras = list_available_captures()
# print("Available camera indices:", available_cameras)