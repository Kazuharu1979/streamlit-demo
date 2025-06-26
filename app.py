import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objs as go

# ページ設定
st.set_page_config(page_title="世界経済ダッシュボード", layout="wide")
st.title("🌐 世界経済ダッシュボード")
st.markdown("株価、為替、コモディティなどの主要経済指標を視覚化します。")

# サイドバー：表示期間の設定
days = st.sidebar.slider("表示期間（日数）", min_value=30, max_value=365, value=90)
start_date = datetime.today() - timedelta(days=days)

# 指標とティッカーの定義（ETFや安定したティッカーを使用）
indices = {
    "S&P 500（SPY）": "SPY",         # 米国株（S&P500 ETF）
    "日経平均（日本）": "^N225",      # 日本株
    "DAX（ドイツ）": "^GDAXI",        # ドイツ株
    "USD/JPY（ドル円）": "JPY=X",     # 為替
    "EUR/USD（ユーロドル）": "EURUSD=X",
    "金価格（Gold）": "GC=F",         # 金先物
    "原油価格（WTI）": "CL=F"         # 原油先物
}

# データ取得関数（キャッシュ付き）
@st.cache_data
def get_data(ticker):
    df = yf.download(ticker, start=start_date)
    return df["Close"].dropna()

# グラフ表示：2列構成で交互に配置
cols = st.columns(2)
'''
for i, (name, ticker) in enumerate(indices.items()):
    with cols[i % 2]:
        st.subheader(name)
        data = get_data(ticker)
        if data.empty:
            st.warning(f"{name} のデータが取得できませんでした。")
        else:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=data.index.to_pydatetime(),  # 明示的に日付に変換
                y=data.values,
                mode='lines',
                name=name
            ))
            fig.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=30, b=0),
                xaxis_title="日付",
                yaxis_title="価格"
            )
            st.plotly_chart(fig, use_container_width=True)
'''
for i, (name, ticker) in enumerate(indices.items()):
    with cols[i % 2]:
        st.subheader(name)
        data = get_data(ticker).dropna()
        if data.empty:
            st.warning(f"{name} のデータが取得できませんでした。")
            continue
        st.write(data.head())  # ← データの確認
    
        # 一旦標準のline_chartで確認
        st.line_chart(data)
