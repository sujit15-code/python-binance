from binance.client import Client
from binance.enums import *
import logging
import getpass

# === Logging Setup ===
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.base_url = 'https://testnet.binancefuture.com'
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.FUTURES_URL = self.base_url

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        try:
            params = {
                'symbol': symbol,
                'side': SIDE_BUY if side.lower() == 'buy' else SIDE_SELL,
                'type': order_type,
                'quantity': quantity
            }

            if order_type == ORDER_TYPE_LIMIT:
                params['price'] = price
                params['timeInForce'] = TIME_IN_FORCE_GTC

            elif order_type == ORDER_TYPE_STOP_MARKET:
                params['stopPrice'] = stop_price
                params['timeInForce'] = TIME_IN_FORCE_GTC

            order = self.client.futures_create_order(**params)
            logging.info(f"Order placed: {order}")
            print("Order placed successfully!")
            print(order)
        except Exception as e:
            logging.error(f"Error placing order: {e}")
            print(f" Error: {e}")

def main():
    api_key = input("Enter your API Key: ")
    api_secret = getpass.getpass("Enter your API Secret (hidden): ")

    bot = BasicBot(api_key, api_secret)

    symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
    side = input("Buy or Sell? ").lower()
    order_type = input("Order type (MARKET / LIMIT / STOP_MARKET): ").upper()
    quantity = float(input("Quantity: "))

    if order_type == "LIMIT":
        price = float(input("Limit Price: "))
        bot.place_order(symbol, side, order_type, quantity, price)
    elif order_type == "STOP_MARKET":
        stop_price = float(input("Stop Price: "))
        bot.place_order(symbol, side, order_type, quantity, stop_price=stop_price)
    else:
        bot.place_order(symbol, side, order_type, quantity)

if __name__ == "__main__":
    main()
