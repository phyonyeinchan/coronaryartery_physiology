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
    parser.add_argument("--in", dest="input", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    df = pd.read_csv(args.input)
    df = df.drop_duplicates(subset=["patient_id"])
    df.to_csv(args.out, index=False)
    print(f"Wrote {args.out}")
