import streamlit as st
from app_model.cyber_incidents import get_all_cyber_incidents
from app_model.db import conn

st.set_page_config(page_title="Home", page_icon="🏡", layout="wide")

st.title("Welcome to the Home Page")

data = get_all_cyber_incidents(conn)

with st.sidebar:
    st.header("Navigation")
    st.selectbox('Severity Level', data['severity'].unique())

st.bar_chart(data["Category"].value_counts())
data()
 