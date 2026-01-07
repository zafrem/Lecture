import _0_Coin_Data_getter as coin_data
from datetime import datetime
import time


def save_data_text(filename, price, change_value):
    with open(filename, "a+", encoding="utf-8") as file:
        file.write(
            f"""{datetime.today().strftime("%Y-%m-%d %H:%M:%S")}|{price}|{change_value}\n""")


def load_data_text(filename):
    with open(filename, "r", encoding="utf-8") as read_file:
        while True:
            for lines in read_file.readlines():
                if not lines: break
                row = lines.rstrip("\n").split("|")
                print(f"Date : {row[0]}, Price : {row[1]}, Percentage : {row[2]}")
            read_file.close()
            break
        read_file.close()


if __name__ == "__main__":
    coin_name = "BTCUSDC"
    current_info = 0.0
    past_info = 0.0
    percentage = 0.0

    while True:
        time.sleep(10)#60 * 60 * 24)  # Daily

        past_info = current_info
        current_info = coin_data.get_altcoin_current_price(coin_name)
        if 0.0 != past_info:
            percentage = (current_info - past_info)/current_info * 100
        save_data_text(f"{coin_name}_info.txt", current_info, percentage)
        load_data_text(f"{coin_name}_info.txt")

        # Add your own abort conditions.