import streamlit as st
import numpy as np
from sklearn.linear_model import LinearRegression
import feedparser
import numpy as np
import time
import matplotlib.pyplot as plt
import random
import time
from utils.bmi import calculate_bmi
from utils.ml_model import load_sleep_model

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
        bmi =   calculate_bmi(can_nang, chieu_cao)
        st.metric("chỉ số bmi của bạn là", f"{bmi: .2f}")
        #st.success(f"chỉ số bmi của bạn là: {bmi: .2f}")

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

    @st.cache_resource
    def get_model():
        return load_sleep_model()
    model = get_model()

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