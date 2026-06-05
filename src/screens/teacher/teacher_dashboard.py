import streamlit as st
import time
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard

from src.screens.teacher.teacher_service import *

def teacher_dashboard():
    teacher_data = st.session_state.teacher_data 

    c1, c2 = st.columns([4, 2], vertical_alignment='center', gap='large')
    with c1:
        header_dashboard()
    with c2:
        # st.subheader(f"""Welcome, {teacher_data['name']}""")
        st.markdown(
            f"""<h3>Welcome, {teacher_data['username']}</h3>""",
            unsafe_allow_html=True
        )
        if st.button("Logout", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data
            st.toast("Logout successfully!")
            time.sleep(1)
            st.rerun()


    st.write("")
    st.write("")
    st.write("")


    # st.header("More feature comming soon...")

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"


    tab1, tab2, tab3 = st.columns(3)


    with tab1:
        # st.header("Comming soon...")

        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        
        if st.button('Take Attendance', type=type1, width='stretch', icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        # st.header("Comming soon...")

        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else "tertiary"
        
        if st.button('Manage Subjects', type=type2, width='stretch', icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        # st.header("Comming soon...")

        type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else "tertiary"
        
        if st.button('Attendance Records', type=type3, width='stretch', icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()


    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()
