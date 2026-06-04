import streamlit as st
from supabase import create_client

print("Loading DB...")
# print(st.secrets)

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)
