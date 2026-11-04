import time
from broker import PaperBroker

def check_strategy_signals():
    return "HOLD" 

def run_bot():
    broker = PaperBroker()
    print("🤖 Paper Trading Bot initialized successfully.")
    print(f"Fake Cash Balance Available: ${broker.get_balance():,.2f}")
    target_symbol = "AAPL"

    while True:
        try:
            signal = check_strategy_signals()
            if signal == "BUY":
                broker.execute_market_order(target_symbol, qty=1, side="buy")
            elif signal == "SELL":
                broker.execute_market_order(target_symbol, qty=1, side="sell")
            else:
                print(f"Scanning market... Signal: HOLD. No action taken.")
            time.sleep(60)
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(30)

if __name__ == "__main__":
    run_bot()
