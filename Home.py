import streamlit as st     

st.set_page_config(page_title="Home", page_icon="🏡", layout="wide")

st.title("Welcome to the Main Page")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    

if st.button("Sign In"):
    st.session_state["logged_in"] = True
    st.success("Successfully Signed In!")

st.session_state