import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def fetch_emotion_info(kin: int) -> dict:
    df = pd.read_csv(os.path.join(DATA_DIR, "totem_emotion.csv"))
    # 將常見的 KIN 欄位名稱統一成 "KIN"
    df = df.rename(columns={
        "Kin": "KIN",
        "kin": "KIN",
        "KIN ": "KIN",
        " KIN": "KIN",
    })
    if "KIN" not in df.columns:
        raise KeyError(f"找不到欄位 'KIN'，目前有：{df.columns.tolist()}")
    # 選出對應的那一列
    matched = df[df["KIN"] == kin]
    if matched.empty:
        raise ValueError(f"No emotion data for KIN {kin}")
    return matched.iloc[0].to_dict()
