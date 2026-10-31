import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import feedparser
import numpy as np
import time
import matplotlib.pyplot as plt
import random
import time
#===================  CSS LÀM ĐẸP GIAO DIỆN  ====================
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #e3fdfd, #cbf1f5);
}

.sidebar .sidebar-content {
    background: linear-gradient(180deg, #00b4d8, #0096c7);
    color: white;
}

h1, h2, h3, h4 {
    color: #0077b6 !important;
}

.stTabs [data-baseweb="tab"] {
    font-size: 18px;
    padding: 12px;
}

.stTabs [data-baseweb="tab-highlight"] {
    background: #90e0ef !important;
    color: black !important;
}

.stButton>button {
    background-color: #48cae4;
    color: black;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
    transition: 0.3s;
}
.stButton>button:hover {
    background-color: #0096c7;
    color: white;
    transform: scale(1.05);
}

.card {
    background: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 12px;
}

a {
    text-decoration: none;
    color: #0077b6 !important;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)
st.title("🎧 Ứng dụng giải trí và sức khỏe")



menu = st.selectbox("Chọn chức năng mà bạn muốn dùng: ",["🎤 MV yêu thích", "📰 Đọc báo","Giá vàng", "Kiểm tra sức khoẻ","Kiểm tra tính cách theo DISC","Nhân tướng học","Nhắc nhở nghỉ ngơi và tập thể dục","Ứng dụng theo dõi sức khoẻ nâng cao","Game"])
if menu == '🎤 MV yêu thích':
    st.sidebar.title("🎶 Danh sách nghệ sĩ")
    selected_artist = st.sidebar.radio("Chọn nghệ sĩ:", ["Đen Vâu", "Hà Anh Tuấn", "Sơn Tùng M-TP"])

    videos = {
        "Đen Vâu": [
            ("Bữa ăn cho em", "https://www.youtube.com/watch?v=ukHK1GVyr0I"),
            ("Mang tiền về cho mẹ", "https://www.youtube.com/watch?v=UVbv-PJXm14"),
            ("Trời hôm nay nhiều mây cực!", "https://www.youtube.com/watch?v=MBaF0l-PcRY"),
            ("Hai triệu năm", "https://www.youtube.com/watch?v=LSMDNL4n0kM")
        ],
        "Hà Anh Tuấn": [
            ("Tuyết rơi mùa hè", "https://www.youtube.com/watch?v=pTh3KCD7Euc"),
            ("Nước ngoài", "https://www.youtube.com/watch?v=pU3O9Lnp-Z0"),
            ("Tháng tư là lời nói dối của em", "https://www.youtube.com/watch?v=UCXao7aTDQM"),
            ("Xuân thì", "https://www.youtube.com/watch?v=3s1r_g_jXNs")
        ],
        "Sơn Tùng M-TP": [
            ("Lạc trôi", "https://www.youtube.com/watch?v=Llw9Q6akRo4"),
            ("Chúng ta không thuộc về nhau", "https://www.youtube.com/watch?v=qGRU3sRbaYw"),
            ("Muộn rồi mà sao còn", "https://www.youtube.com/watch?v=xypzmu5mMPY"),
            ("Hãy trao cho anh", "https://www.youtube.com/watch?v=knW7-x7Y7RE")
        ]
    }
    st.header(f"Các bài hát của {selected_artist} 🎵")
    for title, url in videos[selected_artist]:
        st.subheader(title)
        st.video(url)
elif menu == '📰 Đọc báo':
    st.header("Tin tức mới nhất trên VnExpress")
    feed = feedparser.parse("https://vnexpress.net/rss/tin-moi-nhat.rss")
    for entry in feed.entries[:10]:
        st.subheader(entry.title)
        st.write(entry.published)
        st.write(entry.link)
elif menu == 'Giá vàng':
    st.header("Cập nhật giá vàng từ Vietnamnet")
    feet = feedparser.parse("https://vietnamnet.vn/rss/kinh-doanh.rss")
    gold_news = [entry for entry in feet.entries if "vàng" in entry.title.lower() or "giá vàng" in entry.summary.lower()]
    if gold_news:
        for entry in gold_news[:5]:
            st.subheader(entry.title)
            st.write(entry.published)
            st.write(entry.link)
    else:
        st.info("Không tìm thấy tin tức về giá vàng.")
elif menu == 'Kiểm tra sức khoẻ':
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Kiểm tra chỉ số BMI của bạn",
    "🔮 Dự đoán giờ ngủ mỗi đêm",
    "Kiểm tra nhịp tim xem có nên gặp bác sĩ không",
    "Lượng nước uống khuyến nghị mỗi ngày",
    "Kiểm tra số bước đi nên đi mỗi ngày"])
    with tab1:
        st.header("Kiểm tra chỉ số BMI của bạn ")
        can_nang = st.number_input("Nhập cân nặng của bạn (kg)", min_value=10.0,max_value=200.0,value=60.0,step=0.1)
        chieu_cao = st.number_input("Nhập chiều cao của bạn (m)",min_value=1.0,max_value=2.5,value=1.7,step=0.01)
        bmi_min = 18.5
        can_nang_min = bmi_min*(chieu_cao**2)
        can_nang_tang = can_nang_min - can_nang
        bmi_max = 24.9
        can_nang_max = bmi_max*(chieu_cao**2)
        can_nang_giam = can_nang - can_nang_max
        if st.button("Tính BMI"):
            bmi =   can_nang/(chieu_cao ** 2)
            st.success(f"chỉ số bmi của bạn là: {bmi: .2f}")
            if bmi < 18.5:
                st.warning("Bạn đang thiếu cân, nên ăn uống đầy đủ và dinh dưỡng hơn.")
                st.info(f"Bạn cần tăng số kg là: {can_nang_tang: .2f}")
            elif 18.5 <= bmi < 25:
                st.info("Bạn có cân nặng bình thường. Hãy tiếp tục duy trì lối sống lành mạnh.")
            elif 25 <= bmi < 30:
                st.warning("Bạn đang thừa cân. Nên cân đối chế độ ăn và tập thể dục.")
                st.info(f"Bạn cần giảm số kg là: {can_nang_giam: .2f}")
            else:
                st.error("Bạn đang béo phì. Nên gặp chuyên gia dinh dưỡng hoặc bác sĩ để được tư vấn.")
                st.info(f"Bạn cần giảm số kg là: {can_nang_giam: .2f}")
    with tab2:
        st.header("🔮 Dự đoán giờ ngủ mỗi đêm")
        x = [
                [10, 1, 8],
                [20, 5, 6],
                [25, 8, 3],
                [30, 6, 5],
                [35, 2, 9],
                [40, 4, 3]
            ]
        y = [10, 8, 6, 7, 9.5, 9]
        model = LinearRegression()
        model.fit(x, y)
        st.write("Nhập thông tin cá nhân:")
        age = st.number_input("Tuổi của bạn", min_value=5, max_value=100, value=25)
        activity = st.slider("Mức độ hoạt động thể chất (1 = ít, 10 = rất nhiều)", 1, 10, 5)
        screen_time = st.number_input("Thời gian dùng màn hình mỗi ngày (giờ)", min_value=0, max_value=24, value=6)

        if st.button("💤 Dự đoán ngay"):
            input_data = [[age, activity, screen_time]]
            result = model.predict(input_data)[0]
            st.success(f"Bạn nên ngủ khoảng {result:.1f} giờ mỗi đêm")

            if result < 6.5:
                st.warning("😴 Có thể bạn cần nghỉ ngơi nhiều hơn để cải thiện sức khỏe.")
            elif result > 9:
                st.info("😅 Có thể bạn đang vận động nhiều – ngủ bù hợp lý nhé.")
            else:
                st.success("✅ Lượng ngủ lý tưởng! Hãy giữ thói quen tốt nhé.")
    with tab3:
        st.header("Kiểm tra nhịp tim xem có nên gặp bác sĩ không ")
        x = np.array([
            # Trẻ em
            [100, 2, 12],
            [95, 4, 15],
            [90, 6, 18],
            [85, 9, 20],
            [80, 12, 25],

            # Người lớn
            [75, 20, 50],
            [72, 30, 65],
            [70, 40, 70],
            [68, 50, 75],
            [66, 58, 78],

            # Người cao tuổi
            [70, 65, 70],
            [75, 70, 68],
            [80, 75, 65],
            [85, 80, 60],
            [90, 85, 58],
        ])
        y = np.array([
            # Trẻ em - rủi ro thấp đến vừa
            1.2, 1.3, 1.5, 1.6, 1.7,

            # Người lớn - rủi ro trung bình
            2.0, 2.3, 2.7, 3.0, 3.2,

            # Người cao tuổi - rủi ro cao dần
            3.5, 3.8, 4.0, 4.3, 4.6
        ])
        model = LinearRegression()
        model.fit(x,y)
        st.subheader("Nhập thông tin sức khoẻ ")
        
        hr = st.number_input("Nhịp tim (bm) ", min_value=40,max_value=200,value=75)
        age = st.number_input("Tuổi ",min_value=1,max_value=120,value=30)
        weight = st.number_input("Cân Nặng (kg) ",min_value=10.0,max_value=200.0,value=60.0)
        if st.button("Kiểm tra sức khoẻ"):
            score = model.predict([[hr,age,weight]])[0]
            st.success(f"chỉ số rủi ro: **{score: .2f}**")
            if age<13:
                safe_threshold = 1.5
            elif age<60:
                safe_threshold = 2.0
            else: 
                safe_threshold = 2.5
            if score < safe_threshold:
                st.info("Bạn khoẻ mạnh và không cần đi bác sĩ ")
            elif score <(safe_threshold + 1):
                st.warning("Cần theo dõi thêm, hãy nghỉ ngơi và kiểm tra lại sau ")
            elif score <(safe_threshold + 2):
                st.warning("Có dấu hiệu bất thường cần hỏi thêm ý kiến bác sĩ ")
            else:
                st.error("Rủi ro cao, nên gặp bác sĩ càng sớm càng tốt")
    with tab4:
        st.header("Lượng nước uống khuyến nghị mỗi ngày")
        st.title("Bạn nên uống bao nhiêu lít nước mỗi ngày?")
        age3 = st.number_input("Nhập tuổi của bạn:", min_value=0.0, max_value=120.0, value=18.0, step=1.0)
        if st.button("Kiểm tra số lít nước khuyến nghị"):
            if age3 < 4:
                st.info("Bạn nên uống **1.3 lít nước** mỗi ngày.")
            elif 4<= age3 <=8:
                st.info("Bạn nên uống **1.7 lít nước** mỗi ngày.")
            elif 9<= age3 <=13:
                st.info("Bạn nên uống **2.1-2.4 lít nước** mỗi ngày.")
            elif 14<= age3 <=18:
                st.info("Bạn nên uống **2.3-3.3 lít nước** mỗi ngày.")
            elif 19<= age3 <=50:
                st.warning("Bạn nên uống **2.7 lít nước(nữ)/3.3 lít nước(nam)** mỗi ngày.")
            else:
                st.error("Bạn nên uống **2.5-3.0 lít nước** mỗi ngày tuỳ vào sức khoẻ và hoạt động.") 
    with tab5:
        st.header("Kiểm tra số bước đi nên đi mỗi ngày")
        st.title("Bạn nên đi bao nhiêu bước mỗi ngày?")
        age2 = st.number_input("Nhập tuổi của bạn:", min_value=0.0, max_value=130.0, value=18.0, step=1.0)
        if st.button("Kiểm tra số bước"):
            if age2 < 18:
                st.info("Bạn nên đi **12000-15000 bước** mỗi ngày.")
            elif 18 <=age2 <= 39:
                st.info(" + Bạn nên đi **8000-10000 bước** mỗi ngày.")
            elif 40 <= age2 <= 64:
                st.warning("Bạn nên đi **7000-9000 bước** mỗi ngày.")
            elif age2 > 64:
                st.warning("Bạn nên đi **6000-8000 bước** mỗi ngày.")
            else:
                st.error("A Có lỗi xảy ra. Vui lòng kiểm tra lại thông tin.")
