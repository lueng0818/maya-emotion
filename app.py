import streamlit as st
from utils import load_data, compute_kin, fetch_emotion_info

# Streamlit UI
st.title("情感議題查詢系統")
year, month, day = load_data()
kin = compute_kin(year, month, day)
info = fetch_emotion_info(kin)
st.header(f"您的 KIN: {kin}")
st.subheader(info['圖騰'])
st.write("💞 個人情感特質:", info['個人情感特質'])
st.write("🚧 情感關係中的盲點:", info['情感關係中的盲點'])
st.write("💡 改善關係的建議:", info['改善關係的建議'])
st.write("🤝 需要伴侶了解的重點:", info['需要伴侶了解的重點'])
