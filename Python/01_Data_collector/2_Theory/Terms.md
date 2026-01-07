# Terms
## Html
### **What is HTML?**

HTML (HyperText Markup Language) is the standard markup language used to create and design web pages. 
It structures the content on the web, such as text, images, videos, and links. 
HTML uses "tags" enclosed in angle brackets (`<>`) to define elements like headings, paragraphs, lists, and more.

---

#### **Key Characteristics of HTML**
1. **Structure**: Organizes content on a web page.
2. **Tags**: HTML uses tags to denote elements (e.g., `<p>` for paragraphs, `<h1>` for headings).
3. **Attributes**: Tags can have attributes to provide additional information (e.g., `<a href="url">` specifies a hyperlink).
4. **Platform-Independent**: Works across all browsers and platforms.

---

#### **Basic Example of HTML**

Here is a simple HTML document:

```html
<!DOCTYPE html>
<html>
<head>
    <title>My First HTML Page</title>
</head>
<body>
    <h1>Welcome to My Website</h1>
    <p>This is a simple HTML page example.</p>
    <a href="https://www.example.com" target="_blank">Visit Example</a>
    <ul>
        <li>HTML</li>
        <li>CSS</li>
        <li>JavaScript</li>
    </ul>
    <img src="https://via.placeholder.com/150" alt="Placeholder Image">
</body>
</html>
```

---

#### **Explanation of the Example**

1. **`<!DOCTYPE html>`**:
   - Declares the document type as HTML5.

2. **`<html>`**:
   - The root element that wraps all content.

3. **`<head>`**:
   - Contains metadata about the document (e.g., title, styles).

4. **`<title>`**:
   - Specifies the title of the web page, displayed on the browser tab.

5. **`<body>`**:
   - Contains the visible content of the web page.

6. **Common Tags**:
   - `<h1>`: A heading (level 1).
   - `<p>`: A paragraph.
   - `<a href="url">`: A hyperlink to another webpage.
   - `<ul>`: An unordered list with `<li>` items.
   - `<img src="url">`: Embeds an image.

#### **How It Looks in a Browser**

When viewed in a browser, the example above will display:

**Title (in browser tab)**: My First HTML Page

**Body Content**:
- A large heading: "Welcome to My Website"
- A paragraph: "This is a simple HTML page example."
- A hyperlink: "Visit Example" (clickable link).
- A bullet-point list:
  - HTML
  - CSS
  - JavaScript
- An image placeholder.

## requests
### **What is `requests` in Python?**

The `requests` library in Python is a powerful and easy-to-use HTTP library for sending HTTP/1.1 requests to web servers. It allows developers to interact with web services, APIs, or even web pages by making HTTP requests such as GET, POST, PUT, DELETE, and more.

Unlike Python's built-in `urllib` module, `requests` simplifies the process of sending HTTP requests and handling responses, making it one of the most popular libraries for web development and API integration.

---

### **Key Features of `requests`**
1. **Human-Friendly API**: Easy-to-use functions and a clear syntax.
2. **HTTP Methods**: Supports all common HTTP methods like GET, POST, PUT, DELETE, HEAD, and OPTIONS.
3. **Automatic Decoding**: Handles response decoding (e.g., JSON or text) automatically.
4. **Headers and Cookies**: Easily include headers, authentication, and cookies.
5. **Session Support**: Manages persistent sessions and connections.
6. **Timeouts and Exceptions**: Built-in support for connection timeouts and exception handling.
7. **SSL Support**: Automatically handles HTTPS requests.

---

### **Basic Example**

```python
import requests

# Example URL
url = "https://jsonplaceholder.typicode.com/posts/1"

# Sending a GET request
response = requests.get(url)

# Check the status code
if response.status_code == 200:
    print("Request was successful!")
    print("Response JSON:", response.json())
else:
    print(f"Failed with status code: {response.status_code}")
```

---

### **Explanation**

1. **`requests.get(url)`**:
   - Sends a GET request to the specified `url`.
   - Returns a `Response` object that contains the server's response.

2. **`response.status_code`**:
   - HTTP status code (e.g., `200` for success, `404` for not found).

3. **`response.json()`**:
   - Parses the response as JSON and returns a Python dictionary.

---

### **Commonly Used HTTP Methods**

1. **GET**: Retrieve data from a server.
   ```python
   import requests
   response = requests.get("https://api.example.com/data")
   ```

2. **POST**: Send data to a server.
   ```python
   import requests
   payload = {"name": "John", "age": 30}
   response = requests.post("https://api.example.com/create", json=payload)
   ```

3. **PUT**: Update data on a server.
   ```python
   import requests
   payload = {"name": "John", "age": 31}
   response = requests.put("https://api.example.com/update/1", json=payload)
   ```

