import os
import calendar
from PIL import Image
import pandas as pd
import streamlit as st

# ────────────── Path Setup ──────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
IMG_DIR  = os.path.join(BASE_DIR, "images")

# ────────────── Page Config & CSS ──────────────
st.set_page_config(page_title="Maya 生命印記解碼", layout="wide")
st.markdown(
    """<style>
    /* 模擬 Tailwind utility */
    .hero {padding:4rem 2rem; text-align:center; background:#f0f5f9;}
    .hero h1 {font-size:3rem; font-weight:700; margin-bottom:0.5rem;}
    .hero p  {font-size:1.25rem; margin-bottom:1.5rem;}
    .btn-primary {background:#1d4ed8; color:white; padding:0.75rem 1.5rem; border-radius:0.375rem; text-decoration:none;}
    .features, .example, .testimonials, .faq {padding:2rem;}
    .footer {position:fixed; bottom:0; width:100%; background:#1f2937; color:white; text-align:center; padding:1rem;}
    .footer a {color:#60a5fa; text-decoration:none; margin:0 0.5rem;}
    </style>""",
    unsafe_allow_html=True,
)

# ────────────── Hero Section ──────────────
st.markdown(
    """
    <section class="hero">
      <h1>立即解碼你的 Maya 生命印記，喚醒宇宙支持能量</h1>
      <p>只要輸入出生日期，一鍵探索你的專屬靈性密碼，並獲得實踐建議──無需下載、馬上操作。</p>
      <p><em>請從左側面板輸入你的西元生日，即可立即查看。</em></p>
    </section>
    """,
    unsafe_allow_html=True,
)

# ────────────── Load Data ──────────────
try:
    kin_start   = pd.read_csv(os.path.join(DATA_DIR, "kin_start_year.csv"), index_col="年份")["起始KIN"].to_dict()
    month_accum = pd.read_csv(os.path.join(DATA_DIR, "month_day_accum.csv"),   index_col="月份")["累積天數"].to_dict()
    kin_basic   = pd.read_csv(os.path.join(DATA_DIR, "kin_basic_info.csv"))
    emotion_df  = pd.read_csv(os.path.join(DATA_DIR, "totem_emotion.csv"))
except Exception as e:
    st.error(f"❌ 資料載入失敗：{e}")
    st.stop()

# ────────────── Sidebar Input ──────────────
st.sidebar.header("📅 查詢你的 Maya 印記")
year = st.sidebar.selectbox("西元年", sorted(kin_start.keys()), index=sorted(kin_start.keys()).index(1990))
month = st.sidebar.selectbox("月份", list(range(1,13)), index=0)
max_day = calendar.monthrange(year, month)[1]
day = st.sidebar.slider("日期", 1, max_day, 1)

# 僅保留「情感議題」主題，不再提供選擇
category = "情感議題"

# ────────────── KIN 計算 ──────────────
start_kin = kin_start.get(year)
if start_kin is None:
    st.sidebar.error("⚠️ 此年份無起始 KIN")
    st.stop()
raw = start_kin + month_accum.get(month,0) + day
mod = raw % 260
kin = 260 if mod==0 else mod

# ────────────── 顯示基本 KIN 與圖騰 ──────────────
subset = kin_basic[kin_basic["KIN"]==kin]
if subset.empty:
    st.error(f"❓ 找不到 KIN {kin} 資料")
    st.stop()
info = subset.iloc[0]
totem = info["圖騰"]

st.markdown(f"## 🔢 你的 KIN：{kin} ｜ {info['主印記']} — {totem}", unsafe_allow_html=True)
img_file = os.path.join(IMG_DIR, f"{totem}.png")
if os.path.exists(img_file):
    st.image(Image.open(img_file), width=120)

# ────────────── 功能說明 ──────────────
st.markdown("## 🔍 功能說明")
st.markdown("""
1. **輸入你的生日**  
2. **一鍵生成印記**  
3. **深入能量解讀：情感議題**  
   - 個人情感特質（💞）、關係盲點（🚧）、溝通與修復建議（💡）、伴侶需知（🤝）
4. **分享與回饋**  
""", unsafe_allow_html=True)

# ────────────── 深度解讀 ──────────────
df = emotion_df[emotion_df["圖騰"]==totem]
if not df.empty:
    def render_section(df, items, edu_pts):
        for pt in edu_pts:
            st.info(pt)
        row = df.iloc[0]
        for col, label in items:
            if col not in row: continue
            st.markdown(f"### {label}")
            st.caption({
                "個人情感特質":"←你在感情裡的樣子…",
                "情感關係中的盲點":"←相處障礙小陷阱…",
                "改善關係的建議":"←小方法改善溝通…",
                "需要伴侶了解的重點":"←希望對方知道的需求…"
            }[col])
            st.write(row[col])
    render_section(
        df,
        [("個人情感特質","💞 個人情感特質"),
         ("情感關係中的盲點","🚧 情感關係中的盲點"),
         ("改善關係的建議","💡 改善關係的建議"),
         ("需要伴侶了解的重點","🤝 需要伴侶了解的重點")],
        ["先了解自身情感模式，才能有效調整。","告訴對方需求，共創穩定連結。"]
    )

# ────────────── Footer ──────────────
st.markdown(
    """
    <footer class="footer">
       <a href="https://www.facebook.com/soulclean1413/" target="_blank">👉 加入粉專</a> 
      <a href="https://www.instagram.com/tilandky/" target="_blank">👉 追蹤IG</a>
      <a href="https://line.me/R/ti/p/%40690ZLAGN" target="_blank">👉 加入社群</a>
    </footer>
    """,
    unsafe_allow_html=True
)
