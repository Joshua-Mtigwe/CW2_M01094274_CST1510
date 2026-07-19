import streamlit as st,time

def sidebar():

    with st.sidebar:

        if "logged_in" in st.session_state and st.session_state.logged_in:

            if st.button("🚪 Sign Out", use_container_width=True):
                st.session_state.clear()
                st.session_state.logged_in = False
                st.session_state.username = None
        
                with st.spinner("Signing you out..."):
                        time.sleep(1)

                st.switch_page("Home.py")