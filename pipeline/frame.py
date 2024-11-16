# pipeline/frame.py
from datetime import datetime

class Frame:
    def __init__(self, image_data):
        self.source_img = image_data
        self.vis_img = image_data
        self.timestamp = datetime.now()
        self.fps = 0
        self.width = 0
        self.height = 0
        self.elapsed_time = 0
        self.bboxes = []
        self.class_ids = []
        self.classes = []
        self.scores = []
        self.track_ids = []
        
    def __str__(self):
        return (f"Bounding Boxes: {self.bboxes}, "
                f"Classes: {self.classes}, "
                f"Scores: {self.scores}, "
                f"Tracking IDs: {self.track_ids}")