4. **DELETE**: Remove data from a server.
   ```python
   import requests
   response = requests.delete("https://api.example.com/delete/1")
   ```

---

### **Headers and Authentication**

- Add custom headers:
  ```python
  import requests
  headers = {"Authorization": "Bearer YOUR_TOKEN"}
  response = requests.get("https://api.example.com/data", headers=headers)
  ```

- Basic Authentication:
  ```python
  import requests
  response = requests.get("https://api.example.com/secure", auth=('username', 'password'))
  ```

---

### **Advanced Features**

1. **Handling Cookies**:
   ```python
   import requests
   response = requests.get("https://example.com", cookies={"session_id": "12345"})
   ```

2. **Timeouts**:
   ```python
   import requests
   response = requests.get("https://example.com", timeout=5)  # Wait for max 5 seconds
   ```

3. **Session Management**:
   ```python
   import requests
   session = requests.Session()
   session.headers.update({"Authorization": "Bearer YOUR_TOKEN"})
   response = session.get("https://api.example.com/data")
   ```

---

### **Error Handling**

- Use `try` and `except` to handle errors gracefully:
  ```python
  import requests
  try:
      response = requests.get("https://example.com", timeout=5)
      response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
  except requests.exceptions.RequestException as e:
      print(f"An error occurred: {e}")
  ```

---

### **Why Use `requests`?**

1. **Simplicity**: Minimal boilerplate code.
2. **Readability**: Clear and intuitive syntax.
3. **Rich Features**: Comprehensive support for HTTP functionality.
4. **Popular in API Development**: Perfect for RESTful API integrations.

`requests` is widely used in Python projects for web scraping, data retrieval, and API interactions. Its ease of use and reliability make it a preferred choice for developers.

## selenium
### **What is Selenium?**

Selenium is an open-source framework for automating web browsers. It is widely used for testing web applications, performing web scraping, and automating repetitive browser tasks. Selenium allows you to simulate user interactions with a web application, such as clicking buttons, filling forms, and navigating pages.

### **Key Features of Selenium**
1. **Cross-Browser Support**: Works with popular browsers like Chrome, Firefox, Edge, and Safari.
2. **Programming Language Support**: Supports multiple languages like Python, Java, C#, and more.
3. **Web Testing**: Automates testing of web applications to ensure they work as expected.
4. **Dynamic Web Pages**: Handles JavaScript-heavy and dynamically loaded content.

### **How to Test Using Selenium**

Here’s a basic example of how to use Selenium to automate a browser and perform a simple test.

#### **Step 1: Install Selenium and WebDriver**
1. Install the Selenium library:
   ```bash
   pip install selenium
   ```

