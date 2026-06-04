import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.student_db import get_all_students


@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec



def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()

    faces = detector(image_np, 1)
    # here you can change 1 -> 2, 3, 4 etc but then it need more cpu utilization

    encodings = []

    for face in faces:
        shape = sp(image_np, face)

        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1) #128 embedding

        encodings.append(np.array(face_descriptor))

    return encodings
    # return encodings, faces  # ← return both


@st.cache_resource
def get_trained_model():

    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:

        embedding = student.get("face_embedding")

        if embedding:

            X.append(np.array(embedding))

            y.append(student.get("student_id"))

    if len(X) == 0:
        return None

    # SVM Classifier
    clf = SVC(
        kernel="linear",
        probability=True,
        class_weight="balanced"
    )

    if len(set(y)) < 2:
        return {
            "clf": None,   # explicitly signal "not usable"
            "X": X,
            "y": y         # still useful — you can do direct distance matching
        }

    clf.fit(X, y)          # only reached if 2+ students
    return {"clf": clf, "X": X, "y": y}


def train_classifier():
    st.cache_resource.clear()   # ← destroys stale cache
    model_data = get_trained_model()  # ← forces fresh retrain with new data
    return bool(model_data)     # ← tells caller if training succeeded



def predict_attendance(class_image_np):

    encodings = get_face_embeddings(class_image_np)

    detected_students = {} # no student at starting

    model_data = get_trained_model()

    if not model_data:
        return detected_students, [], len(encodings)

    clf = model_data["clf"]
    X_train = model_data["X"]
    y_train = model_data["y"]

    all_students = sorted(list(set(y_train)))

    for encoding in encodings:

        # Predict student
        if len(all_students) >= 2:
            predicted_id = int(clf.predict([encoding])[0])
        else:
            predicted_id = int(all_students[0])

        # Get stored embedding
        student_embedding = X_train[
            y_train.index(predicted_id)
        ]

        # Calculate Euclidean distance
        distance = np.linalg.norm(
            student_embedding - encoding
        )

        # Threshold verification
        threshold = 0.6

        if distance <= threshold:

            detected_students[predicted_id] = {
                "matched": True,
                "distance": float(distance)
            }

    return detected_students, all_students, len(encodings)

    