elif menu == 'Kiểm tra tính cách theo DISC':
    st.header("Kiểm tra tính cách theo DISC")
    st.markdown("Chọn một mô tả đúng nhất và một mô tả ít đúng nhất trong từng nhóm")
    groups = [
        {
            "D": "Tôi quyết đoán và thích kiểm soát",
            "I": "Tôi thích thân thiện và nói chuyện dễ dàng",
            "S": "Tôi kiên nhẫn và đáng tin cậy",
            "C": "Tôi chính xác và có hệ thống",
        },
        {
            "D": "Tôi thích thử thách và hành động nhanh",
            "I": "Tôi tràn đầy năng lượng và lạc quan",
            "S": "Tôi ổn định và hỗ trợ người khác",
            "C": "Tôi làm việc theo quy tắc rõ ràng",
        },
        {
            "D": "Tôi thích kiểm soát kết quả",
            "I": "Tôi thích được công nhận",
            "S": "Tôi ưu tiên sự hài hoà",
            "C": "Tôi chú ý đến việc chi tiết và phân tích",
        }
    ]
    scores = {"D": 0, "I":0, "S": 0, "C": 0 }
    for idx , group in enumerate(groups):
        st.markdown(f"### nhóm {idx + 1}")
        options = list(group.values())
        keys = list(group.keys())
        most = st.radio("Mô tả đúng nhất với bạn ", options, key = f"most_{idx}")
        least = st.radio("Mô tả ít đúng nhất với bạn ", options, key=f"least_{idx}")
        for key, val in group.items():
            if val == most:
                scores[key] += 1
            if val == least:
                scores[key] -= 1
    if st.button("Xem kết quả DISC "):
        st.header(" Kết quả của bạn ")
        max_type = max(scores, key = scores.get)

        for style, score in scores.items():
            st.write(f"{style}: {score} điểm ")
        st.markdown(f"Tính nổi bật nhất của bạn là: {max_type}**")
        descriptions = {
            "D": "Quyết đoán, định hướng kết quả và thích kiểm soát",
            "I": "Giao tiếp tốt, tràn đầy năng lượng và truyền cảm hứng",
            "S": "Kiên nhẫn, đáng tin cậy và hỗ trợ người khác",
            "C": "Chính xác, tuân thủ quy trình và thích phân tích logic"
        } 
        st.info(descriptions[max_type])
        st.markdown("----")
        st.markdown("Mô tả chi tiết các nhóm DISC")
        st.markdown("""
            - **D (Dominance)**: Người lãnh đạo, chủ động, thích cạnh tranh. Ví dụ: CEO, nhà sáng lập.  
            - **I (Influence)**: Người truyền cảm hứng, thích giao tiếp, có sức hút. Ví dụ: người làm marketing, diễn giả.  
            - **S (Steadiness)**: Người hỗ trợ, trung thành, kiên nhẫn. Ví dụ: giáo viên, điều dưỡng.  
            - **C (Conscientiousness)**: Người phân tích, tỉ mỉ, theo quy trình. Ví dụ: kế toán, kỹ sư.
        """)
        st.caption("Đây chỉ là bài tham khảo về chỉ số DISC")
