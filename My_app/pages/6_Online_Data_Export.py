import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Xuất dữ liệu online ra Excel ", layout="wide")
st.title("Lấy dữ liệu online và xuất Excel")
st.markdown("ứng dụng lấy dữ liệu online từ API và cho phép tải xuống file excel")

#====================================
# Hàm lấy dữ liệu online
@st.cache_data
def load_data():
    url = "https://api.gold-api.com/price/XAU"
    respone = requests.get(url)
    data = respone.json()
    rows = [{
        "Loại vàng": data.get("metal", "XAU"),
        "Gía hiện tại": data.get("price", 0),
        "Đơn vị tiền": data.get("currency", "USD"),
        "Sàn giao dịch": data.get("exchange", "Global"),
        "Thời gian cập nhật": data.get("timestamp", "N/A")
    }]
    return pd.DataFrame(rows)
#===========================
#Hiển thị dữ liệu
df = load_data()
st.subheader("Dữ liệu online ")
st.dataframe(df, use_container_width=True)

#=================
#Tiềm kiếm
st.subheader("Dữ liệu giá vàng")
filtered_df = df
st.dataframe(filtered_df, use_container_width=True)

##########################
#Xuất dữ liệu
def conver_to_excel(dataframe):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        dataframe.to_excel(writer, index=False, sheet_name='Data')
    processed_data = output.getvalue()
    return processed_data
excel_data = conver_to_excel(filtered_df)

