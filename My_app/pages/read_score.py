import streamlit as st
import pandas as pd
data = pd.read_csv('score.csv')
st.line_chart(data)
st.line_chart(data, x='hours', y='scores')
st.bar_chart(data, x=None, y=None)
st.bar_chart(data)
st.bar_chart(data, x='hours', y='scores')
st.area_chart(data, x=None, y=None)
st.area_chart(data)
st.area_chart(data, x='hours', y='scores')