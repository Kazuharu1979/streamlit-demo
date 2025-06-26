# app.py
import streamlit as st

st.set_page_config(page_title="世界経済ダッシュボード", layout="wide")

st.title("🌐 世界経済ダッシュボード")
st.markdown("各種指標から世界経済の動向を把握するシンプルなアプリです。")

# サイドバー（今後インタラクション追加予定）
st.sidebar.header("表示設定")

# 2列レイアウト
col1, col2 = st.columns(2)
with col1:
    st.subheader("ここに株価・為替のチャートを表示")
with col2:
    st.subheader("ここに金・原油などのコモディティを表示")
