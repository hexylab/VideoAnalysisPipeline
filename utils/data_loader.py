# utils/data_loader.py
from abc import ABC, abstractmethod
import cv2

from pipeline.frame import Frame

class DataLoader(ABC):
    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass

    @abstractmethod
    def release(self):
        pass


# Webカメラから読み込む派生クラス
class CameraDataLoader(DataLoader):
    def __init__(self, source=0):
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise ValueError("Error: Could not open video source.")
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print("Camera Stream Parameter")
        print("FPS: ", fps)
        print("Width:", width)
        print("Height:", height)

    def __iter__(self):
        return self

    def __next__(self):
        ret, frame_data = self.cap.read()
        if not ret:
            self.release()
            raise StopIteration("Error: Could not read frame from video source.")
        frame = Frame(frame_data)
        frame.fps = self.cap.get(cv2.CAP_PROP_FPS)
        frame.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return frame
    
    def stream(self, frame):
        for frm in self:
            return frm

    def release(self):
        self.cap.release()


# Videoファイルから読み込む派生クラス
class VideoDataLoader(DataLoader):
    def __init__(self, filepath):
        self.cap = cv2.VideoCapture(filepath)
        if not self.cap.isOpened():
            raise ValueError(f"Error: Could not open file {filepath}.")
        print("Video Stream Parameter")
        print("FPS: ", fps)
        print("Width:", width)
        print("Height:", height)

    def __iter__(self):
        return self

    def __next__(self):
        ret, frame_data = self.cap.read()
        if not ret:
            self.release()
            raise StopIteration("End of video file.")
        frame = Frame(frame_data)
        frame.fps = self.cap.get(cv2.CAP_PROP_FPS)
        frame.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return frame

    def release(self):
        self.cap.release()