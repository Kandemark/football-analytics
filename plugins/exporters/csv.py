import csv
from core.interfaces import Exporter
class CsvExporter(Exporter):
    _tag = "exporter"
    def __init__(self):
        self.rows = []
    def add(self, tracks):
        for t in tracks:
            self.rows.append(t)
    def dump(self, path):
        with open(f"{path}/tracks.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "xyxy"])
            writer.writeheader()
            writer.writerows(self.rows)