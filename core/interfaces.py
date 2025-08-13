from abc import ABC, abstractmethod

class Filter(ABC):
    @abstractmethod
    def __call__(self, dets, meta):  # detections → detections
        pass

class Tracker(ABC):
    @abstractmethod
    def update(self, dets):          # detections → tracks
        pass

class Renderer(ABC):
    @abstractmethod
    def add_frame(self, frame, tracks):  # side-effect drawing
        pass
    @abstractmethod
    def save(self, path):
        pass

class Exporter(ABC):
    @abstractmethod
    def add(self, tracks):
        pass
    @abstractmethod
    def dump(self, path):
        pass