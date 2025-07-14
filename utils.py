import os
import pandas as pd
import calendar
from datetime import datetime

# data 目錄路徑
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def compute_kin(year: int, month: int, day: int) -> int:
    """
    根據西元年、月、日，計算 Maya 的 KIN 值。
    使用 month_day_accum.csv 和 kin_start_year.csv 兩份檔案。
    """
    # 載入起始 KIN 與累積天數
    kin_start = pd.read_csv(os.path.join(DATA_DIR, "kin_start_year.csv"), index_col="年份")["起始KIN"].to_dict()
    month_accum = pd.read_csv(os.path.join(DATA_DIR, "month_day_accum.csv"), index_col="月份")["累積天數"].to_dict()

    if year not in kin_start:
        raise KeyError(f"找不到年份 {year} 的起始 KIN")
    start_kin = kin_start[year]
    days = month_accum.get(month)
    if days is None:
        raise KeyError(f"找不到月份 {month} 的累積天數")
    # 簡單不考慮閏日分上下
    kin_raw = start_kin + days + day
    kin_mod = kin_raw % 260
    return 260 if kin_mod == 0 else kin_mod

def fetch_emotion_info(kin: int) -> dict:
    """
    從 totem_emotion.csv 讀取並回傳對應 KIN 的情感議題資料。
    """
    path = os.path.join(DATA_DIR, "totem_emotion.csv")
    df = pd.read_csv(path)
    # 統一欄位名稱
    df = df.rename(columns={
        "Kin": "KIN",
        "kin": "KIN",
        " KIN": "KIN",
        "KIN ": "KIN",
    })
    if "KIN" not in df.columns:
        raise KeyError(f"CSV 欄位不包含 'KIN'，目前有：{df.columns.tolist()}")
    matched = df[df["KIN"] == kin]
    if matched.empty:
        raise ValueError(f"No data for KIN {kin}")
    return matched.iloc[0].to_dict()
