# MACD (Moving Average Convergence & Divergence)
import _0_File_to_Get_data as get_data
import pandas as pd
import matplotlib.pyplot as plt


def init_pre_df():
    row_data = get_data.get_file_data()
    _df = pd.DataFrame(row_data, columns=['datetime', 'Price', 'persent'])

    # Creating virtual data
    _df["Price"] = _df.Price.astype(float) - 100000
    return _df


def macd(_df, period_long = 26, period_short = 12, period_signal = 9, column = 'Price'):
    ShortEMA = _df[column].ewm(span=period_short, adjust=False).mean()
    LongEMA = _df[column].ewm(span=period_long, adjust=False).mean()
    _df['MACD'] = ShortEMA - LongEMA  + 2800 # virtual data
    #_df['MACD'] = ShortEMA - LongEMA # default
    _df['Signal_Line'] = _df[column].ewm(span=period_signal, adjust=False).mean()

    ax = plt.gca()

    _df.plot(figsize=(18, 8), kind='line', x='datetime', y='MACD', color='red', ax=ax)
    _df.plot(kind='line', x='datetime', y='Signal_Line', color='black', ax=ax)
    plt.grid(alpha=0.3, linestyle=':', linewidth=2)

    plt.xlabel('Date', fontsize=17)
    plt.ylabel('MACD', fontsize=17)

    plt.title('MACD', position=(0.5, 1.05), fontsize=23)

    plt.legend(loc='upper left', fontsize=13)

    plt.gcf().autofmt_xdate()

    return plt, _df


if "__main__" == __name__:
    df = init_pre_df()
    plt, df = macd(df)
    plt.show()