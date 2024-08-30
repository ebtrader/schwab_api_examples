import time
from email import message_from_string

import schwabdev
from datetime import datetime, timedelta
from dotenv import load_dotenv
from time import sleep
import os
import pandas as pd
import json

# Initialize an empty DataFrame to store data
data_df = pd.DataFrame(columns=["message_time", "symbol", "content"])


def main():
    global data_df

    # place your app key and app secret in the .env file
    load_dotenv()  # load environment variables from .env file

    # create client
    client = schwabdev.Client(os.getenv('app_key'), os.getenv('app_secret'), os.getenv('callback_url'), tokens_file="tokens.json", timeout=15, verbose=True, update_tokens_auto=True)
    sleep(3)

    # print(client.quote("AMD").json())
    # sleep(3)

    sleep(3)

    streamer = client.stream

    def response_handler(response):
        global data_df  # Use the global dataframe
        print(response)
        message = json.loads(response)
        message_type = next(iter(message))
        print(message_type)

        if message_type == 'data':
            service = message.get('data', [])[0].get('service')
            message_time = message.get('data', [])[0].get('timestamp')
            content = message.get('data', [])[0].get('content', [{}])[0]  # Safely access nested keys
            symbol = content.get('key')

            # Print extracted information
            print(f"{message_time}")
            print(f"{symbol}")
            print(f"{content}")

            # Append new data to the dataframe
            new_data = pd.DataFrame({
                "message_time": [message_time],
                "symbol": [symbol],
                "content": [content]
            })
            data_df = pd.concat([data_df, new_data], ignore_index=True)

    streamer.start(response_handler)

    # Send a request to the streamer
    streamer.send(streamer.level_one_futures("/NQ", "0,1,2,3,4,5"))

    time.sleep(20)

    streamer.stop()


if __name__ == '__main__':
    print("Welcome to the unofficial Schwab interface!\nGithub: https://github.com/tylerebowers/Schwab-API-Python")
    main()

    # Save the dataframe to a file (optional)
    data_df.to_csv("schwab_data.csv", index=False)  # Save to CSV file
    print("Data saved to schwab_data.csv")

