import base64
import datetime as dt
import hmac
import requests
import json
from decimal import Decimal
from os import getenv


APIKEY = getenv("APIKEY")
APISECRET = getenv("APISECRET")
PASS = getenv("PASS")


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
        return base64.b64encode(hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256').digest())

    def get_header(self, request='GET', endpoint='', body=''):
        cur_time = self.get_time()
        return {
            'CONTENT-TYPE': "application/json",
            'OK-ACCESS-KEY': self.apikey,
            'OK-ACCESS-SIGN': self.signature(cur_time, request, endpoint, body, self.apikey),
            'OK-ACCESS-TIMESTAMP': cur_time,
            'OK-ACCESS-PASSPHRASE': self.password,
        }

    def get_balance(self, currency: str):
        url = self.baseURL + "/api/v5/account/balance"
        header = self.get_header("GET", "/api/v5/account/balance")
        for obj in requests.get(url, headers=header).json()['data'][0]['details']:
            if obj['ccy'] != currency:
                continue

            return obj['availBal']

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