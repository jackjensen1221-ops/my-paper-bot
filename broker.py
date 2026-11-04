from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import config

class PaperBroker:
    def __init__(self):
        self.client = TradingClient(config.API_KEY, config.SECRET_KEY, paper=True)

    def get_balance(self):
        account = self.client.get_account()
        return float(account.cash)

    def execute_market_order(self, symbol: str, qty: int, side: str):
        order_side = OrderSide.BUY if side.lower() == "buy" else OrderSide.SELL
        req = MarketOrderRequest(symbol=symbol, qty=qty, side=order_side, time_in_force=TimeInForce.DAY)
        order = self.client.submit_order(order_data=req)
        print(f"Executed Simulated {side.upper()} order for {qty} shares of {symbol}.")
        return order
