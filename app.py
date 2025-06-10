
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Baccarat Tracker", layout="centered")
st.title("🎰 Baccarat Tracker Mini App")

# Session state
if 'results' not in st.session_state:
    st.session_state.results = []

# Nhập kết quả từng ván
st.subheader("➕ Nhập từng kết quả")
col1, col2 = st.columns(2)
with col1:
    if st.button("➕ Banker (B)", use_container_width=True):
        st.session_state.results.append("B")
with col2:
    if st.button("➕ Player (P)", use_container_width=True):
        st.session_state.results.append("P")

# Nhập chuỗi kết quả
st.subheader("📥 Nhập chuỗi kết quả (cách nhau bằng dấu phẩy)")
input_string = st.text_input("Ví dụ: B,P,P,B,B", key="input_seq")
if st.button("✅ Thêm chuỗi"):
    new_data = [x.strip().upper() for x in input_string.split(",") if x.strip().upper() in ["B", "P"]]
    st.session_state.results.extend(new_data)

# Hiển thị kết quả đã nhập
st.subheader("📊 Lịch sử kết quả")
if st.session_state.results:
    df = pd.DataFrame(st.session_state.results, columns=["Kết quả"])
    st.dataframe(df, use_container_width=True)

    # Xuất file CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Tải xuống CSV", data=csv, file_name="baccarat_history.csv", mime='text/csv')

    # Reset
    if st.button("♻️ Reset kết quả", type="primary"):
        st.session_state.results = []
else:
    st.info("Chưa có kết quả nào được nhập.")
