# Post-Scraping (Analysis)
Let's write a quick note on how to analyze and present the data you extracted and stored.
This will hopefully serve as a foundation for using more and different methods.
## Technical Analysis
### [MACD](_1_technical_analysis_MACD.py)
MACD (Moving Average Convergence Divergence) is a popular technical analysis indicator used to identify trends and momentum in stock prices. It consists of three main components:  

1. **MACD Line** – The difference between the 12-day and 26-day exponential moving averages (EMA).  
2. **Signal Line** – A 9-day EMA of the MACD line, used to generate buy/sell signals.  
3. **Histogram** – The difference between the MACD line and the signal line, showing momentum strength.  

### How It Works:  
- When the MACD line crosses **above** the signal line, it’s a **bullish** signal (buy).  
- When the MACD line crosses **below** the signal line, it’s a **bearish** signal (sell).  
- The histogram helps visualize momentum—wider bars indicate stronger trends.  

It’s widely used to confirm trends and spot potential reversals.
### [Bollinger_band](_1_technical_analysis_Bollinger_band.py)
Bollinger Bands are a technical analysis tool used to measure market volatility and identify overbought or oversold conditions. They consist of three lines:  

1. **Middle Band** – A simple moving average (SMA), usually set to 20 periods.  
2. **Upper Band** – The middle band plus 2 standard deviations.  
3. **Lower Band** – The middle band minus 2 standard deviations.  

### How It Works:  
- When the price touches or moves **above** the upper band, the asset may be **overbought** (potential sell signal).  
- When the price touches or moves **below** the lower band, the asset may be **oversold** (potential buy signal).  
- **Bands expand** during high volatility and **contract** during low volatility, helping traders assess market conditions.  

It’s commonly used to spot breakouts and trend reversals.
### [Stochastic](_1_technical_analysis_Stochastic.py)
The **Stochastic Oscillator** is a momentum indicator used in technical analysis to identify overbought and oversold conditions in a stock or market. It compares the closing price to the price range over a specific period (usually 14 days).  

### Key Components:  
1. **%K Line** – The main stochastic line, showing the current price relative to the high-low range.  
2. **%D Line** – A 3-day moving average of %K, used as a signal line.  

### How It Works:  
- When %K crosses **above** %D and is below 20, it signals a **buy** (oversold condition).  
- When %K crosses **below** %D and is above 80, it signals a **sell** (overbought condition).  
- Strong trends may keep the oscillator in overbought/oversold zones for longer.  

It helps traders identify trend reversals and confirm price momentum.
### [Envelope](_1_technical_analysis_Envelope.py)
The **Envelope Indicator** is a technical analysis tool used to identify overbought and oversold conditions, as well as potential trend reversals. It consists of two bands (or lines) placed above and below a moving average, typically a **simple moving average (SMA)**.  

### Key Components:  
1. **Middle Line** – A moving average (e.g., 20-day SMA).  
2. **Upper Band** – A percentage (e.g., 2%) above the moving average.  
3. **Lower Band** – A percentage (e.g., 2%) below the moving average.  

### How It Works:  
- When the price **touches or breaks above** the upper band, the asset may be **overbought** (potential sell signal).  
- When the price **touches or breaks below** the lower band, the asset may be **oversold** (potential buy signal).  
- Prices tend to stay within the bands, and breakouts can signal strong trends.  

It helps traders confirm trends and detect price volatility.
### [AROON](_1_technical_analysis_AROON.py)
The **Aroon Indicator** is a technical analysis tool used to identify trends and measure the strength of a trend. It consists of two lines:  

### Key Components:  
1. **Aroon Up** – Measures how long since the highest price in a given period (usually 25 days).  
2. **Aroon Down** – Measures how long since the lowest price in the same period.  

### How It Works:  
- When **Aroon Up** is above 70 and **Aroon Down** is below 30, it signals a **strong uptrend**.  
- When **Aroon Down** is above 70 and **Aroon Up** is below 30, it signals a **strong downtrend**.  
- When both lines are low or move together, it suggests a **weak or sideways market**.  

It helps traders identify trend direction and potential reversals.
## [Create docx file](_2_Create_wordpress_file.py)

## [Create xlsx file](_3_Create_excel_file.py)

## [Gmail SMTP](_4_Gmail_Report.py)

## [Telegram bot](_5_Telegram_bot.py)
