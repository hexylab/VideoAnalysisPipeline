# detectors/base_detector.py
from abc import ABC, abstractmethod
import yaml

class Detector(ABC):
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.config=yaml.safe_load(f)

    @abstractmethod
    def detect(self, frame):
        pass