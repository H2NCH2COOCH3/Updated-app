import streamlit as st
def calculate_bmi(can_nang, chieu_cao):
        bmi =   can_nang/(chieu_cao ** 2)
        #st.success(f"chỉ số bmi của bạn là: {bmi: .2f}")
        return bmi

