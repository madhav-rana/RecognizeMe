import streamlit as st


from src.components.footer import footer_dashboard

from src.screens.teacher.login_view import teacher_login
from src.screens.teacher.register_view import teacher_register
from src.screens.teacher.teacher_dashboard import teacher_dashboard

def teacher_screen():
    # st.header("Teacher Screen")

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif ('teacher_login_type' not in st.session_state 
        or st.session_state.teacher_login_type == "login"
    ):
        teacher_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_register()

    footer_dashboard()

