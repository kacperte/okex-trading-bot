from bot import OkexBot, APISECRET, APIKEY, PASS
import time
from os import getenv

SIZE_OF_PROFIT = float(getenv("SIZE_OF_PROFIT"))
SIZE_OF_LOSSES = float(getenv("SIZE_OF_LOSSES"))
SIZE_OF_SELL_POSITIVE = float(getenv("SIZE_OF_SELL_POSITIVE"))
SIZE_OF_SELL_NEGATIVE = float(getenv("SIZE_OF_SELL_NEGATIVE"))


class MarketMaker(OkexBot):

    def __init__(self, details: list, APIKEY, APISECRET, PASS):
        super().__init__(APIKEY, APISECRET, PASS)
        self.details = details

    def open_position(self, size_of_balance: float):
        new_coin_id = self.details[0]["instId"]
        usdt_to_order = float(self.get_balance('USDT')) * size_of_balance
        t0 = time.time()
        order = self.place_market_order(pair=new_coin_id, side='buy', amount=usdt_to_order).json()["data"]
        t1 = time.time() - t0
        print(t1)
        if order[0]['ordId']:
            print(f"Open succesfull new position - order number: {order[0]['ordId']}")
            time.sleep(5)
            order_info = self.get_info()[0]
            self.monitor_position(order_info=order_info, size_of_profit=SIZE_OF_PROFIT, size_of_losses=SIZE_OF_LOSSES)
        else:
            print("ERROR - Failed to complete the transaction")

    def monitor_position(self, order_info: dict, size_of_profit: float, size_of_losses: float):
        print(f"Start monitoring")
        purchase_price = float(order_info['fillPx'])
        while True:
            current_price = float(self.check_price(order_info['instId']))
            if current_price >= purchase_price * size_of_profit:
                self.close_position(coin_id=order_info['instId'], size_of_sell=SIZE_OF_SELL_POSITIVE)
            elif current_price <= purchase_price * size_of_losses:
                self.close_position(coin_id=order_info['instId'], size_of_sell=SIZE_OF_SELL_NEGATIVE)

    def close_position(self, coin_id: str, size_of_sell: float):
        coin_id = coin_id.split("-")[0]
        quantity_of_token = self.get_balance(coin_id)
        quantity_of_tokene_to_sell = float(quantity_of_token) * size_of_sell
        order = self.place_market_order(pair=coin_id, side='sell', amount=quantity_of_tokene_to_sell).json()["data"]
        if not order[0]['ordId']:
            print("ERROR - Failed to complete the transaction")
