import base64
import datetime as dt
import hmac
import requests
import json
from decimal import Decimal

APIKEY = "3d4ae0a2-6a2d-46f6-ad6c-1d74eb30c085"
APISECRET = "C81EF5582B8656D5F9666BB6CDF4ECF8"
PASS = "AZuM25SvkfvKBA3!"


class OkexBot:
    def __init__(self, APIKEY: str, APISECRET: str, PASS: str):
        self.apikey = APIKEY
        self.apisecret = APISECRET
        self.password = PASS
        self.baseURL = 'https://www.okex.com'

    @staticmethod
    def check_price(id: str):
        ticker = requests.get(f'https://okex.com/api/v5/market/ticker?instId={id}').json()
        return ticker['data'][0]['last']

    @staticmethod
    def get_time():
        return dt.datetime.utcnow().isoformat()[:-3] + 'Z'

    @staticmethod
    def signature(timestamp, method, request_path, body, secret_key):
        message = timestamp + method + request_path + body
        mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        output = mac.digest()
        return base64.b64encode(output)

    def get_header(self, request='GET', endpoint='', body=''):
        cur_time = self.get_time()
        header = dict()
        header['CONTENT-TYPE'] = "application/json"
        header['OK-ACCESS-KEY'] = APIKEY
        header['OK-ACCESS-SIGN'] = self.signature(cur_time, request, endpoint, body, APISECRET)
        header['OK-ACCESS-TIMESTAMP'] = cur_time
        header['OK-ACCESS-PASSPHRASE'] = PASS
        return header

    def check_balance(self):
        url = self.baseURL + "/api/v5/account/balance"
        header = self.get_header("GET", "/api/v5/account/balance")
        response = requests.get(url, headers=header).json()['data'][0]['details']
        balance_status = list()
        for obj in response:
            temp_dict = dict()
            temp_dict['id'] = obj['ccy']
            temp_dict['balance'] = obj['availBal']
            balance_status.append(temp_dict)

        return balance_status

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
        header = self.get_header(request, endpoint, str(body))
        response = requests.post(url, headers=header, data=body)
        return response

    def get_info(self, ):
        url = self.baseURL + "/api/v5/trade/fills"
        header = self.get_header("GET", "/api/v5/trade/fills")
        balance_status = requests.get(url, headers=header).json()
        return balance_status["data"]


bot = OkexBot(APIKEY=APIKEY, APISECRET=APISECRET, PASS=PASS)
print(bot.get_info())

