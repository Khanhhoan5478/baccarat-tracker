
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

st.set_page_config(page_title="Theo dõi cầu Baccarat", layout="centered")
st.title("📊 App Theo Dõi Cầu Baccarat (Nâng cấp)")

# Khởi tạo session state nếu chưa có
def init_session():
    if "results" not in st.session_state:
        st.session_state.results = []

init_session()

# Nhập kết quả thủ công
st.subheader("1️⃣ Nhập kết quả thủ công")
col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Banker (B)"):
        st.session_state.results.append("B")

with col2:
    if st.button("➕ Player (P)"):
        st.session_state.results.append("P")

# Nhập hàng loạt
st.subheader("2️⃣ Nhập hàng loạt (vd: B,B,P,B,P,P)")
bulk_input = st.text_input("Nhập kết quả cách nhau bằng dấu phẩy")
if st.button("✅ Thêm hàng loạt"):
    bulk_results = [x.strip().upper() for x in bulk_input.split(",") if x.strip().upper() in ["B", "P"]]
    st.session_state.results.extend(bulk_results)
    st.success(f"Đã thêm {len(bulk_results)} kết quả")

# Hiển thị kết quả
st.markdown("---")
st.subheader("📋 Lịch sử kết quả")
if st.session_state.results:
    df = pd.DataFrame({'Ván': list(range(1, len(st.session_state.results)+1)),
                       'Kết quả': st.session_state.results})
    st.dataframe(df, use_container_width=True)

    # Tần suất
    counts = df['Kết quả'].value_counts()
    st.subheader("📊 Tần suất xuất hiện")
    st.bar_chart(counts)

    # Chuỗi liên tiếp
    streaks = []
    current = st.session_state.results[0]
    count = 1
    for i in range(1, len(st.session_state.results)):
        if st.session_state.results[i] == current:
            count += 1
        else:
            streaks.append((current, count))
            current = st.session_state.results[i]
            count = 1
    streaks.append((current, count))

    st.subheader("🔁 Phân tích chuỗi liên tiếp")
    for s in streaks:
        st.write(f"{s[0]}: {s[1]} lần liên tiếp")

    # Tải file CSV
    st.subheader("💾 Xuất báo cáo")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Tải báo cáo (.csv)", data=csv, file_name="bao_cao_baccarat.csv", mime='text/csv')

    # Lưu lịch sử
    st.subheader("🗃️ Lưu lịch sử phiên")
    history_text = ",".join(st.session_state.results)
    st.download_button("💾 Tải file phiên (.txt)", history_text, file_name="lich_su_baccarat.txt")

    # Reset
    if st.button("🔁 Reset tất cả dữ liệu"):
        st.session_state.results = []
        st.success("Đã reset dữ liệu!")

else:
    st.info("Chưa có dữ liệu. Hãy bắt đầu nhập kết quả từng ván.")

# Tải lại lịch sử
st.subheader("📂 Tải lại từ file lịch sử")
uploaded_file = st.file_uploader("Chọn file .txt chứa chuỗi kết quả (B,P)", type=['txt'])
if uploaded_file:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    content = stringio.read()
    new_results = [x.strip().upper() for x in content.split(",") if x.strip().upper() in ["B", "P"]]
    st.session_state.results = new_results
    st.success(f"Đã tải {len(new_results)} kết quả từ file")
