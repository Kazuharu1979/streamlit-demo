import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objs as go
import pandas as pd

# ページ設定
st.set_page_config(page_title="世界経済ダッシュボード", layout="wide")
st.title("🌐 世界経済ダッシュボード")
st.markdown("株価、為替、コモディティなどの主要経済指標を視覚化します。")

# サイドバー：表示期間
days = st.sidebar.slider("表示期間（日数）", min_value=30, max_value=365, value=90)
start_date = datetime.today() - timedelta(days=days)

# 指標リスト
indices = {
    "S&P 500（SPY）": "SPY",
    "日経平均（日本）": "^N225",
    "DAX（ドイツ）": "^GDAXI",
    "USD/JPY": "JPY=X",
    "EUR/USD": "EURUSD=X",
    "金（Gold）": "GC=F",
    "原油（WTI）": "CL=F"
}

@st.cache_data(ttl=3600)
def fetch_data(ticker):
    df = yf.download(ticker, start=start_date)
    if "Close" in df.columns:
        df = df[["Close"]].dropna()
        df.index = pd.to_datetime(df.index)
        return df
    return pd.DataFrame()

# グラフ表示（2列構成）
cols = st.columns(2)

for i, (label, ticker) in enumerate(indices.items()):
    with cols[i % 2]:
        st.subheader(label)
        df = fetch_data(ticker)
        if df.empty:
            st.warning(f"{label} のデータが取得できませんでした。")
            continue

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df["Close"],
            mode="lines",
            name=label
        ))
        fig.update_layout(
            xaxis_title="日付",
            yaxis_title="価格",
            height=300,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
