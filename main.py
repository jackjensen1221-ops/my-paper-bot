import streamlit as st
import time
from datetime import datetime, timedelta
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.historical import StockHistoricalDataClient
import config
from broker import PaperBroker
from strategy import MovingAverageStrategy

# Set up the visual layout of your web page
st.set_page_config(page_title="Quant Trading Bot Dashboard", page_icon="🤖", layout="wide")

st.title("🤖 Live Quant Paper-Trading Dashboard")
st.write("This application runs your moving average strategy using fake money.")

# Create placeholders in the web UI for live updating data
balance_metric = st.empty()
log_header = st.subheader("Live Activity Log")
log_box = st.empty()

# Initialize session state to keep logs persistent across web refreshes
if "trade_logs" not in st.session_state:
    st.session_state.trade_logs = []

def get_live_market_data(data_client, symbol: str):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=30)
    request_params = StockBarsRequest(symbol_or_symbols=symbol, timeframe=TimeFrame.Minute, start=start_time, end=end_time)
    bars = data_client.get_stock_bars(request_params)
    df = bars.df
    df = df.reset_index(level=0, drop=True)
    return df

# Main operational engine loop
if config.API_KEY and config.SECRET_KEY:
    try:
        broker = PaperBroker()
        data_client = StockHistoricalDataClient(config.API_KEY, config.SECRET_KEY)
        strategy = MovingAverageStrategy(short_window=5, long_window=20)
        target_symbol = "AAPL"
        
        # Display the live balance metric cleanly on screen
        current_balance = broker.get_balance()
        balance_metric.metric(label="Simulated Cash Account Balance", value=f"${current_balance:,.2f}")
        
        # Run execution block loop
        timestamp = datetime.now().strftime('%H:%M:%S')
        historical_data = get_live_market_data(data_client, target_symbol)
        signal = strategy.generate_signal(historical_data)
        
        if signal == "BUY":
            broker.execute_market_order(target_symbol, qty=1, side="buy")
            st.session_state.trade_logs.insert(0, f"[{timestamp}] 🟢 PLACED BUY ORDER for 1 share of {target_symbol}")
        elif signal == "SELL":
            broker.execute_market_order(target_symbol, qty=1, side="sell")
            st.session_state.trade_logs.insert(0, f"[{timestamp}] 🔴 PLACED SELL ORDER for 1 share of {target_symbol}")
        else:
            st.session_state.trade_logs.insert(0, f"[{timestamp}] 🔍 Scanning market... Signal: HOLD. No action taken.")

        # Keep only the last 20 logs to save memory space
        st.session_state.trade_logs = st.session_state.trade_logs[:20]
        
        # Output formatting for your text area logs box
        log_box.text_area("Bot Activity Feed", value="\n".join(st.session_state.trade_logs), height=300)
        
        # Auto-refresh the entire webpage every 60 seconds to scan the market again
        time.sleep(60)
        st.rerun()

    except Exception as e:
        st.error(f"Execution Error occurred: {e}")

