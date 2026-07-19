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


st.title("Welcome to the Cyber Incidents Home🛡️")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "username" not in st.session_state:
    st.session_state.username = None

if not st.session_state.logged_in:
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

if "active_page" not in st.session_state:
    st.session_state.active_page = "Sign In"

page = st.radio(
    "",
    ["Sign In", "Sign Up"],
    index=0 if st.session_state.active_page == "Sign In" else 1,
    horizontal=True
)

if page == "Sign In":
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password")
    login_2fa = st.text_input("Authenticator Code",max_chars=6,key="login_2fa")

    if st.button("Sign In"):
        user = get_user(conn, login_username)

        if user:

            id, user_name, user_hash, twofa_secret, role, status = user

            if status == "blocked":
                st.error("Your account has been blocked. Contact an administrator.")
                st.stop()

            if is_hash_valid(login_password, user_hash):

                # Verify the 2FA code here
                if verify_code(twofa_secret, login_2fa):

                    with st.spinner("Signing you in..."):
                        time.sleep(2)

                    st.session_state["logged_in"] = True
                    st.session_state.username = user_name
                    st.session_state.role = role

                    st.rerun()

                else:
                    st.error("Invalid 2FA code.")

            else:
                st.error("Incorrect password.")

        else:
            st.error("User not found.")

    if st.session_state.logged_in:

        st.markdown("""
        <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
        </style>
        """, unsafe_allow_html=True)

        pages = {
            "🏠 Dashboard": "pages/1_Dashboard.py",
            "🤖 CSDF AI": "pages/2_AI.py",
        }

        if st.session_state.role == "Admin":
            pages["🔐 Admin Panel"] = "pages/3_Admin.py"


        selected_page = st.sidebar.radio(
            "Navigation",
            list(pages.keys())
        )

        if selected_page:
            st.switch_page(pages[selected_page])
         

elif page == "Sign Up":
    register_username = st.text_input("New Username", key="register_username")
    register_password = st.text_input("New Password", type="password", key="register_password")
    hashed_password = hash_generation(register_password)

    if st.button("Sign Up"):

        twofa_secret = generate_secret()

        role = "User"
        status = "Active"

        add_user(
            conn,
            register_username,
            hashed_password,
            twofa_secret,
            role,
            status
        )


        qr = generate_qr(
            register_username,
            twofa_secret
        )

        st.success(
    "Account created! Scan this QR code with your authenticator app."
)

        st.image(qr)

st.info("After scanning the QR code, sign in using your username, password, and the 6-digit code from your authenticator app.")

#Change to the Sign In page
st.session_state.active_page = "Sign In"

time.sleep(5)
st.rerun()