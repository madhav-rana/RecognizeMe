import streamlit as st

def load_css(*files):
    css = ""

    for file in files:
        with open(file, encoding="utf-8") as f:
            css += f.read()

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )