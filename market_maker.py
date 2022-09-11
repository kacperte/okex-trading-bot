from bot import OkexBot, APISECRET, APIKEY, PASS

new_coin = {
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
}

order = {
    "side": "buy",
    "fillSz": "0.106",
    "fillPx": "7.824",
    "fee": "-0.0000742",
    "ordId": "489313426288824330",
    "instType": "SPOT",
    "instId": "LINK-USDC",
    "clOrdId": "",
    "posSide": "net",
    "billId": "489313426330767367",
    "tag": "",
    "execType": "T",
    "tradeId": "646741",
    "feeCcy": "LINK",
    "ts": "1662933411841"
}


class MarketMaker(OkexBot):

    def __init__(self, details: dict, APIKEY, APISECRET, PASS):
        super().__init__(APIKEY, APISECRET, PASS)
        self.details = details
        self.account_balance = self.check_balance()

    def open_position(self, size_of_balance: float):
        print(self.account_balance)
        new_coin_id = self.details["instId"]
        amount_of_usdt = float(self.check_balance()[0]['balance']) * size_of_balance
        order = self.place_market_order(pair=new_coin_id, side='buy', amount=amount_of_usdt).json()["data"]
        if len(order[0]['ordId']) < 1:
            print("ERROR - Failed to complete the transaction")
        self.account_balance = self.check_balance()

    def monitor_position(self, order_info: dict, size_of_profit: int, size_of_losses: int):
        purchase_price = float(order_info['fillSz'])
        while True:
            current_price = self.check_price(order_info['instId'])
            if current_price >= purchase_price * (1 + size_of_profit):
                self.close_position()
            # what losses are acceptable
            elif current_price <= purchase_price * (1 - size_of_losses):
                self.close_position()

    def close_position(self):
        pass
        # sell all assets
        # update balance
        # send notification


agent = MarketMaker(details=new_coin, APISECRET=APISECRET, APIKEY=APIKEY, PASS=PASS)
trans = agent.open_position(0.1)
