# detectors/yolox_detector.py
from .base_detector import Detector

class YOLOXDetector(Detector):
    def detect(self, frame):
        # フレームに対して物体検出を実行
        frame.bounding_boxes.append("YOLOX Box")
        frame.classes.append("Object Class")
        return frame