import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPACA_PAPER_KEY")
SECRET_KEY = os.getenv("ALPACA_PAPER_SECRET")

if not API_KEY or not SECRET_KEY:
    raise ValueError("Missing API keys! Ensure ALPACA_PAPER_KEY and ALPACA_PAPER_SECRET are configured.")
