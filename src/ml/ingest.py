"""Simple ingest placeholder - in production this reads INSPIRE/MIMIC CSVs and normalizes."""
import argparse
import pandas as pd
import os
import sys

# Ensure project root on path for imports
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    df = pd.DataFrame({
        "patient_id": ["p1", "p2", "p3"],
        "age": [70, 55, 82],
        "heart_rate": [88, 72, 95],
        "systolic_bp": [130, 120, 110],
        "in_hospital_mortality": [1, 0, 1]
    })
    df.to_csv(args.out, index=False)
    print(f"Wrote {args.out}")