elif menu == "Nhân tướng học":
    st.header("Phân tích tướng mặt theo ngũ hành")
    st.markdown("Chọn các đặc điểm bạn cảm thấy đúng với gương mặt của mình")
    st.subheader("Đôi mắt")
    eyes_good = st.multiselect("Đặc điểm tốt về đôi mắt: ",[
        "Mắt sáng và có thần (Tư duy nhanh nhạy, có năng lực tích cực)",
        "Mắt dài và đều (tầm nhìn chiến lược và có nội tâm sâu sắc)",
        "Mắt cười (dễ gần, thân thiện và giao tiếp tốt)"
    ])
    eyes_bad = st.multiselect("Đặc điểm chưa tốt về mắt: ",[
        "Mắt lờ đờ, thiêu thần (thiếu sinh khí và mệt mỏi)",
        "Mắt không cân xứng (thiếu cân bằng và cảm giác nhìn yếu)",
        "Tròng trắng lẫn tròng đen (dễ gặp bất ổn, tâm lý dao động)"
    ])
    st.subheader("Mũi")
    nose_good = st.multiselect("Đặc điểm tốt về mũi: ", [
        "Mũi cao thẳng và đầy đặn (tài vận tốt lập nghiệp dễ dàng)",
        "Cánh mũi dày, đều (Biết giữ tiền và quản lý tài chính tốt)",
        "Đầu mũi tròn đầy (Ham học hỏi, lòng bao dung, nhân hậu)"
    ])
    nose_bad = st.multiselect("Đặc điểm chưa tốt về mũi: ", [
        "Mũi lệch (tính cách thiếu ổn định)",
        "Mũi hếch (khó giữ tài sản, hay tiêu xài)",
        "Cánh mũi mỏng (tài chính bấp bênh)"
    ])
    st.subheader("Trán")
    forehead_good = st.multiselect("Đặc điểm tốt về trán: ", [
        "Trán cao và rộng (Thông minh, tư duy logic)",
        "Trán đầy đặn, trơn láng (sự nghiệp tốt, thuận lợi)",
        "Không có nếp nhăn sớm (suy nghĩ tích cực ổn định)"
    ])
    forehead_bad = st.multiselect("Đặc điểm chưa tốt về trán: ",[
        "Trán thấp và hẹp (tầm nhìn hạn chế)",
        "Trán nghiêng (thiếu kiên định)",
        "Trán lõm (dễ bị chi phối thiếu quyết đoán)"
    ])
    st.subheader("Tai")
    ears_good = st.multiselect("Đặc điểm tốt về tai: ", [
        "Tai đầy, vành rõ (sức khoẻ tốt, có phúc khí)",
        "Dái tai dày (hậu vận vững vàng)",
        "Tai cao hơn chân mày (tư duy tốt, trí tuệ sáng)"
    ])
    ears_bad = st.multiselect("Đặc điểm chưa tốt về tai: ", [
        "Tai mỏng như giấy (yếu vận, dễ bị ảnh hưởng)",
        "Tai vểnh ra bên ngoài (nóng bỏng, bốc đồng)",
        "Tai thấp hơn lông mày (thiếu tư duy chiến lược)"
    ])
