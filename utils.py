import pandas as pd
import calendar

def load_data():
    st = __import__('streamlit')
    year = st.sidebar.selectbox("年", list(range(1900, 2101)), index=30)
    month = st.sidebar.selectbox("月", list(range(1, 13)), index=6)
    max_day = calendar.monthrange(year, month)[1]
    day = st.sidebar.slider("日", 1, max_day, 15)
    return year, month, day

def compute_kin(year, month, day):
    kin_start = pd.read_csv('data/kin_start_year.csv', index_col='年份')['起始KIN'].to_dict()
    month_acc = pd.read_csv('data/month_day_accum.csv', index_col='月份')['累積天數'].to_dict()
    start = kin_start.get(year)
    raw = start + month_acc.get(month, 0) + day
    mod = raw % 260
    return 260 if mod == 0 else mod

def fetch_emotion_info(kin):
    df = pd.read_csv('data/totem_emotion.csv')
    row = df[df['KIN']==kin].iloc[0].to_dict()
    return row
