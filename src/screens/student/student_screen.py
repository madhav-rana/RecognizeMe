import streamlit as st

import numpy as np
from PIL import Image

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.screens.student.student_dashboard import student_dashboard
from src.screens.student.student_auth import authenticate_student_face


def student_screen():
    # st.header("Student screen comming soon...")

    if "student_data" in st.session_state:
        student_dashboard()
        return
    
    col1, col2 = st.columns([4, 2], vertical_alignment="center", gap="large")
    with col1:
        header_dashboard()
    with col2:
        if st.button("Go back to home", type="secondary", key="student_back_button", width="stretch"):  # ✅ unique key
            st.session_state["login_type"] = None
            st.rerun()

    st.write("")
    st.header("Login with your face ID", text_alignment="center")
    st.write("")

    photo = st.camera_input("Position your face in the center")

    if photo is not None:
        # st.info("📸 Photo captured! Processing...")  # ✅ user feedback
        image = Image.open(photo)
        image_np = np.array(image)

        with st.spinner("Authenticating..."):
            authenticate_student_face(image_np)
            # print("comming soon...")
            

    footer_dashboard()