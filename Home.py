import streamlit as st
import pandas as pd
from app_model.cyber_incidents import get_all_cyber_incidents
from app_model.db import get_connection

st.set_page_config(page_title="Home", page_icon="🏡", layout="wide")

st.title("Welcome to the Home Page")

conn = get_connection()
data = get_all_cyber_incidents(conn)

with st.sidebar:
    st.header("Navigation")
    severity_ = st.selectbox('Severity Level', data['severity'].unique())

data['timestamp'] = pd.to_datetime(data['timestamp'])
filtered_data = data[data['severity'] == severity_]

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Cyber Incidents with {severity_} Severity")
    st.bar_chart(filtered_data['category'].value_counts())

with col2:
    st.subheader(f"Category Trends Over Time for {severity_} Severity")
    st.line_chart(filtered_data, x = 'timestamp', y ='category')

st.subheader(f"Filtered Data")
st.dataframe(filtered_data)