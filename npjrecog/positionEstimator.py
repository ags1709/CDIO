

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
        goal1 = (x1,ymid)
        goal2 = (x2,ymid)
        cv2.circle(cap, goal1, 30, (200, 150, 0), 3)
        cv2.circle(cap, goal2, 30, (200, 150, 0), 3)
        return [goal1, goal2]
    else:
        print("WARNING! No playfield detected, no goal estimation done")
    
    

import cv2
from ultralytics import YOLO
if __name__ == '__main__':
    model = YOLO("npjrecog/yolov8_20250424.pt")
    cap = cv2.imread("npjrecog/test/testimg.png")
    results = model(cap, conf=0.3)
    
    for result in results:
        estimateGoals(result, cap)
        cap = cv2.resize(cap, (1280, 720))  
        cv2.imshow("YOLOv8 Live Detection", cap)
        cv2.waitKey(10000) 
