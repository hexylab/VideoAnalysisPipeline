# trackers/base_tracker.py
from abc import ABC, abstractmethod
import yaml

class Tracker(ABC):
    def __init__(self, config_path):
        # YAMLコンフィグを読み込み
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

    @abstractmethod
    def track(self, frame):
        pass