import base64
import datetime as dt
import hmac
import requests
import json
from decimal import Decimal

APIKEY = ""
APISECRET = ""
PASS = ""


class OkexBot:
    def __init__(self, APIKEY: str, APISECRET: str, PASS: str):
        self.apikey = APIKEY
        self.apisecret = APISECRET
        self.password = PASS
        self.baseURL = 'https://okex.com'

    @staticmethod
    def check_price(id: str):
        ticker = requests.get(f'https://okex.com/api/v5/market/ticker?instId={id}-SWAP').json()
        return ticker['data'][0]['last']

    @staticmethod
    def get_time():
        return dt.datetime.utcnow().isoformat()[:-3] + 'Z'

    @staticmethod
    def signature(timestamp, method, request_path, body, secret_key):
        if str(body) == '{}' or str(body) == 'None':
            body = ''
        message = str(timestamp) + str.upper(method) + request_path + str(body)
        mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        output = mac.digest()
        return base64.b64encode(output)

    def get_header(self, request='GET', endpoint='', body: dict = dict()):
        cur_time = self.get_time()
        header = dict()
        header['CONTENT-TYPE'] = 'application/json'
        header['OK-ACCESS-KEY'] = APIKEY
        header['OK-ACCESS-SIGN'] = self.signature(cur_time, request, endpoint, body, APISECRET)
        header['OK-ACCESS-TIMESTAMP'] = str(cur_time)
        header['OK-ACCESS-PASSPHRASE'] = PASS
        return header

    def check_balance(self):
        url = self.baseURL + "/api/v5/asset/balances"
        header = self.get_header("GET", "/api/v5/asset/balances")
        balance_status = requests.get(url, headers=header).json()
        return balance_status['data']

    def place_market_order(self, pair, side, amount, tdMode='cash'):
        endpoint = '/api/v5/trade/order'
        url = self.baseURL + '/api/v5/trade/order'
        request = 'POST'
        body = {
            "instId": pair,
            "tdMode": tdMode,
            "side": side,
            "ordType": "market",
            "sz": str(Decimal(str(amount)))
        }

        body = json.dumps(body)
        header = self.get_header(endpoint, request, body)
        response = requests.post(url, headers=header, data=body)
        return response


bot = OkexBot(APIKEY=APIKEY, APISECRET=APISECRET, PASS=PASS)
#print(bot.place_market_order("ETH-BTC"))
print(bot.check_price("XRP-BTC"))

