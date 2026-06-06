import streamlit as st
import time

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.enroll_dialog import enroll_dialog
from src.database.student_db import (
    get_student_subjects,
    get_student_attendance,
    unenroll_student_to_subject
)
from src.components.subject_card import subject_card

from src.utils.alerts import show_alert

def student_dashboard():

    # st.header("Student dashboard is comming soon...")

    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    # c1, c2 = st.columns([3,1], vertical_alignment='center', gap='xxlarge')
    c1, c2 = st.columns([4, 2], vertical_alignment='center', gap='large')

    with c1:
        header_dashboard()
    with c2:
        # st.subheader(f"""Welcome, {student_data['username']} """)
        name = student_data["name"]
        st.markdown(
            f"""
            <h5 style='text-align:center;'>
                Hi, {name}
            </h5>
            """,
            unsafe_allow_html=True
        )
        if st.button("Logout", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data 
            st.rerun()

    st.write("")
    st.write("")

    c1, c2 =st.columns(2)
    with c1:
        st.header('Your Enrolled Subjects')
    with c2:
        if st.button('Enroll in Subject', type='primary', width='stretch'):

            # st.header("comming soon...")

            enroll_dialog()


    st.divider()

    # List your enrolled subjects

    with st.spinner('Loading your enrolled subjects..'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}

    for log in logs:
        sub_id = log['subject_id']

        if sub_id not in stats_map:
            stats_map[sub_id] = {"total":0, "attended": 0}

        stats_map[sub_id]['total'] +=1

        if log.get('is_present'):
            stats_map[sub_id]['attended'] += 1


    cols = st.columns(2) # dynamic column

    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sub_id = sub['subject_id']


        stats = stats_map.get(sub_id,{"total":0, "attended": 0} )

        def unenroll_button(sub_id=sub_id, sub_name=sub['name']):
            if st.button(
                "Unenroll from this course",
                key=f"unenroll_{sub_id}",
                type='tertiary',
                width='stretch',
                icon=':material/delete_forever:'
            ):
                unenroll_student_to_subject(student_id, sub_id)
                # st.toast(f"Unenrolled from {sub_name} successfully!")
                # st.success(
                #     f"Successfully unenrolled from **{sub_name}** ✅"
                # )
                show_alert(
                    f"Successfully unenrolled from {sub_name}",
                    "success"
                )
                time.sleep(2)
                st.rerun()

        with cols[i % 2]:

            subject_card(
                name = sub['name'],
                code =sub['subject_code'],
                section = sub['section'],
                stats = [
                    ('📅', 'Total', stats['total']),
                    ('✅', 'Attended', stats['attended']),
                ],
                footer_callback=unenroll_button
            )
    footer_dashboard()