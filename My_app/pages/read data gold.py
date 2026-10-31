import streamlit as st
import pandas as pd

data = pd.read_csv("gold.csv")
data["date"] = pd.to_datetime(data["date"])

st.title("ỨNG DỤNG THEO DÕI GIÁ VÀNG")

# Chọn nhiều năm
years = sorted(data["year"].unique())

selected_years = st.multiselect(
    "Chọn các năm muốn xem",
    options=years,
    default=years
)

# Lọc dữ liệu theo các năm được chọn
filtered_data = data[data["year"].isin(selected_years)]

st.write("Dữ liệu giá vàng")
st.dataframe(filtered_data)

# Vẽ biểu đồ
st.subheader("1. Biểu đồ đường")
st.line_chart(filtered_data, x="date", y="price")

st.subheader("2. Biểu đồ cột")
st.bar_chart(filtered_data, x="date", y="price")