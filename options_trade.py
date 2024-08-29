import schwabdev
from datetime import datetime, timedelta
from dotenv import load_dotenv
from time import sleep
import os


def main():
    # place your app key and app secret in the .env file
    load_dotenv()  # load environment variables from .env file

    # create client
    client = schwabdev.Client(os.getenv('app_key'), os.getenv('app_secret'), os.getenv('callback_url'), tokens_file="tokens.json", timeout=5, verbose=False, update_tokens_auto=True)

    # print account hash
    account_hash = 'my-account-hash'
    # print(account_hash)
    sleep(3)

    # # get specific account positions (uses default account, can be changed)
    # print("|\n|client.account_details(account_hash, fields='positions').json()", end="\n|")
    # print(client.account_details(account_hash, fields="positions").json())
    # sleep(3)

    order = {"complexOrderStrategyType": "NONE", "orderType": "LIMIT", "session": "NORMAL", "duration": "DAY", "orderStrategyType": "SINGLE",
             "price": '0.30',
             "orderLegCollection": [
                 {"instruction": "BUY_TO_OPEN", "quantity": 1, "instrument": {"symbol": "SPY   240830C00561000", "assetType": "OPTION"}}]}


    resp = client.order_place(account_hash, order)
    print("|\n|client.order_place(account_hash, order).json()", end="\n|")
    print(f"Response code: {resp}")
    sleep(3)


if __name__ == '__main__':
    print("Welcome to the unofficial Schwab interface!\nGithub: https://github.com/tylerebowers/Schwab-API-Python")
    main()  # call the user code above

