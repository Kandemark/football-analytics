# runner/pipeline.py

import os
import cv2
from ultralytics import YOLO
from utils.tracker import PlayerTracker
from analysis.heatmap import generate_heatmap
from analysis.exporter import save_tracking_data, export_summary_stats

def run_analytics(video_path):
    os.makedirs('output', exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    model = YOLO('yolov8n.pt')

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    REAL_FIELD_WIDTH_M = 68
    meters_per_pixel = REAL_FIELD_WIDTH_M / frame_width

    tracker = PlayerTracker(meters_per_pixel=meters_per_pixel)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        results = model.track(frame, persist=True, classes=[0], conf=0.4)
        if results[0].boxes.id is None:
            continue

        boxes = results[0].boxes.xyxy.cpu().numpy()
        ids = results[0].boxes.id.int().cpu().numpy()

        detections = []
        for box, player_id in zip(boxes, ids):
            x1, y1, x2, y2 = box
            detections.append([x1, y1, x2, y2, player_id])

        tracks = tracker.update(detections, frame)
        avg_speeds = tracker.get_average_speeds()
        staminas = tracker.estimate_stamina()

        for x1, y1, x2, y2, track_id in tracks:
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)
            dist = tracker.total_distance.get(track_id, 0)
            speed = avg_speeds.get(track_id, 0)
            stamina = staminas.get(track_id, 100)
            team = tracker.get_team(track_id)

            # Team color
            color = (200, 200, 200)
            if team == "Red":
                color = (0, 0, 255)
            elif team == "Blue":
                color = (255, 0, 0)
            elif team == "Green":
                color = (0, 255, 0)

            # Stamina color
            if stamina > 70:
                stamina_color = (0, 255, 0)
            elif stamina > 40:
                stamina_color = (0, 255, 255)
            else:
                stamina_color = (0, 0, 255)

            # Draw box and labels
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            label = f'{team} ID:{track_id} D:{dist:.1f}m S:{speed:.1f}m/s'
            cv2.putText(frame, label, (cx - 40, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
            cv2.putText(frame, f'Sta:{stamina:.0f}%', (cx - 40, cy + 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, stamina_color, 1)

       
        cv2.imshow('Football Analytics', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    save_tracking_data(tracker.track_history)
    generate_heatmap(tracker.track_history, frame_height, frame_width, tracker.teams)


    distances = tracker.get_distance_covered()
    avg_speeds = tracker.get_average_speeds()
    max_speeds = tracker.get_max_speeds()

    export_summary_stats(distances, avg_speeds, max_speeds, tracker.teams)

