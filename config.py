import os
import streamlit as st
from dotenv import load_dotenv

# Load local variables if running on your machine
load_dotenv()

# Prioritize Streamlit Cloud Secrets, fall back to local environment variables
API_KEY = st.secrets.get("ALPACA_PAPER_KEY") or os.getenv("ALPACA_PAPER_KEY")
SECRET_KEY = st.secrets.get("ALPACA_PAPER_SECRET") or os.getenv("ALPACA_PAPER_SECRET")
