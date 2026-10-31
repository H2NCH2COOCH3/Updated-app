import streamlit as st
import random
import time

tabA,tabB,tabC,tabD,tabF,tabG, tabH = st.tabs(["Game tung xúc sắc", "Game đoán số", "Kéo - Búa - Bao", "Game tính toán nhanh", "Game đuổi hình bắt chữ", "Game trắc nghiệm", "Game quay số may mắn"])
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
    st.title("🎁Game quay số may mắn ")
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
    st.subheader("🎀Danh sách phần thưởng ")
    if st.session_state.new_prizes:
        for i, prize in enumerate(st.session_state.new_prizes):
            st.write(
                f"{i + 1}. {prize} | tỷ lệ {st.session_state.weights[i]}  %"
            )
    else:
        st.info("chưa có phần thưởng ")
    
    st.subheader(" ✨Quay số ")
    if st.button("🎇Quay ngay "):
        if st.session_state.new_prizes:
            spin_placeholder = st.empty()
            for i in range(15):
                spin_placeholder.markdown(
                    f'## 🎡 Đang quay ... {random.choice(st.session_state.new_prizes)}'
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
            st.success(f" 🎉Chúc mừng bạn đã trúng: **{result}**")
        else:
            st.warning("🎃Chưa có phần thưởng")
    
    # Reset
    if st.button(" 🎡Reset game "):
        st.session_state.new_prizes = []
        st.session_state.weights = []
        st.success("✔Đã reset")