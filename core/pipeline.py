import cv2
def run(detector, filter, tracker, renderer, exporter, video_path):
    cap = cv2.VideoCapture(video_path)
    while True:
        ok, frame = cap.read()
        if not ok: break
        dets = detector(frame)
        dets = filter(dets, meta={"frame": int(cap.get(cv2.CAP_PROP_POS_FRAMES))})
        trks = tracker.update(dets)
        renderer.add_frame(frame, trks)
        exporter.add(trks)
    cap.release()
    renderer.save("output")
    exporter.dump("output")