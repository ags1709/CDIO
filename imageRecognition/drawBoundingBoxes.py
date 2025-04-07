import cv2

def drawBoxes(frame, boundingBoxList):
    for box in boundingBoxList:
        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
        