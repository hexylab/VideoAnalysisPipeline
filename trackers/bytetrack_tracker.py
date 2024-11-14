# trackers/bytetrack_tracker.py
from .base_tracker import Tracker

class ByteTrackTracker(Tracker):
    def track(self, frame):
        # フレームに対してトラッキングを実行
        frame.tracking_ids.append("ByteTrack ID")
        return frame