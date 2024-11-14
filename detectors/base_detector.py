# detectors/base_detector.py
from abc import ABC, abstractmethod

class Detector(ABC):
    @abstractmethod
    def detect(self, frame):
        pass