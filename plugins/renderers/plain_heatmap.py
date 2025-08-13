import cv2, numpy as np
from core.interfaces import Renderer
class PlainHeatmap(Renderer):
    _tag = "renderer"
    def __init__(self):
        self.frames = []
    def add_frame(self, frame, tracks):
        self.frames.append(frame)
    def save(self, path):
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        h, w = self.frames[0].shape[:2]
        out = cv2.VideoWriter(f"{path}/heatmap.mp4", fourcc, 30, (w, h))
        for f in self.frames: out.write(f)
        out.release()