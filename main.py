import requests

url = "https://www.okx.com/priapi/v5/rubik/app/public/new-coin-rank?t=1661446882241&type=USDC"
input_a = requests.get(url).json()['data'][0]['online']
input_b = len(input_a)


def raise_new_coin(a, b):
    a = [tuple(sorted(d.items())) for d in a]
    b = [tuple(sorted(d.items())) for d in b]
    return [dict(kvs) for kvs in set(a).difference(b)]


def new_coin_alert(list_of_coins: list, n_of_coins: int):
    while True:
        new_list_of_coins = requests.get(url).json()['data'][0]['online']
        new_n_of_coins = len(requests.get(url).json()['data'][0]['online'])
        if new_n_of_coins > n_of_coins:
            new_coin = raise_new_coin(new_list_of_coins, list_of_coins)
            # function to call a traiding bot
            print("NEW COIN ALERT")
            new_coin_alert(new_list_of_coins, new_n_of_coins)
        print("SAME SHIT")


new_coin_alert(list_of_coins=input_a, n_of_coins=input_b)

