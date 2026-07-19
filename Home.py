import streamlit as st, time    
from app_model.hashing import hash_generation, is_hash_valid
from app_model.db import get_connection 
from app_model.users import add_user, get_user
from app_model.two_factor import (
    generate_secret,
    generate_qr,
    verify_code
)

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
    login_password = st.text_input("Password", type="password")
    login_2fa = st.text_input("Authenticator Code",max_chars=6,key="login_2fa")

    if st.button("Sign In"):
        user = get_user(conn, login_username)

        if user:

            id, user_name, user_hash, twofa_secret = user

            if is_hash_valid(login_password, user_hash):

                # Verify the 2FA code here
                if verify_code(twofa_secret, login_2fa):

                    with st.spinner("Signing you in..."):
                        time.sleep(2)

                    st.session_state["logged_in"] = True
                    st.switch_page("pages/1_Dashboard.py")

                else:
                    st.error("Invalid 2FA code.")

            else:
                st.error("Incorrect password.")

        else:
            st.error("User not found.")
         

with tab_register:
    register_username = st.text_input("New Username", key="register_username")
    register_password = st.text_input("New Password", type="password", key="register_password")
    hashed_password = hash_generation(register_password)

    if st.button("Sign Up"):

        twofa_secret = generate_secret()

        add_user(
            conn,
            register_username,
            hashed_password,
            twofa_secret
        )


        qr = generate_qr(
            register_username,
            twofa_secret
        )

        st.success(
            "Account created! Scan this QR code with your authenticator app."
        )

        st.image(qr)