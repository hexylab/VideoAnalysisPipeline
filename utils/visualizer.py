# utils/visualizer.py
from abc import ABC, abstractmethod
import cv2

class Visualizer(ABC):
    @abstractmethod
    def visualize(self, frame):
        pass

# YOLOXの認識結果を可視化する派生クラス
class YOLOXVisualizer(Visualizer):
    def visualize(self, frame):
        for box in frame.bounding_boxes:
            cv2.rectangle(frame.image_data, (50, 50), (200, 200), (0, 255, 0), 2)

        for i, obj_class in enumerate(frame.classes):
            cv2.putText(frame.image_data, obj_class, (50, 50 + 30 * i), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        cv2.imshow("YOLOX Processed Frame", frame.image_data)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return False
        return True