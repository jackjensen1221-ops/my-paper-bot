import time
from datetime import datetime, timedelta
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.historical import StockHistoricalDataClient
import config
from broker import PaperBroker
from strategy import MovingAverageStrategy

def get_live_market_data(data_client, symbol: str) -> str:
    """
    Fetches the last 30 minutes of price history from Alpaca's live data feed
    and formats it into a table (DataFrame) for our strategy.
    """
    # Calculate the time window (last 30 minutes)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=30)
    
    # Request 1-minute interval price bars
    request_params = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Minute,
        start=start_time,
        end=end_time
    )
    
    # Fetch the data and convert it directly into a clean Pandas table
    bars = data_client.get_stock_bars(request_params)
    df = bars.df
    
    # Standardize format so our strategy class can read it cleanly
    df = df.reset_index(level=0, drop=True) # Cleans up the symbol index layout
    return df

def run_bot():
    # 1. Initialize our Broker connection and Data client
    broker = PaperBroker()
    data_client = StockHistoricalDataClient(config.API_KEY, config.SECRET_KEY)
    
    # 2. Initialize our mathematical strategy rules
    strategy = MovingAverageStrategy(short_window=5, long_window=20)
    
    print("🤖 Paper Trading Bot initialized with Moving Average Strategy.")
    print(f"Fake Cash Balance Available: ${broker.get_balance():,.2f}")
    
    target_symbol = "AAPL"  # The stock our bot will track and trade
    
    # 3. Infinite Trading Loop
    while True:
        try:
            # Step A: Get the newest live market data
            historical_data = get_live_market_data(data_client, target_symbol)
            
            # Step B: Feed that data into our strategy to see if it generates a signal
            signal = strategy.generate_signal(historical_data)
            
            # Step C: Take action based on the signal
            if signal == "BUY":
                broker.execute_market_order(target_symbol, qty=1, side="buy")
            elif signal == "SELL":
                broker.execute_market_order(target_symbol, qty=1, side="sell")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Monitoring {target_symbol}... Strategy says: HOLD.")
            
            # Step D: Rest for 60 seconds before pulling the next live price tick
            time.sleep(60)
            
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(30) # Short break if there's a connection glitch

if __name__ == "__main__":
    run_bot()
