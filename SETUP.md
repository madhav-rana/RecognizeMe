# RecognizeMe — Setup Guide

## 1. Create virtual environment
python -m venv .venv
.venv\Scripts\activate

## 2. Install dependencies
pip install -r requirements.txt

## 3. Two manual steps (Windows only — required for voice recognition)
pip install webrtcvad-wheels
pip install resemblyzer --no-deps

## 4. Add your secrets
Create .streamlit/secrets.toml with:
SUPABASE_URL = "your-url"
SUPABASE_KEY = "your-key"
APP_DOMAIN = "http://localhost:8501"

## 5. Run
streamlit run app.py