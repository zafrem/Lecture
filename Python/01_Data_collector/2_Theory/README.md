# Theory
## API, RSS, Crawling and Scraping

**API** 

**RSS** 

**Crawling** is the process of systematically browsing the web to discover and index pages. It is primarily used by search engines like Google to find new and updated content across the internet. Crawlers, also known as spiders or bots, navigate through web pages by following links. The goal is to create an up-to-date index of websites for search engines, so they can efficiently provide relevant results to users.

**Scraping**, on the other hand, involves extracting specific information from web pages. Scraping targets the content of a page, often for analysis or to make use of the data in some other context, like building price comparison tools. Web scrapers are designed to access a specific site, parse its HTML, and extract structured information like product details, prices, or reviews.

In summary, crawling is about discovering and indexing web content, while scraping is about extracting targeted data from specific sites.

## API
Stock Library
1. yfinance · 2. pandas-datareader · 3. Theta Data · 4. Alpha Vantage · 5. Finnhub · 6. Nasdaq Data Link (formerly Quandl) · 7. Twelve Data · 8. IBApi

## Scraping
### Static (requests)
How to use the requests library in Python to send an HTTP GET request and work with the response.

```python
    import requests
    
    # Step 1: Define the URL
    url = "https://blog.codeforlife.xyz/2024/06/request-python.html"
    
    # Step 2: Send a GET request
    response = requests.get(url)
    
    # Step 3: Check the response status
    if response.status_code == 200:
        print("Request was successful!")
    else:
        print(f"Request failed with status code: {response.status_code}")
    
    # Step 4: Parse the JSON response
    data = response.json()
    
    # Step 5: Display the data
    print("\nResponse JSON Data:")
    print(data)
    
    # Access specific fields from the JSON response
    print("\nTitle of the Post:")
    print(data["title"])
```
### Dynamic (selenium)
Simple example to demonstrate how to use Python's selenium library to automate web browsing. 
```python
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    
    # Step 1: Set up the WebDriver (e.g., for Chrome)
    driver = webdriver.Chrome()  # Make sure you have the ChromeDriver installed
    
    # Step 2: Open a webpage
    url = "https://www.google.com"
    driver.get(url)
    
    # Step 3: Find the search box element
    search_box = driver.find_element(By.NAME, "q")
    
    # Step 4: Interact with the search box (e.g., enter a query and press Enter)
    search_box.send_keys("Python selenium tutorial")
    search_box.send_keys(Keys.RETURN)
    
    # Step 5: Wait for the results to load and print the title of the page
    print("Page title after search:", driver.title)
    
    # Step 6: Close the browser
    driver.quit()
```
## RSS feed
Simple example of how to read and parse an RSS feed using Python. The feedparser library is commonly used for this purpose.
```python
    import feedparser
    
    # Step 1: Define the RSS feed URL
    rss_url = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"  # Example RSS feed
    
    # Step 2: Parse the RSS feed
    feed = feedparser.parse(rss_url)
    
    # Step 3: Display feed information
    print("Feed Title:", feed.feed.title)
    print("Feed Link:", feed.feed.link)
    print("Feed Description:", feed.feed.description)
    
    print("\nTop Articles:")
    # Step 4: Loop through the entries (articles)
    for entry in feed.entries[:5]:  # Limit to the top 5 articles
        print("\nTitle:", entry.title)
        print("Link:", entry.link)
        print("Published:", entry.published)
```
## API
How to perform GET and POST requests with a token-based authentication using Python's requests library.
```python
    import requests
    
    # API Base URL
    base_url = "https://example.com/api"  # Replace with your API base URL
    
    # Your authentication token
    auth_token = "your_token_here"
    
    # Headers with the authorization token
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    
    # ----------------------------
    # Step 1: Perform a GET Request
    # ----------------------------
    # Example endpoint to fetch data
    get_url = f"{base_url}/data"
    response = requests.get(get_url, headers=headers)
    
    # Check if the GET request was successful
    if response.status_code == 200:
        print("GET Request Successful!")
        print("Response JSON:", response.json())
    else:
        print(f"GET Request Failed with status code: {response.status_code}")
    
    # ----------------------------
    # Step 2: Perform a POST Request
    # ----------------------------
    # Example endpoint to create a resource
    post_url = f"{base_url}/data"
    data = {
        "name": "Test Item",
        "description": "This is a test item created via API.",
        "price": 19.99
    }
    
    post_response = requests.post(post_url, headers=headers, json=data)
    
    # Check if the POST request was successful
    if post_response.status_code == 201:
        print("\nPOST Request Successful!")
        print("Response JSON:", post_response.json())
    else:
        print(f"POST Request Failed with status code: {post_response.status_code}")
```
