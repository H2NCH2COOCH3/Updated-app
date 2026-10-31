import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import date

st.set_page_config(
    page_title="Dashboard Công việc - OOP",
    page_icon="📰",
    layout='wide'
)
st.title("Dashboard quản lý công việc")

class TaskManager:
    #constructor
    def __init__(self):
        if "tasks" not in st.session_state:
            st.session_state.tasks = []
    #thêm công việc
    def add_task(self, name, priority, deadline):
        task = {
            "Công việc": name,
            "Ưu tiên": priority,
            "Hạn": str(deadline),
            "Trạng thái": 'Chưa xong'
        }
        st.session_state.tasks.append(task)
    #complete
    def complete_task(self, index):
        st.session_state.tasks[index]["Trạng thái"] = "Hoàn thành"
    #not complete
    def undo_task(self, index):
        st.session_state.tasks[index]["Trạng thái"] = "Chưa xong"
    #delete tasks
    def delete_task(self, index):
        st.session_state.tasks.pop(index)
    #dataframe
    def get_dataframe(self):
        if len(st.session_state.tasks) == 0:
            return pd.DataFrame(columns=[
                "Công việc",
                "Ưu tiên",
                "Hạn",
                "Trạng thái"
            ])
        return pd.DataFrame(st.session_state.tasks)
    #thống kê
    def total(self):
        return len(st.session_state.tasks)
    def done(self):
        count = 0
        for task in st.session_state.tasks:
            if task["Trạng thái"] == "Hoàn thành":
                count += 1
        return count
    def pending(self):
        return self.total() - self.done()
    #tỷ lệ hoàn thành
    def progress(self):
        if self.total() == 0:
            return 0
        return self.done() / self.total()
    #xuat excel
    def export_excel(self):
        output = BytesIO()
        with pd.ExcelWriter(
            output,
            engine='openpyxl'
        ) as writer:
            self.get_dataframe().to_excel(
                writer,
                sheet_name="Task",
                index=False
            )
        return output.getvalue()
#tao doi tuong
manager = TaskManager()
#them cong viec
st.subheader("Them cong viec")
with st.form("add_task_form"):
    task_name = st.text_input("Ten cong viec")
    priority = st.selectbox(
        "Muc uu tien",
        [
            "Cao",
            "Trung binh",
            "Thap"
        ]
    )
    deadline = st.date_input(
        "Han hoan thanh",
        value=date.today()
    )
    submit = st.form_submit_button("Them cong viec")
    if submit:
        if task_name.strip() == "":
            st.warning("vui long nhap ten cong viec")
        else:
            manager.add_task(
                task_name,
                priority,
                deadline
            )
            st.success("Da them cong viec")
            st.rerun()

# ===================================================
# DANH SÁCH CÔNG VIỆC
# ===================================================
st.subheader("Danh sách công việc")
df = manager.get_dataframe()
if len(df) == 0:
    st.info("Chưa có công việc nào.")
else:
    for i, row in df.iterrows():
        col1, col2, col3, col4 = st.columns([5,2,2,1])
        with col1:
            st.write(
                f"**{row['Công việc']}** | "
                f"{row['Ưu tiên']} | "
                f"{row['Hạn']}"
            )
        with col2:
            if row["Trạng thái"] == "Chưa xong":
            
                if st.button("✅ Done", key=f"done{i}"):
                
                    manager.complete_task(i)
                    st.rerun()
            else:
                if st.button("↩ Undo", key=f"undo{i}"):
                    manager.undo_task(i)
                    st.rerun()
        with col3:
            st.write(row["Trạng thái"])
        with col4:
            if st.button("🗑", key=f"delete{i}"):
                manager.delete_task(i)
                st.rerun()
st.divider()
st.subheader("Thống kê")

c1, c2, c3 = st.columns(3)

c1.metric("Tổng", manager.total())
c2.metric("Hoàn thành", manager.done())
c3.metric("Còn lại", manager.pending())
st.subheader("Tiến độ")

percent = manager.progress()
st.progress(percent)
st.write(f"Đã hoàn thành {percent*100:.1f}% công việc")

chart_df = pd.DataFrame({
    "Trạng thái": ["Hoàn thành", "Chưa xong"],
    "Số lượng": [
        manager.done(),
        manager.pending()
    ]
})

st.bar_chart(chart_df.set_index("Trạng thái"))
st.subheader("Xuất Excel")
excel = manager.export_excel()
st.download_button(
    "📥 Tải Excel",
    excel,
    "todo_list.xlsx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
