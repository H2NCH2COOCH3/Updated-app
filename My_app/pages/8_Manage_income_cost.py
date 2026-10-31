import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

st.set_page_config(
    page_title="Quản lý chi tiêu cá nhân",
    layout="wide"
)

st.title("💰 Quản lý chi tiêu cá nhân")

st.markdown("""
Ứng dụng giúp:

- Ghi lại khoản thu
- Ghi lại khoản chi
- Thống kê
- Biểu đồ
- Xuất Excel
""")

# ==========================
# Session State
# ==========================

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "Ngày",
        "Loại",
        "Danh mục",
        "Số tiền",
        "Ghi chú"
    ])

# ==========================
# Sidebar
# ==========================

st.sidebar.header("➕ Thêm giao dịch")

date = st.sidebar.date_input(
    "Ngày",
    datetime.today()
)

transaction_type = st.sidebar.selectbox(
    "Loại",
    ["Thu", "Chi"]
)

category = st.sidebar.selectbox(
    "Danh mục",
    [
        "Ăn uống",
        "Đi lại",
        "Lương",
        "Mua sắm",
        "Giải trí",
        "Tiền điện",
        "Tiền nước",
        "Khác"
    ]
)

amount = st.sidebar.number_input(
    "Số tiền",
    min_value=0,
    step=1000
)

note = st.sidebar.text_input(
    "Ghi chú"
)

if st.sidebar.button("Lưu"):

    new_row = {
        "Ngày": str(date),
        "Loại": transaction_type,
        "Danh mục": category,
        "Số tiền": amount,
        "Ghi chú": note
    }

    st.session_state.data = pd.concat(
        [
            st.session_state.data,
            pd.DataFrame([new_row])
        ],
        ignore_index=True
    )

    st.success("Đã lưu giao dịch!")

# ==========================
# Data
# ==========================

df = st.session_state.data

st.header("📋 Danh sách giao dịch")

st.dataframe(
    df,
    use_container_width=True
)

# ==========================
# Xóa giao dịch
# ==========================

st.header("🗑 Xóa giao dịch")

if len(df) > 0:

    row = st.selectbox(
        "Chọn dòng cần xóa",
        df.index
    )

    if st.button("Xóa giao dịch"):

        st.session_state.data = (
            st.session_state.data
            .drop(row)
            .reset_index(drop=True)
        )

        st.success("Đã xóa thành công!")
        st.rerun()

# ==========================
# Bộ lọc
# ==========================

st.header("🔍 Bộ lọc")

col1, col2 = st.columns(2)

with col1:

    filter_type = st.selectbox(
        "Loại",
        ["Tất cả", "Thu", "Chi"]
    )

with col2:

    categories = ["Tất cả"] + list(df["Danh mục"].unique())

    filter_category = st.selectbox(
        "Danh mục",
        categories
    )

filtered_df = df.copy()

if filter_type != "Tất cả":
    filtered_df = filtered_df[
        filtered_df["Loại"] == filter_type
    ]

if filter_category != "Tất cả":
    filtered_df = filtered_df[
        filtered_df["Danh mục"] == filter_category
    ]

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ==========================
# Thống kê
# ==========================

income = filtered_df[
    filtered_df["Loại"] == "Thu"
]["Số tiền"].sum()

expense = filtered_df[
    filtered_df["Loại"] == "Chi"
]["Số tiền"].sum()

balance = income - expense

st.header("📊 Thống kê")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Tổng thu",
    f"{income:,.0f} VNĐ"
)

c2.metric(
    "Tổng chi",
    f"{expense:,.0f} VNĐ"
)

c3.metric(
    "Số dư",
    f"{balance:,.0f} VNĐ"
)

# ==========================
# Biểu đồ
# ==========================

st.header("📈 Chi tiêu theo danh mục")

expense_df = filtered_df[
    filtered_df["Loại"] == "Chi"
]

if len(expense_df):

    chart = expense_df.groupby(
        "Danh mục"
    )["Số tiền"].sum()

    st.bar_chart(chart)

else:

    st.info("Chưa có dữ liệu.")

# ==========================
# Chi tiêu theo ngày
# ==========================

st.header("📅 Chi tiêu theo ngày")

if len(filtered_df):

    daily = filtered_df.groupby(
        "Ngày"
    )["Số tiền"].sum()

    st.line_chart(daily)

# ==========================
# Export Excel
# ==========================

st.header("📥 Xuất Excel")

option = st.radio(
    "Chọn dữ liệu muốn xuất",
    ["Toàn bộ", "Dữ liệu đã lọc"]
)

if option == "Toàn bộ":
    export_df = st.session_state.data
else:
    export_df = filtered_df



def convert_excel(data):

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:

        # Sheet dữ liệu
        data.to_excel(
            writer,
            sheet_name="Danh sach giao dich",
            index=False
        )

        # Tính thống kê
        income = data[data["Loại"] == "Thu"]["Số tiền"].sum()
        expense = data[data["Loại"] == "Chi"]["Số tiền"].sum()
        balance = income - expense

        summary = pd.DataFrame({
            "Chỉ tiêu": [
                "Tổng giao dịch",
                "Tổng thu",
                "Tổng chi",
                "Số dư"
            ],
            "Giá trị": [
                len(data),
                income,
                expense,
                balance
            ]
        })

        # Sheet thống kê
        summary.to_excel(
            writer,
            sheet_name="Thong ke",
            index=False
        )

    return output.getvalue()


excel = convert_excel(export_df)

st.download_button(
    "📄 Tải Excel",
    excel,
    "chi_tieu.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)