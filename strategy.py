import pandas as pd

class MovingAverageStrategy:
    def __init__(self, short_window=5, long_window=20):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signal(self, historical_data: pd.DataFrame) -> str:
        if len(historical_data) < self.long_window:
            return "HOLD"

        # Calculate moving averages
        short_avg = historical_data['close'].rolling(window=self.short_window).mean().iloc[-1]
        long_avg = historical_data['close'].rolling(window=self.long_window).mean().iloc[-1]

        prev_short_avg = historical_data['close'].rolling(window=self.short_window).mean().iloc[-2]
        prev_long_avg = historical_data['close'].rolling(window=self.long_window).mean().iloc[-2]

        # Crossover logic checks
        if prev_short_avg <= prev_long_avg and short_avg > long_avg:
            return "BUY"
        elif prev_short_avg >= prev_long_avg and short_avg < long_avg:
            return "SELL"
        else:
            return "HOLD"
