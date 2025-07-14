import os
import pandas as pd

# data 目錄路徑
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def compute_kin(year: int, month: int, day: int) -> int:
    """
    根據西元年、月、日，計算 Maya 的 KIN 值。
    使用 month_day_accum.csv 和 kin_start_year.csv 兩份檔案。
    """
    kin_start = pd.read_csv(
        os.path.join(DATA_DIR, "kin_start_year.csv"),
        index_col="年份",
        dtype={"年份": int, "起始KIN": int}
    )["起始KIN"].to_dict()

    month_accum = pd.read_csv(
        os.path.join(DATA_DIR, "month_day_accum.csv"),
        index_col="月份",
        dtype={"月份": int, "累積天數": int}
    )["累積天數"].to_dict()

    if year not in kin_start:
        raise KeyError(f"找不到年份 {year} 的起始 KIN")
    if month not in month_accum:
        raise KeyError(f"找不到月份 {month} 的累積天數")

    start_kin = kin_start[year]
    days = month_accum[month]

    kin_raw = start_kin + days + day
    kin_mod = kin_raw % 260
    return 260 if kin_mod == 0 else kin_mod


def fetch_emotion_info(kin: int) -> dict:
    """
    1) 先讀 kin_basic_info.csv 拿到對應圖騰 (totem)
    2) 再到 totem_emotion.csv 依圖騰去撈情感欄位
    """
    # 1) 讀 KIN→圖騰
    kb = pd.read_csv(
        os.path.join(DATA_DIR, "kin_basic_info.csv"),
        dtype={"KIN": int, "圖騰": str}
    )
    row = kb[kb["KIN"] == kin]
    if row.empty:
        raise ValueError(f"No basic info found for KIN {kin}")
    totem = row.iloc[0]["圖騰"]

    # 2) 讀情感表 by 圖騰
    emo = pd.read_csv(
        os.path.join(DATA_DIR, "totem_emotion.csv"),
        dtype=str
    )
    # 假設檔頭正確，欄位名就是「圖騰」跟四個情感欄位
    matched = emo[emo["圖騰"] == totem]
    if matched.empty:
        raise ValueError(f"No emotion-data for totem {totem}")
    info = matched.iloc[0].to_dict()

    # 加回 KIN 與 Totem
    info["KIN"] = kin
    info["圖騰"] = totem
    return info
