import streamlit as st
import time

from src.database.student_db import get_all_students, create_student
from src.pipelines.img_pipeline import get_face_embeddings, predict_attendance, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding


def authenticate_student_face(img_np):
    
    show_registration = False

    detected, all_ids, num_faces = predict_attendance(img_np)

    if num_faces == 0:
        st.warning('Face not found!')
    elif num_faces >1:
        st.warning('Multiple faces found')
    else:
        if detected:
            student_id = list(detected.keys())[0]
            all_students = get_all_students()
            student = next((s for s in all_students if s['student_id']==student_id), None)

            if student:
                st.session_state.is_logged_in = True
                st.session_state.user_role = 'student'
                st.session_state.student_data = student
                st.toast(f'Welcome Back {student["name"]}')
                time.sleep(1)
                st.rerun()
        else:
            st.info('Face not recognized! You might be a new student!')
            show_registration = True


    # for new student
    if show_registration:
        with st.container(border=True):
            st.header('Register new Profile')
            new_name = st.text_input("Enter your name", placeholder='E.g. Madhav Singh Rana')

            st.subheader('Optional : Voice Enrollment')
            st.info("Enroll your for voice only attendance")


            audio_data = None

            try:
                audio_data = st.audio_input('Record a short phrase like I am present, My name is Akash.')
            except Exception:
                st.error('Audio Data failed!')

            if st.button('Create Account', type='primary'):
                if new_name:
                    with st.spinner('Creating profile..'):
                        # img = np.array(Image.open(img_np))
                        encodings= get_face_embeddings(img_np)
                        if encodings:
                            face_emb = encodings[0].tolist()

                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())

                            response_data = create_student(new_name, face_embedding=face_emb, voice_embedding=voice_emb)

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f'Profile Created! Hi {new_name}!')
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error('Couldnt capture your facial features for registration')

                else:
                    st.warning('Please enter your name!')
