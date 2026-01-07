import _0_File_to_Get_data as get_data
import pandas as pd
import matplotlib.pyplot as plt

def init_pre_df():
    row_data = get_data.get_file_data()
    _df = pd.DataFrame(row_data, columns=['datetime', 'Price', 'persent'])

    # Creating virtual data
    _df["Price"] = _df.Price.astype(float) - 100000
    return _df


# Bollinger Band
def bollinger_band(_df, period=20):
    # 20-windows Simple Moving Average (SMA)
    _df['SMA'] = _df['Price'].rolling(window=period).mean()

    # 20-windows Standard Deviation (SD)
    _df['SD'] = _df['Price'].rolling(window=period).std()

    # Upper Bollinger Band (UB) and Lower Bollinger Band (LB)
    _df['Upper'] = _df['SMA'] + 2 * _df['SD']
    _df['Lower'] = _df['SMA'] - 2 * _df['SD']

    ax = plt.gca()

    _df.plot(figsize = (18,8), kind='line', x='datetime', y='Upper', color='red', ax=ax)
    _df.plot(kind='line', x='datetime', y='Price', color='black', ax=ax)
    _df.plot(kind='line', x='datetime', y='Lower', color='blue', ax=ax)

    plt.grid(alpha=0.3, linestyle=':', linewidth=2)

    plt.xlabel('Date', fontsize=17)
    plt.ylabel('Bollinger band', fontsize=17)

    plt.title('Bollinger Band', position=(0.5, 1.05), fontsize=23)

    plt.legend(loc='upper left', fontsize=13)

    plt.gcf().autofmt_xdate()
    return plt, _df


if "__main__" == __name__:
    df = init_pre_df()
    plt, df = bollinger_band(df)
    plt.show()