st.download_button(
    label="Tải file excel",
    data = excel_data,
    file_name="du_lieu_online.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

#==========================
#thống kê nhanh
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Tổng dữ liệu", len(df))
with col2:
    st.metric("Sau khi lọc", len(filtered_df))
with col3:
    st.metric("Đơn vị tiền", filtered_df["Đơn vị tiền"].iloc[0])

#============================
#Biểu đồ đơn giản

st.subheader("Giá vàng hiện tại")

gold_price = filtered_df["Gía hiện tại"].iloc[0]

chart_df = pd.DataFrame({
    "Thời gian": [
        "-5 phút",
        "-4 phút",
        "-3 phút",
        "-2 phút",
        "-1 phút",
        "Hiện tại"
    ],
    "Giá vàng": [
        gold_price - 15,
        gold_price - 10,
        gold_price - 7,
        gold_price - 5,
        gold_price - 2,
        gold_price
    ]
})

st_autorefresh(interval=10 * 1000, key="refresh")

st.title("Phân tích tỷ giá USD/VND")
# =========================
# REALTIME EXCHANGE RATE
# =========================
@st.cache_data(ttl=10)
def load_exchange_rate():
    url = "https://open.er-api.com/v6/latest/USD"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["rates"]["VND"]
    return None
exchange_rate = load_exchange_rate()
if exchange_rate:
    st.metric(
        label="1 USD",
        value=f"{exchange_rate:,.0f} VND"
    )
    st.caption("Tự động cập nhật mỗi 10 giây")
    usd_amount = st.number_input(
        "Nhập số USD",
        min_value=1.0,
        value=1.0,
        step=1.0
    )
    vnd_value = usd_amount * exchange_rate
    st.success(
        f"{usd_amount:,.2f} USD = {vnd_value:,.0f} VND"
    )
else:
    st.error("Không thể tải tỷ giá.")

#History data
st.header("Lịch sử USD/VND qua các năm ")
history_data = {
    "Năm": [1985, 1990, 1995, 2000, 2005, 2010,
            2015, 2020, 2023, 2024, 2025, 2026 ],

    "Tỷ giá": [15, 6500, 11000, 14000, 15800, 19000,
               22500, 23200, 23800, 25000, 26000, 26300],

    "Nhận xét": [
        "Sau đổi tiền",
        "Lạm phát rất cao",
        "Bắt đầu ổn định hơn",
        "Kinh tế mở cửa mạnh",
        "Tăng chậm",
        "Ap lực phá giá VND",
        "USD mạnh lên toàn cầu",
        "Khá ổn định",
        "USD tăng mạnh hậu COVID",
        "VND mất giá khá nhanh",
        "Lập đỉnh mới",
        "Dao động quanh 26.3k"
    ]        
}

df = pd.DataFrame(history_data)
st.dataframe(df, use_container_width=True)

#Table
st.subheader("Biểu đồ mất giá của VND")
chart_df = df.set_index("Năm")
st.line_chart(chart_df["Tỷ giá"])

#Analysis
st.header("Nhận xét xu hướng")
st.markdown("""
# Giai đoạn từ 1985 đến 1995
- VND mất giá cực mạnh do lạm phát cao
- Sau khi đổi tiền, tỷ giá tăng cao từ khoảng 15 lên hơn 11000VND/USD
            
# giai đoạn từ 2000 - 2015
- Việt Nam mở cửa kinh tế mạnh hơn
- Tỷ giá tăng chậm nhưng liên tục
- Ap lực phá giá sau khủng hoảng tài chính
            
# Giai đoạn từ 2020 - 2026
- USD mạnh lên toàn cầu sau covid
- FEE tăng lãi suất khiến VND chịu áp lực
- Tỷ giá vượt mốc 26.000 vnd/usd năm 2025
""")
# total devaluation
start_rate = df["Tỷ giá"].iloc[0]
end_rate = df["Tỷ giá"].iloc[-1]

increase = end_rate / start_rate
st.warning(
    f"Từ 1985 đến 2026, USD tăng khoảng {increase:,.0f} lần so với VND"
)

df = pd.DataFrame(history_data)

#hiển thị dữ liệu
st.subheader("Dữ liệu tỷ giá USD/VND")
st.dataframe(df, use_container_width=True)

st.header("Lịch sử giá bạc thế giới qua các năm")
silver_data = {
    "Năm" : [1985, 1990, 1995, 2000, 2005, 2010,
             2015, 2020, 2023, 2024, 2025, 2026],
    "Giá bạc (USD/oz)": [
        6.0, 5.0, 5.2, 5.0, 7.3, 20.2,
        15.7, 20.5, 25.0, 35.0, 55.0, 67.75
    ],
    "Nhận xét": [
        "Giai đoạn giá thấp",
        "Ổn định",
        "Đi ngang",
        "Vùng đáy dài hạn",
        "Bắt đầu tăng",
        "Bùng nổ sau khủng hoảng",
        "Điều chỉnh",
        "Hồi phục mạnh",
        "Nhu cầu công nghiệp tăng",
        "Xu hướng tăng mạnh",
        "Phá đỉnh nhiều năm",
        "Lập đỉnh mới"
    ]
}

df = pd.DataFrame(silver_data)
st.dataframe(df, use_container_width=True)
#Biểu đồ
st.subheader("Biểu đồ bạc thế giới ")

chart_df = df.set_index("Năm")
st.line_chart(chart_df["Giá bạc (USD/oz)"])
#Phân tích về xu hướng
st.header("Nhận xét xu hướng")

st.markdown("""
# Giai đoạn từ 1985 - 2005
-Gía bạc duy trì ở vùng thấp trong nhiều năm
-Nguồn cung khá dồi dào
-Nhu cầu công nghiệp chưa bùng nổ
            
# Giai đoạn 2005 - 2015
-Khủng hoảng tài chính 2008 thúc đẩy nhu cầu tài sản trú ẩn
-Gía bạc tăng mạnh từ 7 USD lên hơn 20 USD/OZ
-Có thời điểm vượt 40 USD/OZ trong năm 2011
            
# Gai đoạn 2020 - 2026
-Chính sách tiền tệ nới lỏng hậu covide
-Nhu cầu sản xuất pin mặt trời và điện tử tăng cao
-Bạc trở thành kim loại hưởng lại từ xu hướng năng lượng xanh
-Duy trì giá trên vùng 30 USD/OZ
""")
# Tính mức tăng
start_price = df["Giá bạc (USD/oz)"].iloc[0]
end_price = df["Giá bạc (USD/oz)"].iloc[-1]

st.success(
    f"từ 1985 đến 2026, giá bạc tăng khoảng {increase:.1f} lần"
)

st.header("Lịch sử giá vàng Việt Nam (1985-2026)")
history_data = {
    "Năm": [
        1985, 1990, 1995, 2000,
        2005, 2010, 2015, 2020,
        2021, 2022, 2023, 2024,
        2025, 2026
    ],
    #đơn vị VNĐ/lượng
    "Giá vàng": [
        15_000,
        500_000,
        5_200_000,
        7_000_000,
        8_700_000,
        26_500_000,
        35_000_000,
        56_000_000,
        61_000_000,
        67_000_000,
        74_000_000,
        85_000_000,
        95_000_000,
        191_000_000
    ],
    "Nhận xét" : [
        "ước tính thời bao cấp",
        "Lạm phát cao",
        "Thị trường ổn định hơn",
        "Kinh tế tăng trưởng",
        "Tăng chậm",
        "Chu kì tăng mạnh",
        "Ôn định quanh 35 triệu",
        "Covid-19",
        "Duy trì mức cao",
        "Tiếp tục tăng",
        "Biến động mạnh",
        "Lập mặt bằng giá mới",
        "Tiếp tục tăng",
        "Có thời điểm gần 191 triệu",
    ]
}

gold_df = pd.DataFrame(history_data)
#Hiển thị bảng giá
st.dataframe(gold_df, use_container_width=True)

# Biểu đồ
st.subheader("Biểu đồ giá vàng qua các năm")
G_chart_df = gold_df.copy()
G_chart_df["Giá vàng (triệu đồng/lượng)"] = (
    G_chart_df["Giá vàng"] / 1_000_000
)
st.line_chart(
    G_chart_df.set_index("Năm")["Giá vàng (triệu đồng/lượng)"]
)

#Thống kê
st.subheader("Thống kê nhanh")
col1, col2, col3 = st.columns(3)
price_1985 = gold_df.iloc[0]["Giá vàng"]
price_2026 = gold_df.iloc[-1]["Giá vàng"]

with col1:
    st.metric(
        "Giá năm 1985",
        f"{price_1985:,.0f} VNĐ/lượng",
    )

with col2:
    st.metric(
        "Giá năm 2026",
        f"{price_2026/1_000_000:.1f} triệu VNĐ/lượng",
    )
with col3:
    growth = price_2026/price_1985
    st.metric(
        "Tăng so với 1985",
        f"{growth:,.0f} lần"
    )
#phân tích
st.header("Nhận xét xu hướng")
st.markdown("""
# Giai đoạn từ 1985 - 1995
- Gía vàng còn ở mức thấp theo mặt bằng tiền tệ thời kì bao cấp và đầu thời kì đổi mới
- Lạm phát cao khiến sức mua và giá trị đồng tiền biến động mạnh
- Các số liệu giai đoạn này chủ yếu mang tính chất tham khảo
            
# Giai đoạn từ 2000 - 2010
- Gía vàng tăng dần cùng với sự phát triển của nền kinh tế
- Anh hưởng từ xu hướng tăng của thị trường vàng thế giới

# Giai đoạn từ 2010 - 2020
- Gía vàng tăng mạnh do khủng hoảng tài chính toàn cầu và nhu cầu tích trữ tăng mạnh
- Năm 2020 ghi nhận mức tăng đáng kể trong bối cảnh đại dịch covid-19

# Giai đoạn từ 2021 - 2026
- Gía vàng tiếp tục duy trì ở mức cao do lạm phát, bất ổn địa chính trị và nhu cầu trú ẩn an toàn        
- Năm 2026 giá vàng trong nước có thời điểm lên sát 191 triệu đồng/lượng, phản ánh mức độ biến động rất lớn.
            
""")