import sys
import os
from pathlib import Path

# 確保同目錄下的 utils.py 可以被匯入
sys.path.append(os.path.dirname(__file__))

import streamlit as st
from utils import compute_kin, fetch_emotion_info

# 基本頁面設定
st.set_page_config(page_title="情感議題查詢", layout="centered")

st.title("💞 情感議題｜Maya 圖騰心靈解讀")

# 側欄輸入
st.sidebar.header("輸入你的生日")
year = st.sidebar.number_input("年 (西元)", min_value=1900, max_value=2100, value=1990)
month = st.sidebar.selectbox("月", list(range(1,13)))
day = st.sidebar.selectbox("日", list(range(1,32)))
if st.sidebar.button("查詢 KIN"):
    try:
        kin = compute_kin(year, month, day)
        info = fetch_emotion_info(kin)
    except Exception as e:
        st.error(f"❌ 查詢失敗: {e}")
    else:
        st.subheader(f"你的 KIN：{kin}  ｜ 圖騰：{info['圖騰']}")
        st.markdown("---")
        # 顯示四大情感欄位
        sections = [
            ("個人情感特質", "💞 你的情感特質"),
            ("情感關係中的盲點", "🚧 關係盲點"),
            ("改善關係的建議", "💡 改善建議"),
            ("需要伴侶了解的重點", "🤝 對方須知"),
        ]
        for key, title in sections:
            if key in info:
                st.markdown(f"### {title}")
                st.write(info[key])
        st.markdown("---")
        st.caption("感謝使用！若有問題，歡迎回報。")
else:
    st.info("請在側欄輸入生日，然後點「查詢 KIN」。")
