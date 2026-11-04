import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.historical import StockHistoricalDataClient

import config
from broker import PaperBroker
from strategy import MovingAverageStrategy

# 1. Page Configuration and Title Layout
st.set_page_config(page_title="Quant Trading Bot", page_icon="📈", layout="centered")
st.title("🤖 Quant Trading Dashboard")
st.write("A real-time paper trading engine running on Streamlit Cloud.")

# 2. Key Check Security Shield
if not config.API_KEY or not config.SECRET_KEY:
    st.warning("⚠️ Access Keys Missing. Please paste your API credentials inside your Streamlit Cloud Secrets settings panel.")
    st.stop()

# 3. Persistent UI Log Tracker Setup
if "activity_logs" not in st.session_state:
    st.session_state.activity_logs = ["System Initialized. Ready to scan."]

# 4. Helper Function: Live Market Data Pull
def get_market_data(client, symbol: str):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=45) # Grab plenty of buffer ticks
    request_params = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Minute,
        start=start_time,
        end=end_time
    )
    bars = client.get_stock_bars(request_params)
    df = bars.df.reset_index(level=0, drop=True)
    return df

# 5. Core Operational Code Execution Block
try:
    # Initialize Engine Instances
    broker = PaperBroker()
    data_client = StockHistoricalDataClient(config.API_KEY, config.SECRET_KEY)
    strategy = MovingAverageStrategy()

    # Visual Matrix Section
    current_cash = broker.get_balance()
    st.metric(label="Simulated Account Balance (Fake Cash)", value=f"${current_cash:,.2f}")

    # Interactive Dashboard Features Area
    st.subheader("Bot Configuration Control Panel")
    selected_stock = st.selectbox("Choose a Target Asset to Trade:", ["AAPL", "TSLA", "NVDA", "MSFT", "AMZN"])
    
    # Execution Activation Button
    if st.button("⚡ Scan Market and Process Rules Now"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with st.spinner(f"Pulling real-time candle ticks for {selected_stock}..."):
            # Execute Pipeline Sequence Steps
            df = get_market_data(data_client, selected_stock)
            signal = strategy.generate_signal(df)
            
            if signal == "BUY":
                broker.execute_market_order(selected_stock, qty=1, side="buy")
                log_msg = f"[{timestamp}] 🟢 BUY ORDER PLACED: 1 Share of {selected_stock} executed."
            elif signal == "SELL":
                broker.execute_market_order(selected_stock, qty=1, side="sell")
                log_msg = f"[{timestamp}] 🔴 SELL ORDER PLACED: 1 Share of {selected_stock} executed."
            else:
                log_msg = f"[{timestamp}] 🔍 Scan Result for {selected_stock}: Trend is holding steady (HOLD)."
            
            # Save the result to our session history feed array
            st.session_state.activity_logs.insert(0, log_msg)
            st.success("Analysis Complete!")

    # Render History Feed Output Window Box
    st.subheader("Live Operations Activity Feed Log")
    st.text_area(
        label="Terminal Updates Feed (Newest at Top)",
        value="\n".join(st.session_state.activity_logs[:15]),
        height=250,
        disabled=True
    )

except Exception as error:
    st.error(f"Operational Hub Error: {error}")
