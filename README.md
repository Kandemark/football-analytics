

sport-analytics/
├── app.py                    # single entry point (GUI/CLI)
├── config/
│   └── sport_configs/
│       ├── football.yaml
│       ├── basketball.yaml
│       ├── tennis.yaml
│       └── __template__.yaml
├── core/                     # zero sport-specific code
│   ├── __init__.py
│   ├── tracker.py            # generic SORT / ByteTrack / etc.
│   ├── detector.py           # YOLOv8 wrapper
│   ├── exporter.py           # CSV / JSON / MP4 output
│   └── heatmap.py            # generic heatmap renderer
├── plugins/                  # ONLY place you touch for a new sport
│   ├── football/
│   │   ├── classes.py        # “ball”, “goalkeeper”, …
│   │   ├── filters.py        # ball size ratios, goal-area masks, …
│   │   └── visual.py         # pitch drawing, team-colour logic
│   ├── basketball/
│   │   ├── classes.py
│   │   ├── filters.py
│   │   └── visual.py
│   └── __template__/         # copy-paste starter
├── data/
│   └── videos/
│       └── match.mp4
├── models/
│   └── yolov8n.pt
└── requirements.txt