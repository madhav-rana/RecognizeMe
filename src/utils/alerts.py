import streamlit as st

def show_alert(message, alert_type="info"):
    
    styles = {
        "success": {
            "bg": "#d1e7dd",
            "text": "#0f5132",
            "border": "#198754",
            "icon": "✅"
        },
        "warning": {
            "bg": "#fff3cd",
            "text": "#664d03",
            "border": "#ffc107",
            "icon": "⚠️"
        },
        "error": {
            "bg": "#f8d7da",
            "text": "#842029",
            "border": "#dc3545",
            "icon": "❌"
        },
        "info": {
            "bg": "#cff4fc",
            "text": "#055160",
            "border": "#0dcaf0",
            "icon": "ℹ️"
        }
    }

    style = styles.get(alert_type, styles["info"])

    st.markdown(
        f"""
        <div style="
            background:{style['bg']};
            color:{style['text']};
            padding:15px;
            border-radius:12px;
            border-left:6px solid {style['border']};
            margin-bottom:10px;
        ">
            {style['icon']} {message}
        </div>
        """,
        unsafe_allow_html=True
    )