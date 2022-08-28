import requests
from test_json import test_json_1
from test_json import test_json_2


url = "https://www.okx.com/priapi/v5/rubik/app/public/new-coin-rank?t=1661446882241&type=USDC"
input_a = requests.get(url).json()['data'][0]['online']
input_b = len(input_a)


def new_coin_alert(list_of_coins: list, n_of_coins: int):
    while True:
        new_list_of_coins = requests.get(url).json()['data'][0]['online']
        new_n_of_coins = len(requests.get(url).json()['data'][0]['online'])
        if new_n_of_coins > n_of_coins:
            new_coin = [x for x in new_list_of_coins if x not in list_of_coins]
            # function to call a traiding bot
            print("NEW COIN ALERT")
            new_coin_alert(new_list_of_coins, new_n_of_coins)
        print("SAME SHIT")


new_coin_alert(list_of_coins=input_a, n_of_coins=input_b)

