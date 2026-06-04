import streamlit as st

from src.components.header import header_dashboard
from src.database.teacher_db import register_teacher

def teacher_register():
    # st.header("register")

    col1, col2 = st.columns([3, 1], vertical_alignment="center", gap="medium")
    with col1:
        header_dashboard()
    with col2:
        if st.button("Go back to home", type="secondary", key="registerbackbutton"):
            st.session_state["login_type"] = None
            st.rerun()

    st.header("Register your teacher profile")
    st.write("")
    st.write("")

    teacher_name     = st.text_input("Enter full name", placeholder="Madhav Singh Rana")
    teacher_username = st.text_input("Enter username", placeholder="madhavrana")
    teacher_password = st.text_input("Enter password", type="password", placeholder="Enter your password")
    confirm_password = st.text_input("Confirm password", type="password", placeholder="Confirm your password")

    st.divider()

    col1, col2 = st.columns(2, gap="small")
    with col1:
        if st.button('Register now', icon=":material/passkey:", type='primary', width="stretch"):
            if not teacher_name or not teacher_username or not teacher_password or not confirm_password:
                st.error("Please fill all fields")
            elif teacher_password != confirm_password:
                st.error("Passwords don't match")
            else:
                res = register_teacher(teacher_name, teacher_username, teacher_password)
                print(res)
                if res["success"]:
                    st.success("Registered successfully! Please login ✅")
                    st.session_state.teacher_login_type = "login"
                    st.rerun()
                else:
                    st.error(res["message"])

    with col2:
        if st.button('Login Instead', icon=":material/passkey:", type='secondary', width="stretch"):
            st.session_state.teacher_login_type = "login"
            st.rerun()
