import streamlit as st

from src.components.header import header_home
from src.components.footer import footer_home

def home_screen():

    header_home()

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        # st.header("I'm Student")
        st.markdown(
            "<h2 class='card-title'>I'm Student</h2>",
            unsafe_allow_html=True
        )
        st.image("src/assets/images/student_img.png", width=120)
        if st.button("Student Login", type="secondary", icon=':material/arrow_outward:', icon_position='right'):
            st.session_state["login_type"] = "student"
            st.rerun()

    with col2:
        # st.header("I'm Teacher")
        st.markdown(
            "<h2 class='card-title'>I'm Teacher</h2>",
            unsafe_allow_html=True
        )
        st.image("src/assets/images/teacher_img.png", width=145)
        if st.button("Teacher Login", type="secondary", icon=':material/arrow_outward:', icon_position='right'):
            st.session_state["login_type"] = "teacher"
            st.rerun()
    
    footer_home()