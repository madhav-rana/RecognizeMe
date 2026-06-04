import streamlit as st
import base64

logo_url = "src/assets/images/madhav_photo.png"

@st.cache_data
def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

LOGO_BASE64 = get_base64("src/assets/images/madhav_pic.png")

def footer_home():
    st.markdown(f"""
        <div class="footer">
            <p>
                RecognizeMe • Smart Attendance Through AI
            </p>
            <p><strong>Created with ❤️ by </strong><img src="data:image/png;base64,{LOGO_BASE64}" height="30"></p>
            
        </div>
    """, unsafe_allow_html=True)


def footer_dashboard():
    st.markdown(f"""
        <div class="footer">
            <p id="footer-dashboard">
                RecognizeMe • Smart Attendance Through AI
            </p>
            <p id="footer-dashboard"><strong>Created with ❤️ by </strong><img src="data:image/png;base64,{LOGO_BASE64}" height="30"></p>
        </div>
    """, unsafe_allow_html=True)