import pandas as pd
import numpy as np

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame()
    out["age"] = df["age"]
    out["heart_rate"] = df.get("heart_rate", pd.Series(np.nan, index=df.index)).fillna(80)
    out["systolic_bp"] = df.get("systolic_bp", pd.Series(np.nan, index=df.index)).fillna(120)
    out["age_gt_65"] = (out["age"] > 65).astype(int)
    out["shock_index"] = out["heart_rate"] / out["systolic_bp"]
    out = out.fillna(out.median())
    return out
