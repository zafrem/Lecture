import _0_File_to_Get_data as get_data
import pandas as pd
import matplotlib.pyplot as plt


def init_pre_df():
    row_data = get_data.get_file_data()
    _df = pd.DataFrame(row_data, columns=['datetime', 'Price', 'persent'])

    # Creating virtual data
    _df["Price"] = _df.Price.astype(float) - 100000

    return _df


# Envelope
def envelope(_df, period=20):
    _df['MA'] = _df['Price'].rolling(window=period).mean()

    ev = 0.025  # envelope persentage

    _df["Upper"] = _df["MA"] * (1 + ev)
    _df["Lower"] = _df["MA"] * (1 - ev)

    ax = plt.gca()

    _df.plot(figsize=(18, 8), kind='line', x='datetime', y='Upper', color='red', ax=ax)
    _df.plot(kind='line', x='datetime', y='Price', color='black', ax=ax)
    _df.plot(kind='line', x='datetime', y='Lower', color='blue', ax=ax)

    plt.grid(alpha=0.3, linestyle=':', linewidth=2)

    plt.xlabel('Date', fontsize=17)
    plt.ylabel('Envelope', fontsize=17)

    plt.title('Envelope', position=(0.5, 1.05), fontsize=23)

    plt.legend(loc='upper left', fontsize=13)

    plt.gcf().autofmt_xdate()


plt.show()
