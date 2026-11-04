import os
import streamlit as st
from dotenv import load_dotenv

# Try loading local .env first
load_dotenv()

# Check local environment or fall back to Streamlit cloud secrets
API_KEY = os.getenv("ALPACA_PAPER_KEY") or st.secrets.get("ALPACA_PAPER_KEY")
SECRET_KEY = os.getenv("ALPACA_PAPER_SECRET") or st.secrets.get("ALPACA_PAPER_SECRET")

if not API_KEY or not SECRET_KEY:
    st.error("Missing API keys! Please configure them in Streamlit Secrets.")
