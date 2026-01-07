# Post-Scraping (Analysis)

Once data has been collected and stored, the next step is to analyze and present it effectively. This section demonstrates how to apply various technical analysis indicators to your data and how to automate the generation and distribution of reports.

## Technical Analysis

These modules utilize **pandas** for data manipulation and **matplotlib** for visualization. They generally expect a DataFrame with a `Price` column.

### Moving Average Convergence Divergence (MACD)

MACD is a momentum indicator that identifies trends by comparing short-term and long-term exponential moving averages.

<details>
<summary>View Code: MACD Implementation</summary>

```python
def macd(_df, period_long=26, period_short=12, period_signal=9, column='Price'):
    # Calculate Short and Long term EMAs
    ShortEMA = _df[column].ewm(span=period_short, adjust=False).mean()
    LongEMA = _df[column].ewm(span=period_long, adjust=False).mean()
    
    # MACD Line
    _df['MACD'] = ShortEMA - LongEMA
    # Signal Line (EMA of the MACD Line)
    _df['Signal_Line'] = _df['MACD'].ewm(span=period_signal, adjust=False).mean()

    # Plotting logic using matplotlib...
```
</details>

*   **MACD Line**: Difference between the 12-day and 26-day EMAs.
*   **Signal Line**: 9-day EMA of the MACD line, used for buy/sell signals.
*   **Analysis**: A cross above the signal line is bullish, while a cross below is bearish.

---

### Bollinger Bands

Bollinger Bands measure market volatility and identify overbought or oversold conditions.

<details>
<summary>View Code: Bollinger Band Implementation</summary>

```python
def bollinger_band(_df, period=20):
    # Middle Band (Simple Moving Average)
    _df['SMA'] = _df['Price'].rolling(window=period).mean()
    # Standard Deviation
    _df['SD'] = _df['Price'].rolling(window=period).std()

    # Upper and Lower Bands
    _df['Upper'] = _df['SMA'] + 2 * _df['SD']
    _df['Lower'] = _df['SMA'] - 2 * _df['SD']

    # Plotting logic using matplotlib...
```
</details>

*   **Middle Band**: Usually a 20-day Simple Moving Average (SMA).
*   **Upper/Lower Bands**: Placed 2 standard deviations away from the middle band.
*   **Analysis**: Prices near the upper band suggest overbought conditions, while prices near the lower band suggest oversold conditions.

---

### Stochastic Oscillator

The Stochastic Oscillator compares a closing price to its price range over a specific period to identify momentum.

<details>
<summary>View Code: Stochastic Implementation</summary>

```python
def stochastic(_df, period=14):
    _df['LP'] = _df['Low'].rolling(window=period).min()
    _df['HP'] = _df['High'].rolling(window=period).max()

    # %K Line
    _df['K'] = 100 * ((_df['Price'] - _df['LP']) / (_df['HP'] - _df['LP']))
    # %D Line (Signal Line)
    _df['D'] = _df['K'].rolling(window=3).mean()

    # Plotting logic using matplotlib...
```
</details>

*   **%K Line**: Current price relative to the high-low range.
*   **%D Line**: A 3-day moving average of %K.
*   **Analysis**: Values below 20 are oversold; values above 80 are overbought.

---

### Envelope Indicator

Envelopes are percentage-based bands set around a moving average.

<details>
<summary>View Code: Envelope Implementation</summary>

```python
def envelope(_df, period=20):
    _df['MA'] = _df['Price'].rolling(window=period).mean()
    ev = 0.025  # 2.5% envelope percentage

    _df["Upper"] = _df["MA"] * (1 + ev)
    _df["Lower"] = _df["MA"] * (1 - ev)

    # Plotting logic using matplotlib...
```
</details>

*   **Bands**: Set at a fixed percentage (e.g., 2.5%) above and below an SMA.
*   **Analysis**: Helps confirm trends and detect when a price is moving too far from its average.

---

### Aroon Indicator

Aroon measures the time between highs and lows to determine trend strength and direction.

<details>
<summary>View Code: Aroon Implementation</summary>

```python
def aroon(_df, period=25):
    # Measures time since highest/lowest prices
    _df['Up'] = 100 * _df.High.rolling(period + 1).apply(lambda x: x.argmax()) / period
    _df['Down'] = 100 * _df.Low.rolling(period + 1).apply(lambda x: x.argmin()) / period

    # Plotting logic using matplotlib...
```
</details>

*   **Aroon Up/Down**: Indicates the strength of the uptrend and downtrend respectively.
*   **Analysis**: High Aroon Up (>70) combined with low Aroon Down (<30) indicates a strong uptrend.

---

## Reporting & Automation

These modules handle the export of analyzed data into various formats and automate communication.

### Word & Excel Reporting

Utilizes `python-docx` for document generation and `xlsxwriter` for Excel spreadsheets.

<details>
<summary>View Code: Word Report Generation</summary>

```python
from docx import Document

document = Document()
document.add_heading('Analysis Report', level=1)
document.add_paragraph('Automated report content...')
document.add_picture('plot.png')
document.save('report.docx')
```
</details>

### Email Distribution (SMTP)

Automates sending reports via Gmail's SMTP server using the `smtplib` library. Supports attachments for both images and documents.

<details>
<summary>View Code: Gmail SMTP Automation</summary>

```python
import smtplib
from email.mime.multipart import MIMEMultipart

# Configure SMTP server and credentials
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(username, password)
server.send_message(message)
```
</details>

### Telegram Bot Integration

Leverages the `python-telegram-bot` library to provide an interactive interface for requesting data or receiving automated alerts and images.

<details>
<summary>View Code: Telegram Bot Implementation</summary>

```python
from telegram.ext import Application, CommandHandler

async def image_command(update, context):
    # Logic to generate and send a plot to the user
    await context.bot.send_document(chat_id=update.message.chat_id, document=open('plot.png', 'rb'))

application = Application.builder().token(token).build()
application.add_handler(CommandHandler("image", image_command))
```
</details>