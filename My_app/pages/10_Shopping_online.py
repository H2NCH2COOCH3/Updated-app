import streamlit as st
st.set_page_config(page_title="Vương quốc mô hình", page_icon=":sparkles")

with st.sidebar:
    st.title("Vương quốc mô hình")
    st.header("Chào mừng bạn đến với vương quốc mô hình")
    st.image("https://www.ffcollectibles.com.au/cdn/shop/products/G5STUDIOHIGHENDCUSTOMSERIESTHELIFEOFNARUTOUZUMAKI_2.jpg?v=1689176734&width=823")
    st.write("""Chúng tôi chuyên bán các mô hình nhân vật hoạt hình chất lượng. Luôn cập nhật và đa dạng sản phẩm
cam kết sự hài lòng của khách hàng với dịch vụ chuyên nghiệp. Hãy đến và khám phá thế giới mô hình
tại Vương quốc mô hình
""")
    st.write(":house: Địa chỉ cửa hàng")
    st.write(":phone: Điện thoại liên hệ")

st.title("Vương quốc mô hình")
col1, col2, col3 = st.columns(3)

with col1:
    b1 = st.button("Dragon Ball")

with col2:
    b2 = st.button("Naruto")

with col3:
    b3 = st.button("One Piece")

if b1:
    st.header("Danh sách mô hình dragon Ball")
    col4, col5, col6 = st.columns(3)
    with col4:
        st.image("https://product.hstatic.net/200000707011/product/image_20250325193648_097a328052fe447185a678efbcf11e71_master.jpg",
                caption="Goku Ultra Instinct- Mã mô hình: 001")
    with col5:
        st.image("https://cdn2.weeboo.vn/2026/06/bbb39248-4457-4d28-a8fe-49c1d37f09ed_99dc79c82a9947d4935cb3e346ba3b01_master.jpg",
                caption="Vegeta Ultra Ego - Mã mô hình: 002")
    with col6:
        st.image("https://product.hstatic.net/200000707011/product/image_20240220210054_46c6e4c3075a428c974c3692d037c9e6_master.jpg",
                caption="Frieza - Mã mô hình: 003")
if b2:
    st.header("Danh sách mô hình Naruto")
    col4, col5, col6 = st.columns(3)

    with col4:
        st.image("https://www.ffcollectibles.com.au/cdn/shop/products/G5STUDIOHIGHENDCUSTOMSERIESTHELIFEOFNARUTOUZUMAKI_2.jpg?v=1689176734&width=823",
                 caption="Uzumaki - Mã mô hình: 001")

    with col5:
        st.image("https://cdn.hstatic.net/products/200000707011/image_2025-08-29_173725_779_065e1496c2524caf9ae09e24c04dfabc_master.jpg",
                 caption="Uchiha Sasuke - Mã mô hình: 002")

    with col6:
        st.image("https://pos.nvncdn.com/f625c0-33854/ps/20241220_mnfl8fhjHd.jpeg?v=1734685010",
                 caption="Hatake kakashi - Mã mô hình: 003")

if b3:
    st.header("Danh sách mô hình One Piece")
    col4, col5, col6 = st.columns(3)

    with col4:
        st.image("https://nguyenngocfigure.com/wp-content/uploads/2026/05/mo-hinh-one-piece-luffy-gear-5-nika-jimei-palace-anikingdom-1.jpg",
                 caption="Monkey D.Luffy - Mã mô hình: 001")

    with col5:
        st.image("https://product.hstatic.net/200000462939/product/436121273_411649725036756_6364554075504794175_n_86dd790994144b27a2aff5339c30ca21_master.jpg",
                 caption="Roronoa Zoro - Mã mô hình: 002")

    with col6:
        st.image("https://product.hstatic.net/200000707011/product/438937996_418765547570280_8491042640023264585_n_e45f0a1e21fb45faa427971f94e086b9_master.jpg",
                 caption="Vinsmoke sanji - Mã mô hình: 003")