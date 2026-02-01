import os
import streamlit as st
from dotenv import load_dotenv

from resume_analyzer.ui import show_form, show_results
from resume_analyzer.utils import load_bert_model

# ---------------------------
# Streamlit app: Resume Analyzer
# ---------------------------

# --- Session State Defaults ---
if "resume" not in st.session_state:
    st.session_state.resume = None
if "job_descriptions" not in st.session_state:
    st.session_state.job_descriptions = []
if "results" not in st.session_state:
    st.session_state.results = []
if "page" not in st.session_state:
    st.session_state.page = "form"
    st.session_state['analysis_triggered'] = False
    st.session_state.page = "form"

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("🚨 GROQ_API_KEY is not set! Please add it to your .env file or environment variables.")
    st.stop()

# Load CSS safely
if os.path.exists("style.css"):
    with open("style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.warning("⚠ style.css not found. Using default Streamlit styling.")

# Title and description
st.title("AI Resume Analyzer 📝")
st.caption("Multi-JD comparison — per JD a dedicated analysis")

# ---------------------------
# --- Main App Flow ---

# Main flow
if not st.session_state['analysis_triggered']:
    # Pre-load model once and pass it to the form
    # Use st.cache_resource to load the model only once.
    @st.cache_resource
    def get_model():
        
        return load_bert_model()

    model = get_model()
    show_form(model, api_key)
else:
    show_results(api_key)
