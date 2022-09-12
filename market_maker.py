from bot import OkexBot, APISECRET, APIKEY, PASS

new_coin = [{
    "changePerDay24h": "0.0032",
    "changePerDayUtc0": "0.0399",
    "changePerDayUtc8": "-0.0011",
    "icon": "https://static.coinall.ltd/cdn/announce/20220901/1662021138108b7501e58-6ece-4483-88b8-38c576e79017.png",
    "instId": "LINK-USDC",
    "instType": "SPOT",
    "lastPrice": "1.878",
    "onlineTs": "1661149481000",
    "turnOver24h": "1032005.7397",
    "volume24h": "552933.5601"
}]


class MarketMaker(OkexBot):

    def __init__(self, details: list, APIKEY, APISECRET, PASS):
        super().__init__(APIKEY, APISECRET, PASS)
        self.details = details
        self.account_balance = self.check_balance()

    def open_position(self, size_of_balance: float):
        new_coin_id = self.details[0]["instId"]
        amount_of_usdc = [token['balance'] for token in self.check_balance() if token['id'] == "USDC"]
        usdc_to_order = float(amount_of_usdc[0]) * size_of_balance
        order = self.place_market_order(pair=new_coin_id, side='buy', amount=usdc_to_order).json()["data"]
        if len(order[0]['ordId']) < 1:
            print("ERROR - Failed to complete the transaction")
            print(order)
        else:
            print(f"Open succesfull new position - order number: {order[0]['ordId']}")
            order_details = self.get_info()[0]
            print(ord)
            # self.monitor_position()

    def monitor_position(self, order_info: list, size_of_profit: int, size_of_losses: int):
        purchase_price = float(order_info[0]['fillSz'])
        while True:
            current_price = self.check_price(order_info['instId'])
            if current_price >= purchase_price * (1 + size_of_profit):
                self.close_position(coin_id=order_info['instId'], size_of_sell=1)
            # what losses are acceptable??
            elif current_price <= purchase_price * (1 - size_of_losses):
                self.close_position(coin_id=order_info['instId'], size_of_sell=1)

    def close_position(self, coin_id: str, size_of_sell: float):
        quantity_of_token = [token['balance'] for token in self.check_balance() if token['id'] == coin_id.split("-")[0]]
        print(quantity_of_token)
        quantity_of_tokene_to_sell = float(quantity_of_token[0]) * size_of_sell
        order = self.place_market_order(pair=coin_id, side='sell', amount=quantity_of_tokene_to_sell).json()["data"]
        print(order)
        if len(order[0]['ordId']) < 1:
            print("ERROR - Failed to complete the transaction")
        # send notification ??


agent = MarketMaker(details=new_coin, APISECRET=APISECRET, APIKEY=APIKEY, PASS=PASS)
trans = agent.open_position(0.8)
