# utils/tracker.py

import sys
import os
sys.path.append(os.path.abspath("tracking/sort"))
from sort import Sort
import numpy as np
from collections import defaultdict
import cv2

class PlayerTracker:
    def __init__(self, meters_per_pixel=1.0):
        self.tracker = Sort()
        self.track_history = defaultdict(list)
        self.total_distance = defaultdict(float)
        self.speeds = defaultdict(list)
        self.last_positions = {}
        self.meters_per_pixel = meters_per_pixel
        self.team_assignments = {}  # player_id -> team_name

    def update(self, detections, frame=None):
        if len(detections) == 0:
            dets = np.empty((0, 5))
        else:
            dets = np.array(detections)

        tracks = self.tracker.update(dets)

        for x1, y1, x2, y2, track_id in tracks:
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            track_id = int(track_id)
            self.track_history[track_id].append((cx, cy))

            if track_id in self.last_positions:
                x_prev, y_prev = self.last_positions[track_id]
                dx, dy = cx - x_prev, cy - y_prev
                dist = ((dx**2 + dy**2)**0.5) * self.meters_per_pixel
                self.total_distance[track_id] += dist

                speed = dist  # since frame rate is roughly 1 frame per sec
                self.speeds[track_id].append(speed)

            self.last_positions[track_id] = (cx, cy)

            # Assign team if not done already
            if frame is not None and track_id not in self.team_assignments:
                self.team_assignments[track_id] = self._detect_team_color(frame, x1, y1, x2, y2)

        return tracks

    def _detect_team_color(self, frame, x1, y1, x2, y2):
        # Crop upper body region
        h = int(y2 - y1)
        jersey_area = frame[int(y1):int(y1 + 0.4 * h), int(x1):int(x2)]
        if jersey_area.size == 0:
            return "Unknown"

        # Average color in BGR
        avg_color = cv2.mean(jersey_area)[:3]
        b, g, r = avg_color

        if r > 150 and g < 100 and b < 100:
            return "Red"
        elif b > 150 and r < 100 and g < 100:
            return "Blue"
        elif g > 150 and r < 100 and b < 100:
            return "Green"
        else:
            return "Unknown"

    def get_distance_covered(self):
        return self.total_distance

    def get_average_speeds(self):
        return {k: sum(v)/len(v) for k, v in self.speeds.items() if len(v) > 0}

    def get_max_speeds(self):
        return {k: max(v) for k, v in self.speeds.items() if len(v) > 0}

    def get_team(self, track_id):
        return self.team_assignments.get(track_id, "Unknown")

    def estimate_stamina(self):
        stamina = {}
        for track_id in self.track_history:
            distance = self.total_distance.get(track_id, 0)
            avg_speed = np.mean(self.speeds.get(track_id, [0]))
            
            # Basic stamina model: high distance + speed reduces stamina
            # Max distance expected: 10,000m (professional level)
            # Max speed considered: 8 m/s (sprinting)
            normalized_dist = min(distance / 10000, 1)
            normalized_speed = min(avg_speed / 8, 1)
            
            # Assume stamina depletes faster if avg speed is high
            depletion_factor = 0.6 * normalized_dist + 0.4 * normalized_speed
            stamina_score = max(1.0 - depletion_factor, 0) * 100  # Scale to 0–100%
            
            stamina[track_id] = round(stamina_score, 1)
        return stamina