elif menu == "Nhắc nhở nghỉ ngơi và tập thể dục":
    st.subheader("Nhắc nhở nghỉ ngơi và tập thể dục")
    minutes = st.number_input("Nhập số phút làm việc: ",min_value=1,step=1,value=1)
    if st.button("Bắt đầu đếm ngược"):
        st.info(f"Bắt đầu đếm ngược {minutes} phút")
        my_bar = st.progress(0)
        total_seconds = minutes * 60
        for sec in range(total_seconds):
            percent = int(((sec+1)/total_seconds)*100)
            my_bar.progress(percent)
            time.sleep(1)
        st.success("Hết giờ rồi! Hãy đứng dậy nghỉ ngơi và tập vài động tác nhé!")
        audio_file = open("alarm.mp3","rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes,format="audio/mp3",start_time=0)
elif menu == "Ứng dụng theo dõi sức khoẻ nâng cao":
    st.set_page_config(page_title="Ứng dụng Sức Khoẻ Nâng Cao",layout="centered")
    st.title("Ứng dụng Theo Dõi Sức Khoẻ Nâng Cao")
    st.header("Nhập thông tin cá nhân")
    name = st.text_input("Họ và tên:")
    age = st.number_input("Tuổi:",min_value=0,max_value=120,step=1)
    gender = st.radio("Giới tính:",("Nam","Nữ"))
    height = st.number_input("Chiều cao (cm):",min_value=50.0,max_value=250.0,step = 0.1)
    weight = st.number_input("Cân nặng (kg):",min_value=10.0,max_value=250.0,step = 0.1)
    activity_level= st.selectbox("Mức độ hoạt động thể chất:",[
        "Ít vận động",
        "Vận động nhẹ (1-3 buổi/tuần)",
        "Vận động vừa (3-5 buổi/tuần)",
        "Vận động nhiều (6-7 buổi/tuần)",
        "Vận động rất nhiều (2 lần/ngày)"
    ])
    if st.button("Phân tích sức khoẻ"):
        if height>0 and weight>0:
            height_m = height/100
            bmi = weight/(height_m**2)
            if gender == "Nam":
                bmr = 10*weight+6.25*height-5*age+5
            else:
                bmr = 10*weight+6.25*height-5*age-161
            activity_factors = {
                "Ít vận động": 1.2,
                "Vận động nhẹ (1-3 buổi/tuần)":1.375,
                "Vận động vừa (3-5 buổi/tuần)":1.55,
                "Vận động nhiều (6-7 buổi/tuần)":1.725,
                "Vận động rất nhiều (2 lần/ngày)":1.9
            }
            activity_factor = activity_factors[activity_level]
            tdee = bmr * activity_factor
            water_intake = weight *35/1000
            st.subheader("Kết quả phân tích")
            st.write(f"**Chào {name}!**")
            st.write(f"**Chỉ số BMI:** '{bmi:.2f}'")
            st.write(f"**BMR(Tỷ lệ trao đổi chất cơ bản):** '{bmr:.0f}' kcal/ngày")
            st.write(f"**TDEE(Năng lượng tiêu hao mỗi ngày):** '{tdee:.0f}' kcal/ngày")
            st.write(f"**Lượng nước nên uống mỗi ngày:** '{water_intake:.0f}' lít")
            st.markdown("### Đánh giá chỉ số BMI:")
            if bmi<18.5:
                st.warning(f"Bạn đang thiếu cân. Hãy tăng dinh dưỡng. Bạn nên tăng {round(((18.5 - bmi)*(height_m**2)),2)} kg")
            elif 18.5 <= bmi <24.9:
                st.success("Bạn có cân nặng bình thường. Duy trì chế độ sống lành mạnh!")
            elif 25<=bmi<29.9:
                st.warning(f"Bạn đang thừa cân. Hãy cân bằng lại chế độ ăn và hoạt động. Bạn nên giảm {round(((bmi - 24.9)*(height_m**2)),2)} kg")
            else:
                st.error(f"Bạn đang béo phì. Cần tham khảo chuyên gia để cải thiện sức khoẻ. Bạn nên giảm {round(((bmi - 24.9)*(height_m**2)),2)} kg")
            
            st.markdown("### Gợi ý chế độ ăn (Theo mục tiêu):")
            col1,col2 = st.columns(2)
            with col1:
                st.info("**Duy trì cân nặng:**")
                st.write(f"- Ăn khoảng '{tdee:.0f}' kcal/ngày")
            with col2:
                st.info("**Giảm cân nhẹ:**")
                st.write(f"- Ăn khoảng '{tdee-300:.0f}' kcal/ngày")
            st.markdown("### Gợi ý thực đơn mẫu:")
            st.markdown("""
            - **Sáng:** Trứng luộc, bánh mì nguyên cám, trái cây
            - **Trưa** Cơm gạo lứt, ức gà, rau luộc, canh
            - **Tối** Salad rau xanh, cá hấp, trái cây ít ngọt
            - **Snack:** Hạt khô,sữa chua ít đường
             """)

    st.header("Theo dõi sức khoẻ về nhịp tim")
    sys = st.number_input("Huyết áp tâm thu(mmhg): ",min_value=50, max_value = 250,step=1)
    dia = st.number_input("Huyết áp tâm trương(mmhg)",min_value=30,max_value=150,step=1)
    heart_rate = st.number_input("Nhịp tim khi nghỉ ngơi(bpm): ",min_value=30,max_value=200,step=1)
    if st.button("Phân tích tim mạch:"):
        st.subheader("Kết quả phân tích tim mạch")
        if sys<90 or dia<60:
            st.warning("Huyết áp thấp")
        elif 90<= sys <= 120 and 60<=dia<=80:
            st.success("Huyết áp bình thường")
        elif 120<=sys<=139 and 80<=dia<=89:
            st.warning("Tiền huyết áp")
        elif 140<=sys<=159 or 90<=dia<=99:
            st.error("Tăng huyết áp độ 1") 
        elif 160<=sys<=179 or 100<=dia<=109:
            st.error("Tăng huyết áp độ 2")
        else:
            st.error("Tăng huyết áp độ 3")         
        if heart_rate <60:
            st.warning("Nhịp tim chậm")
        elif 60<=heart_rate<=100:
            st.success("Nhịp tim bình thường")
        else:
            st.success("Nhịp tim cao")
        # ==========================
        # 📖 Lý thuyết nhịp tim theo độ tuổi
        # ==========================
        st.markdown("### 📖 Nhịp tim theo độ tuổi")
        st.markdown("""
        - Công thức nhịp tim tối đa: 220 - tuổi  
        - Vùng tập luyện hiệu quả: *50% - 85% nhịp tim tối đa*

        | Tuổi | Tối đa (bpm) | 50-85% (bpm) |
        |------|--------------|--------------|
        | 20   | 200          | 100 - 170    |
        | 30   | 190          | 95 - 162     |
        | 40   | 180          | 90 - 153     |
        | 50   | 170          | 85 - 145     |
        | 60   | 160          | 80 - 136     |
        | 70   | 150          | 75 - 128     |
        """)
    # 📖 Lý thuyết nhịp tim theo độ tuổi
        # ==========================
        st.markdown("### 📖 Nhịp tim theo độ tuổi")
        st.markdown("""
        - Công thức nhịp tim tối đa: `220 - tuổi`  
        - Vùng tập luyện hiệu quả: **50% - 85% nhịp tim tối đa**
        | Tuổi | Tối đa (bpm) | 50-85% (bpm) |
        |------|--------------|--------------|
        | 20   | 200          | 100 - 170    |
        | 30   | 190          | 95 - 162     |
        | 40   | 180          | 90 - 153     |
        | 50   | 170          | 85 - 145     |
        | 60   | 160          | 80 - 136     |
        | 70   | 150          | 75 - 128     |
        """)
        st.header("Phát triển chiều cao")

        if  age > 0:
            st.subheader("Phân tích tiềm năng phát triển chiều cao")
            if gender == "Nam":
                max_growth_age = 21
            else:
                max_growth_age = 19
            if age >= max_growth_age:
                st.info("""Ở độ tuổi hiện tại, khả năng tăng chiều cao tự nhiên gần như là không còn. 
                        Bạn nên tập luyện và bổ sung dinh dưỡng để giữ vóc dáng cân đối.
                        """)
            else:
                remaining_years = max_growth_age - age
                st.write(f"Bạn vẫn còn khoảng {remaining_years} năm để phát triển chiều cao tối ưu.")
                if activity_level == "Ít vận động":
                    growth_potential  = "Thấp"
                    st.warning("Mức độ vận động thấp có thể làm hạn chế phát triển chiều cao. Hãy cố gắng vận động nhiều hơn mỗi ngày.")
                elif activity_level == ["Vận động nhẹ (1-3 buổi/tuần)", "Vận động vừa (3-5 buổi/tuần)"]:
                    growth_potential  = "Trung bình"
                    st.info("Mức độ vận động khá tốt, bạn nên bổ sung thêm các bài tập kéo dãn hoặc thể thao ngoài trời để tối ưu phát triển.")
                else:
                    growth_potential = "cao"
                    st.success("Rất tốt! Mức độ vận động cao giúp kích thích hormone tăng trưởng, hỗ trợ phát triển chiều cao tối đa.")
                
                st.markdown(f"Tiềm năng phát triển chiều cao của bạn: {growth_potential}")
                st.markdown("Gợi ý phát triển chiều cao tối đa")
                with st.expander("Chế độ dinh dưỡng nên bổ sung"):
                    st.markdown("""
                        -**Protein:** Thịt nạc, cá, trứng, đậu phụ
                        -**Canxi:** Sữa, phô mai, sữa chua, cá hồi, rau xanh đậm 
                        -**Vitamin D:** Phơi nắng 15-20 phút hoặc ăn trứng, cá
                        -**Kẽm và Magie:** Có trong hải sản, các loại hạt, đậu, ngũ cốc nguyên hạt
                        -**Tránh:** Nước ngọt có gas, đồ ăn nhanh, đồ chiên rán nhiều mỡ
    """)
                with st.expander("Bài tập hỗ trợ phát triển chiều cao"):
                    st.markdown(""""
                        -**Tập hàng ngày:** Bơi lội, nhảy dây, bóng rổ, đu xà, yoga kéo giãn
                        -**Buổi sáng:** Kéo dãn cơ thể, vươn vai, hít thở sâu ngoài trời
                        -**Thói quen:** Giữ lưng thẳng khi ngồi và đứng, tránh gù lưng
                                """)
                with st.expander("Thói quen sinh hoạt và giấc ngủ"):
                    st.markdown("""
                        -Ngủ đủ 8-10 tiếng/ngày, đặc biệt ngủ từ 22h đến 6h sáng
                        -Hạn chế thức khuya, dùng điện thoại trước khi ngủ
                        -Uống đủ nước (theo khuyến nghị ở phần trên)
                        -Duy trì cân nặng hợp lý để không ảnh hưởng đến hormone tăng trưởng
    """)
                if gender == "Nam":
                    avg_height = 175
                else:
                    avg_height = 162
                potential_height = height + remaining_years * 0.8
                if potential_height > avg_height:
                    potential_height = avg_height + 2
                st.markdown(f"Chiều cao tiềm năng ước tính: {potential_height:.1f} cm")
        else:
            st.warning("Vui lòng nhập thông tin cá nhân ở phần đầu(tuổi, giới tính, chiều cao...) trước khi phân tích")
        st.header("Trợ lý AI - Tư vấn sức khoẻ thông tin")
        st.markdown("""
            Nhập câu hỏi hoặc yêu cầu để được AI gợi ý chế độ ăn, bài tập, hoặc cách cải thiện sức khoẻ dựa trên thông tin của bạn
    """)
        user_questions = st.text_area("Câu hỏi của bạn")
        if st.button("Hỏi AI"):
            if not name or age == 0 or height == 0 or weight == 0:
                st.warning("Vui lòng nhập đầy đủ thông tin cá nhân ở phần đầu trước khi hỏi AI")
            else:
                health_summary = f"""
                Thông tin người dùng:
                -Họ tên: {name}
                -Tuổi: {age}
                -Giới tính: {gender}
                -Chiều cao: {height} cm
                -Cân nặng: {weight} kg
                -Mức độ vận động: {activity_level}
                -BMI: {weight/((height/100)**2) : .2f}
    """ 

                st.info(" Gợi ý từ AI: ")
                st.markdown(f"""
                Dựa trên thông tin cá nhân của bạn (**{age} tuổi, {gender.lower()}, BMI {weight/((height/100)**2) : .2f}**),
                bạn nên:
                -Ăn cân đối bằng các nhóm chất(đạm, tinh bột, rau xanh, vitamin)
                -Uống khoảng **{weight * 35/1000 : .1f} lít nước / ngày
                -Tập luyện đều đặn {activity_level.lower()}
                -Ngủ đủ giấc 7 - 9 tiếng, tránh bị stress
    """)
    st.header("Dự đoán xu hướng cân nặng")
    st.markdown("Nhập dữ liệu dự đoán cân nặng gần đây để có thể dự đoán sau 30 ngày liên tiếp")
    num_entries = st.number_input("Bạn có bao nhiêu lần ghi nhận cân nặng gần đây ?", 2, 10, 5)
    weight = []
    days = []
    st.markdown("Nhập dữ liệu")
    for i in range(int(num_entries)):
        col1, col2 = st.columns(2)
        with col1:
            day = st.number_input(f"ngày thứ (tính từ khi bắt đầu theo dõi)- lần {i+1}: ",value=i*7)
        with col2:
            w = st.number_input(f"cân nặng (kg) lần {i+1}: ",value = 70 - i*0.3, step = 0.1)
        days.append(day)
        weight.append(w)
    if st.button("Dự đoán cân nặng sau 30 ngày "):
        x= np.array(days).reshape(-1,1)
        y= np.array(weight)

        model = LinearRegression()
        model.fit(x,y)
        future_day = np.array([[max(days) + 30]])
        predicted_weight = model.predict(future_day)[0]
        st.subheader("dự đoán kết quả ")
        st.write(f"cân nặng hiện tại: '{weight[-1]: .1f}' ")
        st.write(f"dự đoán sau 30 ngày: '{predicted_weight:.1f}' ")
        if predicted_weight < weight[-1]:
            st.success("xu hướng giảm cân tích cực ")
        elif predicted_weight > weight[-1]:
            st.warning("xu hướng tăng cân bạn cần xem lại chế độ ăn")
        else:
            st.info("cân nặng ổn định")
        
        future_x = np.append(days,max(days)+30)
        future_y = model.predict(future_x.reshape(-1,1))

        fig, ax = plt.subplots()
        fig.patch.set_facecolor("#f9f9f9")
        ax.plot(days,weight, 'o-', color = 'blue', label = "Dữ liệu thực tế")
        ax.plot(future_x,future_y, '--', color = 'orange', label = "Dự đoán(Linear regression)")
        ax.plot(future_day,predicted_weight, 'ro', label = "Dự đoán sau 30 ngày")
        for (x, y_val) in zip(days,weight):
            ax.text(x,y_val +0.1, f"{y_val:.1f}",ha="center",fontsize=8)
        ax.set_title("Xu hướng cân nặng và dự đoán 30 ngày tới")
        ax.set_xlabel("Ngày theo dõi")
        ax.set_ylabel("Cân nặng (kg)")
        ax.set_ylim(min(weight)-1, max(weight) + 1)
        ax.legend()
        ax.grid(True,linestyle = "--", alpha = 0.5)
        st.pyplot(fig)
    st.header("Thể hình và giảm cân thông minh")
    goal = st.selectbox(
        " Mục tiêu tập luyện của bạn: ",
        ["Giảm cân", "Giữ cân", "Tăng cơ"]
    )
    workout_days = st.slider("Bạn muốn tập bao nhiêu ngày/tuần?",1,7,4)
    st.write(f"Bạn dự định tập {workout_days} buổi/tuần để đạt mục tiêu {goal.lower()}.")
    if 'tdee' in locals():
        if goal == "Giảm cân":
            target_calories = tdee-400
        elif goal == "Giữ cân":
            target_calories = tdee
        else:
            target_calories = tdee+300
        st.subheader("Nhu cầu năng lượng theo mục tiêu")
        st.write(f"- TDEE: {tdee: .0f} kcal/ngày")
        st.write(f"- Lượng calo khuyến nghị để {goal.lower()}: '{target_calories: .0f}' kcal/ngày")
        st.markdown("Tỷ lệ dinh dưỡng")
        if goal == "Giảm cân":
            st.write("Protein: 40% | Carb = 35% | Fat: 25%")
        if goal == "Giữ cân":
            st.write("Protein: 30% | Carb = 45% | Fat: 25%")
        else:
            st.write("Protein: 35% | Carb = 45% | Fat: 20%")
        st.markdown("Gợi ý bữa ăn sáng hàng ngày ")
        if goal == "Giảm cân":
            st.markdown("""
            - Sáng: Yến mạch + sữa chua + trái cây
            - Trưa: Cơm gạo lứt, ức gà, rau luộc
            - Tối: salad cá hồi / đậu phụ + rau củ
            - Snack: hạnh nhân, sữa chua không đường
    """)
        elif goal == "Tăng cơ":
            st.markdown("""
            - Sáng: Trứng + bánh mì nguyên cám + sữa
            - Trưa: Cơm, thịt bò, rau xanh
            - Tối: cá hồi, khoai lang, rau củ
            - Snack: sữa chocolate ít báo
    """)
        else:
            st.markdown("""
            - Sáng: Trứng + trái cây + bánh mì đen
            - Trưa: Cơm, thịt gà, rau 
            - Tối: cá + rau + trái cây
    """)
        st.markdown("Gợi ý bài tập cơ bản")
        if goal == "Giảm cân":
            st.markdown("""
            - Cardio: Chạy bộ, đạp xe, nhảy dây (4-5 buổi/tuần)
            - Tập sức mạnh: Squat, push-up, plank (3 buổi/tuần)
            - Nghỉ ngơi hợp lý, ngủ đủ 7-8 tiếng
    """)
        elif goal == "Tăng cơ":
            st.markdown("""
            - Tập tạ 4-5 buổi / tuần (nhóm cơ: ngực lưng chân tay)
            - Ăn nhiều protein, đặc biệt sau khi tập
            - Cardio nhẹ (2 buổi/tuần) để duy trì tim mạch
    """)
        else:
            st.markdown("""
            - Kết hợp cardio + tập tạ
            - Giữ thói quen vận động đều và duy trì năng lượng ổn định
    """)
    else:
        st.warning("Hãy phân tích sức khoẻ để hệ thống tính TDEE trước khi lập kế hoạch")
elif menu == "Game":
    tabA,tabB,tabC,tabD,tabF,tabG, tabH, tabJ = st.tabs(["Game tung xúc sắc", "Game đoán số", "Kéo - Búa - Bao", "Game tính toán nhanh", "Game đuổi hình bắt chữ", "Game trắc nghiệm", "Game quay số may mắn", "Game puay số may mắn V2"])
    with st.sidebar:
        st.video("https://dn720301.ca.archive.org/0/items/rpreplay-final-1680875953/RPReplay_Final1680875953.mp4",autoplay=True, muted=True)
    with tabA:
        st.header("Game tung xúc sắc")
        st.image("https://thumb.ac-illust.com/11/11208a7f39207d32b1cff1a66d22dd75_t.jpeg")
        st.write("LUẬT CHƠI")
        st.write("Bấm Lắc xúc sắc để được một số ngẫu nhiên từ 1 đến 6")
        if st.button("Lắc xúc sắc"):
            roll = random.randint(1,6)
            st.success(f"bạn tung được số {roll}!!!!")
            if roll == 1:
                st.image(
                "http://www.clker.com/cliparts/m/v/m/J/4/V/dice-1-md.png"
            )
            if roll == 2:
                st.image(
                "https://www.clker.com/cliparts/a/Y/E/o/z/t/dice-2-md.png"
            )
            if roll == 3:
                st.image(
                "https://www.clker.com/cliparts/O/I/r/9/W/x/dice-3-md.png"
            )
            if roll == 4:
                st.image(
                "https://www.clker.com/cliparts/r/z/d/a/L/V/dice-4-md.png"
            )
            if roll == 5:
                st.image(
                "https://www.clker.com/cliparts/U/N/J/F/T/x/dice-5-md.png"
            )
            if roll == 6:
                st.image(
                "https://www.clker.com/cliparts/l/6/4/3/K/H/dice-6-md.png"
            )
    with tabB:
        st.header("Game đoán số bí mật 1 - 100")
        st.image("https://m.media-amazon.com/images/I/71Agu95C-jL._AC_UF894,1000_QL80_.jpg")
        st.write("LUẬT CHƠI")
        st.write("Đoán một số bất kì từ 1 đến 100, nhập số để biết được số chính xác lớn hay bé hơn số đã nhập, cố đoán trong ít lần thử nhất có thể. Bấm chơi lại sau khi đoán đúng để được chơi lại")
        if "secret" not in st.session_state:
            st.session_state.secret = random.randint(1, 100)
            st.session_state.tries = 0
        guess = st.number_input("Nhập số dự đoán 1 - 100", min_value=1,max_value=100,step=1)
        if st.button("Đoán !!!!!"):
            st.session_state.tries += 1
            if guess < st.session_state.secret:
                st.warning("lớn hơn")
                st.image(
                "https://i.kym-cdn.com/editorials/icons/original/000/013/755/mon.jpg"
            )
            elif guess > st.session_state.secret:
                st.warning("nhỏ hơn")
                st.image(
                "https://i.kym-cdn.com/editorials/icons/original/000/013/755/mon.jpg"
            )
            else:
                st.success(f"Chính xác! Bạn đoán đúng sau {st.session_state.tries} lần")
                st.image(
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR2pBfdCwgvKb7E8RBYkSluf3u3EdNxv54GuQ&s"
            )
        if st.button("Chơi lại"):
            st.session_state.secret = random.randint(1,100)
            st.session_state.tries = 0
    with tabC:
        st.header("Kéo - Búa - Bao")
        st.image("https://static.tvtropes.org/trope_videos_transcoded/images/sd/q7uwxt.jpg")
        st.write("LUẬT CHƠI")
        st.write("Bấm nút để ra một trong kéo, búa hoặc bao. Hãy cố gắng thắng con bot nha!")
        st.write("Kéo thắng bao")
        st.write("Búa thắng kéo")
        st.write("Bao thắng búa")
        user = st.selectbox("Bạn chọn: ", ["Kéo", "Búa", "Bao"])
        bot = random.choice(["Kéo", "Búa", "Bao"])
        if st.button("Ra tay nào !!!!!!"):
            st.write(f"Bot chọn: {bot}")
            if user == bot:
                st.warning("Hoà!!!")
                st.image("https://i1.sndcdn.com/artworks-ecyyzfetWzmHLDpo-X7ICfQ-t500x500.jpg")
            elif(user == "Kéo" and bot == "Bao") or (user == "Bao" and bot == "Búa") or (user == "Búa" and bot == "Kéo"):
                st.success("Bạn thắng!!!!")
                st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR1MBsQ9GnV0RNq9b_rJA63UN8m4e0Xq6HpGQ&s")
            else:
                st.error("Bạn thua!!!!")
                st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGlF-k_0Gsm39dJSSZCSEJUF-UsSkm_SAkHg&s")
    with tabD:
        st.header("Game tính toán nhanh (+ - * /)")
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ60myNa1QL0kJZoObUjDzto5UAyBokwUzLUg&s")
        st.write("LUẬT CHƠI")
        st.write("Nhập kết quả cho phép toán đã cho và bấm kiểm tra để biết đáp án đúng hay sai, bấm nút câu hỏi để được phép tính mới. Hãy trổ tài toán học của bạn nhé!")
        if "a" not in st.session_state:
            st.session_state.a = random.randint(1, 20)
            st.session_state.b = random.randint(1, 20)
            st.session_state.op = random.choice(["+", "-", "*", "/"])

        a = st.session_state.a
        b = st.session_state.b
        op = st.session_state.op
        st.session_state.answer = 0.0
        #tính kết quả đúng
        if op == "+":
            correct = a + b
        elif op == "-":
            correct = a - b
        elif op == "*":
            correct = a * b
        else:
            correct = round(a / b, 2)

        if st.button("Câu hỏi"):
            st.session_state.a = random.randint(1, 20)
            st.session_state.b = random.randint(1, 20)
            st.session_state.op = random.choice(["+", "-", "*", "/"])
            st.session_state.answer = 0.0

        a = st.session_state.a
        b = st.session_state.b
        op = st.session_state.op
        st.session_state.answer = 0.0
        if op == "/":
            st.write(f"tính {a} {op} {b} = ? (làm tròn 2 chữ số)")
        else:
            st.write(f"tính {a} {op} {b} = ?")

        answer = st.number_input("Nhập kết quả: ", step=1.0)

        if st.button ("Kiểm tra "):
            if correct == answer:
                st.success(" Chính xác")
                st.image("https://media.tenor.com/DtD4LZbctTIAAAAM/tamm-cat.gif")
            elif abs(answer - correct) < 0.005:
                st.success(" Chính xác")
                st.image("https://media.tenor.com/DtD4LZbctTIAAAAM/tamm-cat.gif")
            else:
                st.error(f"sai rùi, đáp án đúng là {correct} ")
                st.image("https://media.tenor.com/jXMsEpz30nIAAAAM/cat-cat-meme.gif")
    with tabF:
        st.header("🎯 Game Đuổi hình bắt chữ")

        puzzles = [
            {
                "image": "https://cdn.lazi.vn/storage/uploads/dhbc/1469120972_tra-hoi.jpg",
                "answer": "tra hỏi"
            },
            {
                "image": "https://cdn.lazi.vn/storage/uploads/dhbc/1469120797_khoa-so.jpg",
                "answer": "khóa sổ"
            },
            {
                "image": "https://cdn.lazi.vn/storage/uploads/dhbc/1469120784_kien-truc-su.jpg",
                "answer": "kiến trúc sư"
            },
            {
                "image": "https://cdn.lazi.vn/storage/uploads/dhbc/1468933376_thong-so.jpg",
                "answer": "thông số"
            },
            {
                "image": "https://cdn.lazi.vn/storage/uploads/dhbc/1468932212_thua-tuong.jpg",
                "answer": "thừa tướng"
            },
            {
                "image": "https://cdn.lazi.vn/storage/uploads/dhbc/1468933353_nhac-thinh-phong.jpg",
                "answer": "Nhạc thính phòng"
            },
            {
                "image": "https://cdn.lazi.vn/storage/uploads/dhbc/1468933365_sau-sac.jpg",
                "answer": "Sâu sắc"
            },
            {
                "image": "https://cdn.lazi.vn/storage/uploads/dhbc/1468933422_xa-hoa.jpg",
                "answer": "xa hoa"
            },
            {
                "image": "https://cdn.lazi.vn/storage/uploads/dhbc/1469011991_vai-tro.jpg",
                "answer": "vai trò"
            },
            {
                "image": "https://cdn.lazi.vn/storage/uploads/dhbc/1469022597_dhbc.jpg",
                "answer": "thương tâm"
            },
            {
                "image": "https://cdn.lazi.vn/storage/uploads/dhbc/1469120698_dan-bau.jpg",
                "answer": "đàn bầu"
            },
            {
                "image": "https://cdn.lazi.vn/storage/uploads/dhbc/1469120711_dan-gay-tai-trau.jpg",
                "answer": "đàn gảy tai trâu"
            },
            {
                "image": "https://cdn.lazi.vn/storage/uploads/dhbc/1469120723_dien-anh.jpg",
                "answer": "điện ảnh"
            },
            {
                "image": "https://cdn.lazi.vn/storage/uploads/dhbc/1469120735_dong-co.jpg",
                "answer": "động cơ"
            },
            {
                "image": "https://cdn.lazi.vn/storage/uploads/dhbc/1469120766_hau-dau.jpg",
                "answer": "hậu đậu"
            }
        ]

        # ===== Khởi tạo =====
        if "dhbc_index" not in st.session_state:
            st.session_state.dhbc_index = random.randint(0, len(puzzles)-1)
            st.session_state.start_time = time.time()
            st.session_state.duration = 45
            st.session_state.finished = False
            st.session_state.result = ""

        puzzle = puzzles[st.session_state.dhbc_index]

        # ===== Hiển thị hình =====
        st.image(puzzle["image"], width=300)

        # ===== Đếm giờ =====
        elapsed = int(time.time() - st.session_state.start_time)
        remaining = st.session_state.duration - elapsed

        if remaining > 0 and not st.session_state.finished:
            st.warning(f"⏳ Còn lại: {remaining} giây")
        else:
            st.session_state.finished = True
            st.error("⏰ Hết giờ!")

        # ===== Nhập đáp án =====
        guess = st.text_input("Nhập đáp án:", disabled=st.session_state.finished)

        # ===== Nút kiểm tra =====
        if st.button("Kiểm tra") and not st.session_state.finished:
            if guess.lower().strip() == puzzle["answer"].lower():
                st.session_state.result = "correct"
                st.session_state.finished = True
            else:
                st.session_state.result = "wrong"

        # ===== Hiển thị kết quả =====
        if st.session_state.result == "correct":
            st.success("🎉 Chính xác!")
            st.balloons()
        elif st.session_state.result == "wrong":
            st.error("❌ Sai rồi, thử lại!")

        # ===== Nếu hết giờ =====
        if st.session_state.finished and remaining <= 0:
            st.info(f"Đáp án đúng là: **{puzzle['answer']}**")

        # ===== Nút vòng mới =====
        if st.button("🔄 Vòng mới"):
            st.session_state.dhbc_index = random.randint(0, len(puzzles)-1)
            st.session_state.start_time = time.time()
            st.session_state.finished = False
            st.session_state.result = ""
            st.rerun()
    with tabG:
        st.header("🎯 Game Trắc Nghiệm")

        questions = [
            {
                "question": "Thủ đô của Việt Nam là gì?",
                "options": ["Hà Nội", "Huế", "Đà Nẵng", "Sài Gòn"],
                "answer": "Hà Nội"
            },
            {
                "question": "5 + 7 * 2 = ?",
                "options": ["24", "19", "17", "26"],
                "answer": "19"
            },
            {
                "question": "Ngôn ngữ dùng cho Streamlit?",
                "options": ["Java", "Python", "C++", "PHP"],
                "answer": "Python"
            },
            {
                "question": "Trái đất có bao nhiêu châu lục",
                "options": ["5", "6", "7", "8"],
                "answer": "7"
            },
            {
                "question": "HTML là viết tắt của? ",
                "options": ["HyperText Markup Language", "HighText Machine Language", "Hyper Tool Markup", "Home Tool Markup"],
                "answer": "HyperText Markup Language"
            }

        ]
        #Khởi tạo
        if "quiz_index" not in st.session_state:
            st.session_state.quiz_index = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_done = False
            st.session_state.quiz_feedback = ""
            st.session_state.quiz_checked = False
            st.session_state.start_time = time.time()
        

        TATOL_TIME = 60 # giây
        elapsed = int(time.time() - st.session_state.start_time)
        remaining = max(TATOL_TIME - elapsed, 0)

        if remaining == 0:
            st.session_state.quiz_done = True

        # Thanh tiến độ thời gian
        st.progress(remaining/TATOL_TIME)
        st.write(f"Thời gian còn lại: ** {remaining} giây")

        #Thanh tiến trình câu hỏi
        st.progress(st.session_state.quiz_index/len(questions))

        if st.session_state.quiz_done:
            st.success(f"Hoàn thành ! Điểm của bạn: {st.session_state.quiz_score}/ {len(questions)}")
            if st.button("Chơi_lại"):
                st.session_state.quiz_index = 0
                st.session_state.quiz_score = 0
                st.session_state.quiz_done = False
                st.session_state.quiz_feedback = ""
                st.session_state.quiz_checked = False
                st.session_state.start_time = time.time()
                st.rerun()
        else:
            q = questions[st.session_state.quiz_index]
            st.header(f"Câu {st.session_state.quiz_index+1}: {q['question']}")
            choice = st.radio(
                "Chọn đáp án",
                q['options'],
                key = f"quiz_{st.session_state.quiz_index}"
            )
            if st.button("Kiểm_tra"):
                if choice == q["answer"]:
                    st.session_state.quiz_score += 1
                    st.session_state.quiz_feedback = "correct"
                    st.balloons()
                    st.audio("https://www.soundjay.com/buttons/sounds/button-3.mp3")
                else:
                    st.session_state.quiz_feedback = "wrong"
                    st.audio("https://www.soundjay.com/buttons/sounds/button-10.mp3")
            #=====Hiển thị kết quả ========
            if st.session_state.quiz_feedback == "correct":
                st.success("Chính xác")
                st.balloons()
            elif st.session_state.quiz_feedback == "wrong":
                st.error(f"Sai rồi, đáp án đúng là : {q['answer']}")
            #====nút câu tiếp theo
            if st.session_state.quiz_feedback != "":
                if st.button("Câu tiếp theo"):
                    st.session_state.quiz_index += 1
                    st.session_state.quiz_feedback = ""
                    st.session_state.quiz_checked = False

                    if st.session_state.quiz_index >= len(questions):
                        st.session_state.quiz_done = True
                    st.rerun()
    with tabH:
        st.title("🧧 Game quay số may mắn")
        # Khởi tạo danh sách phần thưởng
        if "prizes" not in st.session_state:
            st.session_state.prizes = []

        # Nhập phần thưởng
        new_prize = st.text_input("Nhập phần thưởng")
        if st.button("➕ Thêm phần thưởng"):
            if new_prize:
                st.session_state.prizes.append(new_prize)
                
        # Hiển thị danh sách
        st.write("🎁 Danh sách phần thưởng:", st.session_state.prizes)
        
        # Quay số
        if st.button("🎡 Quay số"):
            if st.session_state.prizes:
                result = random.choice(st.session_state.prizes)
                st.success(f"🎉 Bạn trúng: {result}")
                # Xóa phần thưởng đã trúng
                #st.session_state.prizes.remove(result)
            else:
                st.warning("⚠️ Chưa có phần thưởng!")
        # Reset
        if st.button("🔄 Reset"):
            st.session_state.prizes = []
    with tabJ: 
        st.title("Game quay số may mắn ")
        #khởi tạo dữ liệu
        if "new_prizes" not in st.session_state:
            st.session_state.new_prizes = []
        if "weights" not in st.session_state:
            st.session_state.weights = []
        #Thêm phần thưởng
        st.subheader("➕ Thêm phần thưởng")
        col1, col2 = st.columns(2)
        with col1:
            new_prize = st.text_input("Tên phần thưởng ")
        with col2:
            weight = st.number_input("Tỷ lệ trúng (%)", 1, 100, 1)

        if st.button("Thêm"):
            if new_prize:
                st.session_state.new_prizes.append(new_prize)
                st.session_state.weights.append(weight)
                st.success(f"Đã thêm : {new_prize}")
        #danh sách phần thưởng
        st.subheader("Danh sách phần thưởng ")
        if st.session_state.new_prizes:
            for i, prize in enumerate(st.session_state.new_prizes):
                st.write(
                    f"{i + 1}. {prize} | tỷ lệ {st.session_state.weights[i]}  %"
                )
        else:
            st.info("chưa có phần thưởng ")
        
        st.subheader(" Quay số ")
        if st.button("Quay ngay "):
            if st.session_state.new_prizes:
                spin_placeholder = st.empty()

                for i in range(15):
                    spin_placeholder.markdown(
                        f'## Đang quay ... {random.choice(st.session_state.new_prizes)}'
                    )
                    time.sleep(0.1)
                #chọn kết quả theo tỷ lệ
                result = random.choices(
                    st.session_state.new_prizes,
                    weights = st.session_state.weights,
                    k = 1
                )[0]
                spin_placeholder.empty()
                st.balloons()
                st.success(f" Chúc mừng bạn đã trúng: **{result}**")
            else:
                st.warning("Chưa có phần thưởng")
        
        # Reset
        if st.button(" Reset game "):
            st.session_state.new_prizes = []
            st.session_state.weights = []
            st.success("Đã reset")





