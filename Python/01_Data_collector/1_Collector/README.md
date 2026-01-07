# Code for life
## Example code
1. [Stock - yfinance](_1_API_Stock_Funds_yfinance.py)
2. [Stock - pandas_datareader](_2_API_Stock_pandas_datareader.py)
3. [Altcoin - binance](_3_API_AltCoin_binance.py)
4. [Trend Keyword - Google Trend](_4_RSS_Trend_Keyword_Google_trend.py)
5. [Trend Keyword - Blackkiwi](_5_Scraping_Trend_Keyword_Blackkiwi.py)
6. [Spot-NFL](_6_Scraping_Spot_NFL.py)
7. [Spot-Premier League](_7_Scraping_Spot_Premier_League.py)
8. [Weather](_8_Scraping_Weather_windy.py)

## Descriptions
### Stock - yfinance
#### Step 1. Pypi Yahoo! Finance's API
  * Site : https://pypi.org/project/yfinance/
#### Step 2. pip package install
<code>
$ pip install yfinance
</code>

#### Step 3. Github.io
  * https://ranaroussi.github.io/yfinance/index.html
#### Step 4. Example Code
  * [API_Stock_Funds_yfinance.py](_1_API_Stock_Funds_yfinance.py)

### Stock - pandas_datareader
#### Step 1. Pypi Pandas Datareader
  * https://pypi.org/project/pandas-datareader/
#### Step 2. pip package install
<code>
pip install pandas-datareader
</code>

#### Step 3. Example Code
  * [API_Stock_pandas_datareader.py](_2_API_Stock_pandas_datareader.py)

### Altcoin - binance
#### Step 1. Binance APIs
  * [API Data Document](https://developers.binance.com/docs/binance-spot-api-docs/rest-api#market-data-endpoints)

#### Step 2. Default packages install
<code>
pip install requests
</code>

#### Step 3. Example Code
  * [API_AltCoin_binance.py](_3_API_AltCoin_binance.py)

### Trend Keyword - Google Trend
#### Step 1. Google Trend > Trending now 
<img src="./images/Trend_google_1.jpg" title="in file"/>

#### Step 2. Select RSS Feed 
I have an RSS Feed, not Scraping, so I put that in too. If you have RSS, this is the way to go. 
<img src="./images/Trend_google_2.jpg" title="in file"/>

#### Step 3. Get RSS feed URL
<img src="./images/Trend_google_3.jpg" title="in file"/>

#### Step 4. Other National information
<img src="./images/Trend_google_4.jpg" title="in file"/>

#### Step 5. Example Code
  * [RSS_Trend_Keyword_Google_trend.py](_4_RSS_Trend_Keyword_Google_trend.py)

#### Step 6. Cmd stdout
<img src="./images/Trend_google_5.jpg" title="in file"/>
<img src="./images/Trend_google_6.jpg" title="in file"/>

### NFL Schedule
#### Step 1. NFL Web page
<img src="./images/NFL_1.jpg" title=""/>

#### Step 2. Mouse right button click, Inspect select
<img src="./images/NFL_2.jpg" title=""/>

#### Step 3. Match code and text
<img src="./images/NFL_3.jpg" title=""/>

#### Step 4. Copy Full XPath
<img src="./images/NFL_4.jpg" title=""/>

#### Step 5. Two type information
<img src="./images/NFL_5.jpg" title=""/>

#### Step 6. Parsing string
<img src="./images/NFL_6.jpg" title=""/>

#### Step 7. Chrome selenium mode (Automation test mode)
<img src="./images/NFL_7.jpg" title=""/>

#### Step 8. Example Code
  * [Scraping_Spot_NFL.py](_6_Scraping_Spot_NFL.py)

#### Step 9. Cmd stdout
<img src="./images/NFL_8.jpg" title=""/>

### Premier League Schedule
#### Step 1. Premier League Web page target
<img src="./images/Premier_league_1.jpg" title=""/>

#### Step 2. Mouse right button click, Inspect select
<img src="./images/Premier_league_2.jpg" title=""/>

#### Step 3. Match Web and Code
<img src="./images/Premier_league_3.jpg" title=""/>

#### Step 4. Two type information
<img src="./images/Premier_league_4.jpg" title=""/>

#### Step 5. Finished and upcoming matches
<img src="./images/Premier_league_5.jpg" title=""/>

#### Step 6. Merge two 
<img src="./images/Premier_league_6.jpg" title=""/>

#### Step 7. Chrome selenium mode (Automation test mode)
<img src="./images/Premier_league_7.jpg" title=""/>

#### Step 8. Example Code
  * [Scraping_Spot_Premier_League.py](_7_Scraping_Spot_Premier_League.py)

#### Step 9. Cmd stdout
<img src="./images/Premier_league_8.jpg" title=""/>

### Weather
#### Step 1. Weather Web site 
<img src="./images/Weather_1.jpg" title=""/>

#### Step 2. Mouse right button click, Inspect select
<img src="./images/Weather_2.jpg" title=""/>

#### Step 3. Target city
<img src="./images/Weather_3.jpg" title=""/>

#### Step 4. Arrow down and Return key
<img src="./images/Weather_4.jpg" title=""/>

#### Step 5. Change city
<img src="./images/Weather_5.jpg" title=""/>

#### Step 6. Code copy
<img src="./images/Weather_6.jpg" title=""/>

#### Step 7. Detect iframe 
<img src="./images/Weather_7.jpg" title=""/>

#### Step 8. Switch iframe
<img src="./images/Weather_8.jpg" title=""/>

#### Step 9. Chrome selenium mode (Automation test mode)
<img src="./images/Weather_9.jpg" title=""/>

#### Step 10. Example Code
  * [Scraping_Weather_windy.py](_8_Scraping_Weather_windy.py)

#### Step 11. Cmd stdout
<img src="./images/Weather_10.jpg" title=""/>