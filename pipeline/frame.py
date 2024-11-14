# pipeline/frame.py
class Frame:
    def __init__(self, image_data):
        self.image_data = image_data
        self.bboxes = []
        self.class_ids = []
        self.classes = []
        self.scores = []
        self.tracking_ids = []
        
    def __str__(self):
        return (f"Image Data: {self.image_data}, "
                f"Bounding Boxes: {self.bounding_boxes}, "
                f"Classes: {self.classes}, "
                f"Scores: {self.scores}, "
                f"Tracking IDs: {self.tracking_ids}")