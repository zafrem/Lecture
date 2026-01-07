import _0_Coin_Data_getter as coin_data
import json
from datetime import datetime
import time


def init_json_file(filename):
    data = {
    }
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)  # indent=4 makes the JSON readable
    print(f"Data init successfully to {filename}.")


def load_data_json(filename):
    try:
        with open(filename, 'r') as file:
            loaded_data = json.load(file)
            return loaded_data
    except FileNotFoundError:
        print(f"{filename} not found. Starting with an empty dictionary.")
        return {}


def save_data_json(filename, price, percentage):
    data = load_data_json(filename)
    add_data = {datetime.today().strftime("%Y-%m-%d %H:%M:%S") : f"{price} ({percentage})"}
    data.update(add_data)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)  # indent=4 makes the JSON readable


if __name__ == "__main__":
    coin_name = "BTCUSDC"
    init_json_file(f"{coin_name}_info.json")

    current_info = 0.0
    past_info = 0.0
    percentage = 0.0

    while True:
        time.sleep(60 * 60 * 24)  # Daily

        past_info = current_info
        current_info = coin_data.get_altcoin_current_price(coin_name)
        if 0.0 != past_info:
            percentage = (current_info - past_info) / current_info * 100

        save_data_json(f"{coin_name}_info.json", current_info, percentage)
        print(load_data_json(f"{coin_name}_info.json"))

        # Add your own abort conditions.