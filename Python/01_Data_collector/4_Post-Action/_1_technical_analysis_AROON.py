# Virtual - High & Low Data
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


# AROON
def aroon(_df, period=25):

    _df['Up'] = 100 * _df.High.rolling(period + 1).apply(lambda x: x.argmax()) / period
    _df['Down'] = 100 * _df.Low.rolling(period + 1).apply(lambda x: x.argmin()) / period

    ax = plt.gca()

    _df.plot(figsize=(18, 8), kind='line', x='datetime', y='Up', color='red', ax=ax)
    _df.plot(kind='line', x='datetime', y='Down', color='blue', ax=ax)

    plt.grid(alpha=0.3, linestyle=':', linewidth=2)

    plt.xlabel('Date', fontsize=17)
    plt.ylabel('Stochastic', fontsize=17)

    plt.title('AROON', position=(0.5, 1.05), fontsize=23)

    plt.legend(loc='upper left', fontsize=13)

    plt.gcf().autofmt_xdate()

    return plt, _df


if "__main__" == __name__:
    df = init_pre_df()
    plt, df = aroon(df)
    plt.show()
