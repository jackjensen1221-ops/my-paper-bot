import pandas as pd

class MovingAverageStrategy:
    def __init__(self, short_window=5, long_window=20):
        """
        short_window: The average price of the last 5 minutes (fast-moving price trend)
        long_window: The average price of the last 20 minutes (slow-moving background trend)
        """
        self.short_window = short_window
        self.long_window = long_window

    def generate_signal(self, historical_data: pd.DataFrame) -> str:
        """
        Takes a table of recent stock prices and calculates if we should BUY, SELL, or HOLD.
        historical_data must be a Pandas DataFrame containing a 'close' price column.
        """
        # 1. Ensure we have enough data points to calculate the averages
        if len(historical_data) < self.long_window:
            return "HOLD"

        # 2. Calculate the short-term and long-term moving averages
        # .iloc[-1] targets the absolute newest, most current calculated average
        short_avg = historical_data['close'].rolling(window=self.short_window).mean().iloc[-1]
        long_avg = historical_data['close'].rolling(window=self.long_window).mean().iloc[-1]

        # 3. Get the *previous* minute's averages to see if a crossover just happened
        prev_short_avg = historical_data['close'].rolling(window=self.short_window).mean().iloc[-2]
        prev_long_avg = historical_data['close'].rolling(window=self.long_window).mean().iloc[-2]

        # 4. Core Crossover Logic:
        # If the fast line crosses ABOVE the slow line -> BUY signal
        if prev_short_avg <= prev_long_avg and short_avg > long_avg:
            return "BUY"
            
        # If the fast line crosses BELOW the slow line -> SELL signal
        elif prev_short_avg >= prev_long_avg and short_avg < long_avg:
            return "SELL"
            
        # Otherwise, if they are just moving in parallel, do nothing
        else:
            return "HOLD"
