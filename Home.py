import streamlit as st, time    
from app_model.hashing import hash_generation, is_hash_valid
from app_model.db import get_connection 
from app_model.users import add_user, get_user

conn = get_connection()

st.set_page_config(page_title="Home", page_icon="🏡", layout="wide")


st.title("Hello, Friend!😁")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

tab_login, tab_register = st.tabs(["Sign In", "Sign Up"])

with tab_login:
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Sign In"):
        id, user_name, user_hash = get_user(conn, login_username)
        if login_username == user_name and is_hash_valid(login_password, user_hash):

            with st.spinner("Signing you in..."):
                    # Load user data here if needed
                    time.sleep(2)

            st.session_state["logged_in"] = True
            st.switch_page("pages/1_Dashboard.py")
            st.success("Successfully Signed In!")

            time.sleep(0.5)
        st.session_state["logged_in"] = False

with tab_register:
    register_username = st.text_input("New Username", key="register_username")
    register_password = st.text_input("New Password", type="password", key="register_password")
    hashed_password = hash_generation(register_password)

    if st.button("Sign Up"):
        st.session_state["logged_in"] = True
        add_user(conn, register_username, hashed_password)
        st.success("Successfully Registered and Signed In!")