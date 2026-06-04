import streamlit as st
import base64


@st.cache_data
def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

LOGO_BASE64 = get_base64("src/assets/images/logo.png")

def header_home():
    st.markdown(
        f"""
        <div class="home-header">
            <img src="data:image/png;base64,{LOGO_BASE64}" height="100">
            <h1 class="home-title">RECOGNIZE<br>ME</h1>
        </div>
        """,
        unsafe_allow_html=True
    )


def header_dashboard():
    st.markdown(
        f"""
            <div style="display:flex; align-items:center; justify-content:left; gap:20px;">
                <img src="data:image/png;base64,{LOGO_BASE64}" height="100">
                <h2 style='text-align:center; color:#5865F2'>RECOGNIZE<br/>ME</h2>
            </div>   
                
        """, unsafe_allow_html=True)
    