from ultralytics import YOLO

MODEL_PATH = "models/yolov8n.pt"

class Detector:
    def __init__(self, conf=0.25):
        self.model = YOLO(MODEL_PATH)
        self.conf = conf

    def __call__(self, frame):
        return self.model.predict(frame, conf=self.conf, verbose=False)[0].boxes