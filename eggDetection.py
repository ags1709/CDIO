import numpy as np
import cv2


class EggDetection:
    def __init__(self):
        self.lowerWhite1 = (120, 120, 120)
        self.upperWhite1 = (255, 255, 255)

    def detectEgg(self, frame):
        listofEggs = []
        