# utils/data_loader.py
from abc import ABC, abstractmethod
import cv2

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

    def __iter__(self):
        return self

    def __next__(self):
        ret, frame_data = self.cap.read()
        if not ret:
            self.release()
            raise StopIteration("Error: Could not read frame from video source.")
        
        # フレームデータを返す
        return frame_data

    def release(self):
        self.cap.release()

# MP4ファイルから読み込む派生クラス
class MP4DataLoader(DataLoader):
    def __init__(self, filepath):
        self.cap = cv2.VideoCapture(filepath)
        if not self.cap.isOpened():
            raise ValueError(f"Error: Could not open file {filepath}.")

    def __iter__(self):
        return self

    def __next__(self):
        ret, frame_data = self.cap.read()
        if not ret:
            self.release()
            raise StopIteration("End of video file.")
        
        return frame_data

    def release(self):
        self.cap.release()