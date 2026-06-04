import io
import librosa
import numpy as np
import streamlit as st

from resemblyzer import (VoiceEncoder, preprocess_wav)

# LOAD VOICE ENCODER MODEL

@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()


# GENERATE VOICE EMBEDDING

def get_voice_embedding(audio_bytes):
    try:
        # Load cached voice encoder
        encoder = load_voice_encoder()

        # Convert bytes into waveform
        audio, sample_rate = librosa.load(
            io.BytesIO(audio_bytes),
            sr=16000
        )

        # Preprocess audio
            # Handles:
            # - normalization
            # - silence trimming
            # - formatting

        wav = preprocess_wav(audio)

        # Generate speaker embedding
        embedding = encoder.embed_utterance(wav)

        # Convert NumPy array → Python list
        # Useful for database storage

        return embedding.tolist()
    except Exception as error:

        st.error(f"Voice embedding error: {error}")
        return None




# IDENTIFY SPEAKER
def identify_speaker(new_embedding, candidates_dict, threshold=0.65):

    # Validate inputs
    if new_embedding is None:
        return None, 0.0

    if not candidates_dict:
        return None, 0.0

    # Track best match
    best_student_id = None
    best_score = -1.0

    # Convert to NumPy array
    new_embedding = np.array(new_embedding)

    # Compare against all registered students
    for student_id, stored_embedding in candidates_dict.items():

        if stored_embedding is None:
            continue

        stored_embedding = np.array(stored_embedding)

        # Similarity Calculation
        # Dot Product Similarity

        # Higher value = more similar


        similarity = np.dot(
            new_embedding,
            stored_embedding
        )

        # Keep best match
        if similarity > best_score:

            best_score = similarity

            best_student_id = student_id

    # Threshold Verification
    if best_score >= threshold:
        return best_student_id, best_score

    # No reliable match found
    return None, best_score




# PROCESS LONG AUDIO / MULTI-SPEAKER AUDIO
def process_bulk_audio(audio_bytes, candidates_dict, threshold=0.65):
    try:
        # Load voice encoder
        encoder = load_voice_encoder()

        # Load waveform
        audio, sample_rate = librosa.load(
            io.BytesIO(audio_bytes),
            sr=16000
        )

        # Detect non-silent regions
        # top_db controls silence sensitivity
        segments = librosa.effects.split(
            audio,
            top_db=30
        )

        # Store detected speakers
        identified_results = {}

        # Process each speech segment
        for start, end in segments:

            # Ignore extremely short segments
            segment_duration = (end - start) / sample_rate

            if segment_duration < 0.5:
                continue

            segment_audio = audio[start:end] # Extract speech segment
            wav = preprocess_wav(segment_audio) # Preprocess audio
            embedding = encoder.embed_utterance(wav) # Generate speaker embedding

            # Identify speaker
            student_id, score = identify_speaker(embedding, candidates_dict, threshold)

            # Store best score per student
            if student_id:
                if (
                    student_id not in identified_results
                    or
                    score > identified_results[student_id]
                ):

                    identified_results[student_id] = score

        return identified_results

    except Exception as error:

        st.error(f"Bulk audio processing error: {error}")

        return {}

