import streamlit as st

from src.screens.home_screen import home_screen
from src.screens.student.student_screen import student_screen
from src.screens.teacher.teacher_screen import teacher_screen
from src.utils.style_loader import load_css
from src.components.auto_enroll_dialog import auto_enroll_dialog


def main():
    print("App is running...✅")
    st.set_page_config(
        page_title='RecognizeMe - Smart Attendance Through AI',
        page_icon="src/assets/images/logo.png"
    )

    load_css("src/assets/styles/style.css")# base css for all

    if 'login_type' not in st.session_state:
        st.session_state.login_type = None

    if st.session_state.login_type == "student":
        load_css("src/assets/styles/dashboard.css", "src/assets/styles/footer.css")
        student_screen()
    elif st.session_state.login_type == "teacher":
        load_css("src/assets/styles/dashboard.css", "src/assets/styles/footer.css")
        teacher_screen()
    else:
        load_css("src/assets/styles/home.css", "src/assets/styles/footer.css")
        home_screen()



    join_code = st.query_params.get('join-code')
    if join_code:
        if st.session_state.login_type != 'student':
            st.session_state.login_type = 'student'
            st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            auto_enroll_dialog(join_code)

if __name__ == "__main__":
    main()