2. Download the WebDriver for your browser:
   - **Chrome**: [ChromeDriver](https://sites.google.com/chromium.org/driver/)
   - **Firefox**: [GeckoDriver](https://github.com/mozilla/geckodriver/releases)

   Ensure the WebDriver is in your system's PATH or specify its path in the code.

---

#### **Step 2: Write a Simple Test**

Here’s an example of automating Google search using Selenium:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Step 1: Set up the WebDriver (Chrome in this case)
driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and in PATH

# Step 2: Open the webpage
driver.get("https://www.google.com")

# Step 3: Find the search box element
search_box = driver.find_element(By.NAME, "q")

# Step 4: Enter a search query and press Enter
search_box.send_keys("Selenium Python")
search_box.send_keys(Keys.RETURN)

# Step 5: Verify the page title
assert "Selenium Python" in driver.title

# Step 6: Print the first search result title
first_result = driver.find_element(By.CSS_SELECTOR, "h3")
print("First Search Result:", first_result.text)

# Step 7: Close the browser
driver.quit()
```

---

### **Explanation of the Code**

1. **WebDriver Setup**:
   - Use `webdriver.Chrome()` to create an instance of the Chrome browser.
   - Replace with `webdriver.Firefox()` or another driver for other browsers.

2. **Navigate to a Website**:
   - `driver.get("URL")` opens the specified URL in the browser.

3. **Find Elements**:
   - Use `find_element()` methods to locate elements by `id`, `name`, `CSS selector`, etc.
   - In the example, the search box is located by its `name` attribute.

4. **Interact with Elements**:
   - Use methods like `send_keys()` to type into input fields and `click()` to simulate clicks.

5. **Assertions**:
   - Use `assert` statements to verify conditions like page title.

6. **Close Browser**:
   - `driver.quit()` closes the browser and frees resources.

---

### **Why Use Selenium for Testing?**

1. **Automation of Repetitive Tasks**:
   Automates browser interactions like filling forms or navigating pages.

2. **Cross-Browser Testing**:
   Ensures your web application works across different browsers.

3. **Dynamic Web Pages**:
   Handles JavaScript-rendered content effectively.

4. **Integration with Testing Frameworks**:
   Can be integrated with testing frameworks like `pytest` or `unittest` for automated testing pipelines.

---

### **Best Practices for Selenium Testing**
1. Use `wait` methods (`WebDriverWait`) to handle dynamic content.
2. Ensure the WebDriver matches your browser version.
3. Structure your tests with reusable functions and modular code.
4. Use headless mode (`options.headless = True`) for faster, non-UI testing.

Selenium is a versatile and powerful tool for testing and automating browsers!

## XPath
### **What is XPath?**

XPath (XML Path Language) is a query language used to navigate and extract information from XML or HTML documents. It allows developers to locate elements in a structured document based on their hierarchical paths, attributes, or text content. XPath is commonly used in web scraping or crawling, especially when working with libraries like `lxml`, `selenium`, or `BeautifulSoup`.

---

### **Key Features of XPath**

1. **Hierarchy-Based Navigation**:
   - Locate elements by their position in the document tree.
2. **Attribute-Based Selection**:
   - Select elements using attributes like `id`, `class`, or `href`.
3. **Text-Based Selection**:
   - Extract elements based on their text content.
4. **Flexible Queries**:
   - Supports complex expressions to filter and target specific elements.

---

### **Basic Syntax of XPath**

| Syntax                        | Description                                           |
|-------------------------------|-------------------------------------------------------|
| `/`                           | Selects from the root node.                          |
| `//`                          | Selects nodes anywhere in the document.              |
| `.`                           | Refers to the current node.                          |
| `..`                          | Refers to the parent of the current node.            |
| `@`                           | Selects attributes.                                  |
| `*`                           | Matches any element.                                 |

---

### **Examples of XPath Queries**

1. **Selecting Elements by Tag**:
   - `//h1` → Select all `<h1>` elements.
   - `//div` → Select all `<div>` elements.

2. **Selecting by Attributes**:
   - `//a[@href]` → Select all `<a>` elements with an `href` attribute.
   - `//img[@src='image.jpg']` → Select all `<img>` elements with `src="image.jpg"`.

3. **Selecting by Text Content**:
   - `//p[text()='Hello World']` → Select `<p>` elements with the exact text "Hello World".
   - `//span[contains(text(), 'example')]` → Select `<span>` elements containing the word "example".

4. **Combining Conditions**:
   - `//div[@class='content' and @id='main']` → Select `<div>` elements with `class="content"` and `id="main"`.

5. **Selecting by Position**:
   - `//ul/li[1]` → Select the first `<li>` element inside a `<ul>`.
   - `//table/tr[last()]` → Select the last `<tr>` in a `<table>`.

---

### **Using XPath in Python**

Here’s how you can use XPath for web scraping with `lxml` and `selenium`.

#### **Example 1: Using `lxml`**

```python
from lxml import html
import requests

# Step 1: Fetch the web page
url = "https://example.com"
response = requests.get(url)

# Step 2: Parse the HTML content
tree = html.fromstring(response.content)

# Step 3: Extract data using XPath
titles = tree.xpath('//h1/text()')  # Extract all text inside <h1> tags
links = tree.xpath('//a/@href')    # Extract all href attributes from <a> tags

print("Titles:", titles)
print("Links:", links)
```

---

#### **Example 2: Using `Selenium`**

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

# Step 1: Set up the WebDriver
driver = webdriver.Chrome()

# Step 2: Open the webpage
driver.get("https://example.com")

# Step 3: Find elements using XPath
titles = driver.find_elements(By.XPATH, '//h1')  # Find all <h1> elements
links = driver.find_elements(By.XPATH, '//a[@href]')  # Find all <a> elements with href

# Step 4: Extract text and attributes
for title in titles:
    print("Title:", title.text)

for link in links:
    print("Link:", link.get_attribute("href"))

# Step 5: Close the browser
driver.quit()
```

---

### **Advantages of XPath for Crawling**

1. **Precise Targeting**:
   - XPath allows you to locate elements with high accuracy.
2. **Flexibility**:
   - Supports conditions, text matching, and attribute-based selection.
3. **Universal**:
   - Works for both XML and HTML structures.

---

### **When to Use XPath**
- When working with complex or poorly structured HTML.
- When you need to target specific elements based on attributes or hierarchy.
- When other methods (e.g., CSS selectors) are insufficient for precise targeting.

XPath is a powerful tool for web scraping and crawling, enabling you to extract data efficiently from even the most complex HTML structures!
## Selector
### ### **What is a Selector in Crawling?**

A **selector** is a pattern or query used to locate and extract elements from HTML or XML documents. In web crawling and scraping, selectors play a crucial role in targeting specific elements, such as headings, paragraphs, links, or images, within a web page.

Selectors can be based on:
1. **CSS Selectors**: Use the syntax of Cascading Style Sheets (CSS) to target elements.
2. **XPath**: Use the XML Path Language for flexible and powerful queries.

Both methods are widely supported by web scraping libraries like `BeautifulSoup`, `Selenium`, and `Scrapy`.

---

### **CSS Selectors**

CSS selectors are commonly used in web development and scraping to style or locate elements.

#### **Basic CSS Selector Syntax**

| Selector                   | Description                                    | Example                 |
|----------------------------|------------------------------------------------|-------------------------|
| `element`                  | Selects all `<element>` tags                   | `p` selects all `<p>` tags. |
| `#id`                      | Selects an element by its ID                   | `#main` selects `<div id="main">`. |
| `.class`                   | Selects elements by class                     | `.content` selects `<div class="content">`. |
| `element1 element2`        | Selects all `element2` inside `element1`       | `div p` selects all `<p>` tags inside `<div>`. |
| `element.class`            | Selects an element with a specific class       | `p.article` selects `<p class="article">`. |
| `element[attr=value]`      | Selects elements with a specific attribute value | `a[href="https://example.com"]` selects `<a>` tags with `href="https://example.com"`. |

---

#### **Examples of CSS Selectors**

1. Select all `<h1>` tags:
   ```css
   h1
   ```

2. Select a `<div>` with `id="header"`:
   ```css
   #header
   ```

3. Select all elements with `class="footer"`:
   ```css
   .footer
   ```

4. Select all links (`<a>` tags) with an `href` attribute:
   ```css
   a[href]
   ```

5. Select all `<li>` inside a `<ul>`:
   ```css
   ul li
   ```

---

### **XPath Selectors**

XPath provides a more robust and flexible way to locate elements, especially in complex or dynamic HTML structures.

#### **Basic XPath Syntax**

| Selector                    | Description                                         | Example                   |
|-----------------------------|-----------------------------------------------------|---------------------------|
| `/element`                  | Selects the root element                           | `/html`                   |
| `//element`                 | Selects all elements matching the name             | `//h1` selects all `<h1>` tags. |
| `@attribute`                | Selects attributes of an element                   | `//@href` selects all `href` attributes. |
| `//element[@attr='value']`  | Selects elements with a specific attribute value    | `//a[@href='https://example.com']` |
| `text()`                    | Selects the text content of an element             | `//h1/text()`             |
| `//element[position()]`     | Selects an element by its position                 | `//ul/li[1]` selects the first `<li>` inside `<ul>`. |

---

### **Example: Crawling with Selectors**

#### **Using CSS Selectors with BeautifulSoup**

```python
from bs4 import BeautifulSoup
import requests

# Fetch the webpage
url = "https://example.com"
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Use CSS selectors to extract data
title = soup.select_one("h1").text  # Extract the first <h1> text
links = soup.select("a[href]")      # Extract all <a> tags with href attributes

print("Title:", title)
print("Links:")
for link in links:
    print(link['href'])
```

#### **Using XPath Selectors with lxml**

```python
from lxml import html
import requests

# Fetch the webpage
url = "https://example.com"
response = requests.get(url)

# Parse the HTML content
tree = html.fromstring(response.content)

# Use XPath to extract data
title = tree.xpath("//h1/text()")[0]  # Extract the first <h1> text
links = tree.xpath("//a[@href]/@href")  # Extract all href attributes from <a> tags

print("Title:", title)
print("Links:", links)
```

---

### **Comparison: CSS Selectors vs. XPath**

| Feature                | CSS Selectors                        | XPath                            |
|------------------------|---------------------------------------|----------------------------------|
| **Simplicity**         | Easier and more readable             | Can be verbose for complex tasks |
| **Flexibility**        | Limited to CSS-style queries         | Handles complex conditions and structures |
| **Attribute Handling** | Requires specific syntax (`[attr=value]`) | Direct attribute access with `@` |
| **Performance**        | Often faster for simple tasks        | Better for nested or conditional queries |

---

### **When to Use CSS Selectors or XPath**

- Use **CSS Selectors** for:
  - Simple, flat HTML structures.
  - Tasks that don't require advanced conditions or logic.
- Use **XPath** for:
  - Complex or deeply nested HTML documents.
  - Scenarios requiring precise targeting with multiple conditions.

Selectors are essential tools for efficient and accurate web crawling and scraping. Choose CSS or XPath depending on your use case!