sport-analytics/
├─ launcher.py                     # 30-line bootstrap
├─ registry.py                     # auto-discovers plugins
├─ config/
│  ├─ sessions/                    # YAML recipe files
│  │  ├─ football.yaml
│  │  ├─ basketball.yaml
│  │  ├─ tennis.yaml
│  │  └─ minimal.yaml
│  └─ default.yaml                 # fallback
├─ core/
│  ├─ interfaces.py                # 4 ABCs (Filter, Tracker, Renderer, Exporter)
│  ├─ detector.py                  # single YOLO wrapper (yolov8n.pt)
│  └─ pipeline.py                  # generic DAG runner
├─ plugins/
│  ├─ filters/
│  │  ├─ __init__.py               # exposes plugin list
│  │  ├─ ball_only.py
│  │  ├─ team_color.py
│  │  └─ tennis_ball.py
│  ├─ trackers/
│  │  ├─ __init__.py
│  │  └─ sort_tracker.py
│  ├─ renderers/
│  │  ├─ __init__.py
│  │  ├─ football_pitch.py
│  │  ├─ basketball_court.py
│  │  └─ plain_heatmap.py
│  └─ exporters/
│     ├─ __init__.py
│     ├─ csv.py
│     └─ video_overlay.py
├─ models/
│  └─ yolov8n.pt                   # provided model
├─ tests/                          # pytest skeletons
├─ requirements.txt
└─ README.md                       # quick-start


'''
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python launcher.py --config config/sessions/football.yaml --video match.mp4

'''