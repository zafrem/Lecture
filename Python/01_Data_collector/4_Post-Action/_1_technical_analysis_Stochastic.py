import _0_File_to_Get_data as get_data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def init_pre_df():
    row_data = get_data.get_file_data()
    _df = pd.DataFrame(row_data, columns=['datetime', 'Price', 'persent'])

    _df["Price"] = _df.Price.astype(float)

    # Creating virtual data
    _df['High'] = _df['Price'] - np.random.randint(1, 200, _df.shape[0])
    _df['Low'] = _df['Price'] - np.random.randint(1, 200, _df.shape[0])

    return _df


def stochastic(_df, period=14):
    _df['LP'] = _df['Low'].rolling(window=period).min()
    _df['HP'] = _df['High'].rolling(window=period).max()

    _df['K'] = 100*((_df['Price'] - _df['LP']) / (_df['HP'] - _df['LP']) )
    _df['D'] = _df['K'].rolling(window=3).mean()

    ax = plt.gca()

    _df.K.plot(figsize = (18,8), color='red', ax=ax)
    _df.D.plot(color = 'blue', ax=ax)

    plt.grid(alpha=0.3, linestyle=':', linewidth=2)

    plt.xlabel('Date', fontsize=17)
    plt.ylabel('Stochastic', fontsize=17)

    plt.title('Stochastic Oscillator', position=(0.5, 1.05), fontsize=23)

    plt.legend(loc='upper left', fontsize=13)

    return plt, _df


if "__main__" == __name__:
    df = init_pre_df()
    plt, df = stochastic(df)
    plt.show()

