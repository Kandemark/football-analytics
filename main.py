import os
import cv2
import numpy as np
from ultralytics import YOLO
from utils.tracker import PlayerTracker
from analysis.heatmap import generate_heatmap
from analysis.exporter import save_tracking_data
from analysis.exporter import export_summary_stats

# Ensure output folder exists
os.makedirs('output', exist_ok=True)

# Load video
video_path = 'input/match.mp4'
cap = cv2.VideoCapture(video_path)

# Load YOLOv8 model (Nano)
model = YOLO('yolov8n.pt')

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Meters per pixel calibration
REAL_FIELD_WIDTH_M = 68  # Real pitch width in meters
meters_per_pixel = REAL_FIELD_WIDTH_M / frame_width

# Initialize tracker
tracker = PlayerTracker(meters_per_pixel=meters_per_pixel)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Run YOLOv8 tracking
    results = model.track(frame, persist=True, classes=[0], conf=0.4)
    if results[0].boxes.id is None:
        continue

    boxes = results[0].boxes.xyxy.cpu().numpy()
    ids = results[0].boxes.id.int().cpu().numpy()

    detections = []
    for box, player_id in zip(boxes, ids):
        x1, y1, x2, y2 = box
        detections.append([x1, y1, x2, y2, player_id])

    # Update tracking
    tracks = tracker.update(detections)

    avg_speeds = tracker.get_average_speeds()

    for x1, y1, x2, y2, track_id in tracks:
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)
        dist = tracker.total_distance.get(track_id, 0)
        speed = avg_speeds.get(track_id, 0)

        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
        cv2.putText(frame, f'ID:{track_id} D:{dist:.1f}m S:{speed:.1f}m/s', (cx - 40, cy - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    cv2.imshow('Football Analytics', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()

# Save tracking data
save_tracking_data(tracker.track_history)

# Generate heatmap
generate_heatmap(tracker.track_history, frame_height, frame_width)

# Export summary stats
distances = tracker.get_distance_covered()
avg_speeds = tracker.get_average_speeds()
max_speeds = tracker.get_max_speeds()

export_summary_stats(distances, avg_speeds, max_speeds)