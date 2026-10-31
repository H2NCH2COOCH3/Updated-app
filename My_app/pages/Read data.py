import streamlit as st
import pandas as pd
# =========================
# Đọc dữ liệu
# =========================
data = pd.read_csv("travel.csv")
# =========================
# Tiêu đề
# =========================
st.title("✈️ Nhật ký chuyến đi")
st.write("Danh sách các chuyến đi của tôi")
# =========================
# Hiển thị dữ liệu
# =========================
st.subheader("📋 Tất cả chuyến đi")
st.dataframe(data)
# =========================
# Tổng số chuyến đi
st.write("Các địa điểm đã đi:")
diadiem_list = data["diadiem"].unique()
st.write(diadiem_list)
# =========================
# Chọn địa điểm
# =========================
st.subheader("🔎 Tìm kiếm chuyến đi")

diadiem = st.selectbox(
    "Chọn địa điểm:",
    diadiem_list
)
# =========================
# Lọc dữ liệu
# =========================
result = data[data["diadiem"] == diadiem]
# =========================
# Hiển thị kết quả
# =========================

st.write("Các chuyến đi đến:", diadiem)
st.dataframe(result)

# =========================
# Số chuyến đi tại địa điểm
# =========================

st.write(
    "Số chuyến đi:",
    len(result)
)