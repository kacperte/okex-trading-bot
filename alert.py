import requests
from market_maker import MarketMaker


def new_coin_alert():
    url = "https://www.okx.com/priapi/v5/rubik/app/public/new-coin-rank?t=1661446882241&type=USDC"
    input_a = requests.get(url).json()['data'][0]['online']
    n_of_coins = len(input_a)
    while True:
        new_list_of_coins = requests.get(url).json()['data'][0]['online']
        new_n_of_coins = len(requests.get(url).json()['data'][0]['online'])
        if new_n_of_coins > n_of_coins:
            new_coin = [x for x in new_list_of_coins if x not in input_a]
            print(new_coin)
            input_a = new_list_of_coins
            n_of_coins = new_n_of_coins
            MarketMaker(details=new_coin)
            print("NEW COIN ALERT")

        print("Checking for new coin...")