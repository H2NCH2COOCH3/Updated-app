import streamlit as st
import feedparser

@st.cache_data()
def load_news():
    return feedparser.parse("https://vnexpress.net/rss/tin-moi-nhat.rss")
@st.cache_data()
def load_news_gold():
    return feedparser.parse("https://vietnamnet.vn/rss/kinh-doanh.rss")

#menu = st.selectbox("Chọn chức năng mà bạn muốn dùng: ",["📰 Đọc báo","Giá vàng"])
tab1, tab2 = st.tabs(["📰 Đọc báo", "Giá vàng"])
with tab1:
    st.header("Tin tức mới nhất trên VnExpress")
    feed = load_news()
    for entry in feed.entries[:10]:
        st.subheader(entry.title)
        st.write(entry.published)
        st.write(entry.link)
with tab2:
    st.header("Cập nhật giá vàng từ Vietnamnet")
    feet = load_news_gold()
    gold_news = [entry for entry in feet.entries if "vàng" in entry.title.lower() or "giá vàng" in entry.summary.lower()]
    if gold_news:
        for entry in gold_news[:5]:
            st.subheader(entry.title)
            st.write(entry.published)
            st.write(entry.link)
    else:
        st.info("Không tìm thấy tin tức về giá vàng.")