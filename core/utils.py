# File: src/core/utils.py
import streamlit as st
from openai import OpenAI

def initialize_client():
    try:
        if "api_client" in st.session_state: return st.session_state.api_client
        API_KEY = st.secrets["GROQ_API_KEY"]
        client = OpenAI(api_key=API_KEY, base_url="https://api.groq.com/openai/v1")
        st.session_state.api_client = client
        return client
    except Exception:
        st.sidebar.error("GROQ API Key tidak ditemukan di `.streamlit/secrets.toml`.")
        return None

def init_session_state():
    if "cv_texts" not in st.session_state: st.session_state.cv_texts = []
    if "analysis_results" not in st.session_state: st.session_state.analysis_results = None