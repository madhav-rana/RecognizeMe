import streamlit as st
import time

from src.components.header import header_dashboard
from src.database.teacher_db import login_teacher

from src.utils.alerts import show_alert

def teacher_login():
    # st.header("login")

    col1, col2 = st.columns([3, 1], vertical_alignment="center", gap="medium")
    with col1:
        header_dashboard()
    with col2:
        if st.button("Go back to home", type="secondary", key="loginbackbutton"):
            st.session_state["login_type"] = None
            st.rerun()

    st.write("")
    st.header("Login using password", text_alignment="center")
    st.write("")

    teacher_username = st.text_input("Enter username", key="teacher_username", placeholder="madhavrana")
    teacher_password = st.text_input("Enter password", key="teacher_password", type="password", placeholder="Enter your password")

    st.divider()

    col1, col2 = st.columns(2, gap="small")
    with col1:
        if st.button('Login', icon=":material/passkey:", type='primary', width="stretch"):
            
            with st.spinner('Authenticating user...'):
                
                if not teacher_username or not teacher_password:
                    st.error("Please fill all fields")
                else:
                    res = login_teacher(teacher_username, teacher_password)
                    print(res)
                    if res["success"]:
                        st.session_state.user_role ='teacher'
                        st.session_state.teacher_data = res["data"]
                        st.session_state.is_logged_in = True

                        # st.toast("welcome back!", icon="👋")
                        show_alert(
                            f"Welcome back {teacher_username}",
                            "success"
                        )
                        time.sleep(1)
                        st.rerun()
                    else:
                        # st.error("Invalid username and password combo")
                        show_alert(
                            "Invalid username or password",
                            "error"
                        )
                        time.sleep(1)
                        st.rerun()
                    

    with col2:
        if st.button('Register Instead', icon=":material/passkey:", type='secondary', width="stretch"):
            st.session_state.teacher_login_type = "register"
            st.rerun()
    