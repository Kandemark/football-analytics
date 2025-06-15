# app.py

import argparse
from runner.pipeline import run_analytics

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Football Analytics Tool")
    parser.add_argument('--input', type=str, required=True, help="Path to input video")
    args = parser.parse_args()

    run_analytics(args.input)
