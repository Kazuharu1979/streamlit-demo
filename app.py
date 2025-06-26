import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objs as go

st.set_page_config(page_title="世界経済ダッシュボード", layout="wide")

st.title("🌐 世界経済ダッシュボード")
st.markdown("株価、為替、コモディティなどの主要指標を表示しています。")

# 期間設定
days = st.sidebar.slider("表示期間（日数）", min_value=30, max_value=365, value=90)
start_date = datetime.today() - timedelta(days=days)

# 表示する指標
indices = {
    "S&P 500（米国）": "^GSPC",
    "日経平均（日本）": "^N225",
    "DAX（ドイツ）": "^GDAXI",
    "USD/JPY": "JPY=X",
    "EUR/USD": "EURUSD=X",
    "金（Gold）": "GC=F",
    "WTI原油": "CL=F"
}

# データ取得（キャッシュあり）
@st.cache_data
def get_data(ticker):
    df = yf.download(ticker, start=start_date)
    return df["Close"]

# グリッド表示（2列）
cols = st.columns(2)
for i, (name, ticker) in enumerate(indices.items()):
    with cols[i % 2]:
        st.subheader(name)
        data = get_data(ticker)
        st.write(data.tail())  # データが取得できているか確認
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data, mode='lines'))
        fig.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)
