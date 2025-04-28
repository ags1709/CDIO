import cv2
from ultralytics import YOLO

def estimateGoals(result, cap):
    boxes = result.boxes
    id_playfield = 3
    playfield_box = [x for x in boxes if x.cls == id_playfield]
    if len(playfield_box) > 1:
        print("WARNING! ", len(playfield_box), " playfield_boxes detected, expected 1. defaulting to index 0")
    if (len(playfield_box) == 1):
        box = playfield_box[0]
        xyxy = box.xyxy[0].cpu().numpy().astype(int)
        x1, y1, x2, y2 = xyxy
        ymid = int(y1+(y2-y1)/2)
        leftGoal = (x1,ymid)
        rightGoal = (x2,ymid)
        cv2.circle(cap, leftGoal, 30, (200, 150, 0), 3)
        cv2.circle(cap, rightGoal, 30, (200, 150, 0), 3)
        return [leftGoal, rightGoal]
    else:
        print("WARNING! No playfield detected, no goal estimation done")
    
def estimatePositionFromSquare(x1,y1,x2,y2):
    xCoordinate = (x1 + x2) / 2
    yCoordinate = (y1 + y2) / 2

    return (xCoordinate, yCoordinate)