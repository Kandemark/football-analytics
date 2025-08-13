from filterpy.kalman import KalmanFilter
import numpy as np
from core.interfaces import Tracker

class SortTracker(Tracker):
    _tag = "tracker"
    def __init__(self, max_age=30, min_hits=3):
        self.max_age, self.min_hits = max_age, min_hits
        self.trackers = []
    def update(self, dets):
        # minimal SORT implementation
        return [{"id": 1, "xyxy": d.xyxy} for d in dets]  # stub