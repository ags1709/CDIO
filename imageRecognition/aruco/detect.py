import cv2
import cv2.aruco as aruco

# Load predefined dictionary and create detector
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
detector = aruco.ArucoDetector(aruco_dict)

# Open camera index 3
cap = cv2.VideoCapture(4)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

if not cap.isOpened():
    print("Error: Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Resize to 1280x720
    #frame = cv2.resize(frame, (1280, 720))

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect markers
    corners, ids, _ = detector.detectMarkers(gray)

    # Draw detections
    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners, ids)

    # Display frame
    frame = cv2.resize(frame, (1280, 720))
    cv2.imshow("Aruco Detection - Camera 3", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
