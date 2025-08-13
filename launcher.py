import argparse, yaml, cv2
from core.detector import Detector
from core.pipeline import run
from registry import PLUGINS

ap = argparse.ArgumentParser()
ap.add_argument("--config", required=True)
ap.add_argument("--video", required=True)
args = ap.parse_args()

cfg = yaml.safe_load(open(args.config))

det = Detector()
flt = PLUGINS["filter"][cfg["filter"]]()
trk = PLUGINS["tracker"][cfg["tracker"]]()
ren = PLUGINS["renderer"][cfg["renderer"]]()
exp = PLUGINS["exporter"][cfg["exporter"]]()

run(det, flt, trk, ren, exp, args.video)