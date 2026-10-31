import streamlit as st
import numpy as np
from sklearn.linear_model import LinearRegression
import feedparser
import numpy as np
import time
import matplotlib.pyplot as plt
import random
import time

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