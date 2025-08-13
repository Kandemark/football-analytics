from core.interfaces import Filter
class BallOnly(Filter):
    _tag = "filter"
    def __call__(self, dets, meta):
        return [d for d in dets if d.cls == 0]  # YOLO class 0 = ball