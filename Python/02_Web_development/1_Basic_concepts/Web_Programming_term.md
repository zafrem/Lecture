# Programming Term
## HTTP
### **Definition of HTTP**  
HTTP (**HyperText Transfer Protocol**) is an application-layer protocol used for transmitting hypertext over the internet. It defines how messages are formatted and transmitted between clients (such as web browsers) and servers. HTTP follows a **request-response** model, where a client sends a request to a server, and the server responds with the requested resource or an appropriate status code.  

HTTP is **stateless**, meaning each request is independent and does not retain information from previous interactions. However, technologies like cookies and sessions help manage state when necessary.  

#### Example
```html
<body>
   <h1>Title</h1>
</body>
```
---
### **History of HTTP**
1. **HTTP/0.9 (1991)** – The first version of HTTP, created by Tim Berners-Lee. It supported only **GET** requests and returned simple HTML documents.  
2. **HTTP/1.0 (1996)** – Introduced additional request methods (**POST, HEAD**), status codes, and headers. However, it required a new connection for each request.  
3. **HTTP/1.1 (1997)** – Improved efficiency by introducing **persistent connections**, chunked transfer encoding, and caching mechanisms. It became the dominant version for many years.  
4. **HTTP/2 (2015)** – A major upgrade that introduced **multiplexing**, allowing multiple requests to be sent over a single connection. It also improved compression and security.  
5. **HTTP/3 (2022)** – Uses **QUIC** instead of TCP, reducing latency and improving performance, especially on unreliable networks.  

Each version of HTTP has enhanced speed, security, and efficiency, making web interactions smoother and more reliable.

## REST API
### **What is REST API? (Simple Explanation)**  

A **REST API** (Representational State Transfer API) is a way for different applications to communicate with each other over the internet. It follows simple rules to request and send data between a client (like a web browser or mobile app) and a server.  

---

### **How Does REST API Work?**  

Think of a **restaurant** as an example:  
1. You (the client) **order food** (request data).  
2. The **kitchen** (server) prepares the food (processes the request).  
3. The **waiter** (API) brings the food to your table (returns the response).  

In a REST API, the client sends a request using **HTTP methods**, and the server responds with data, usually in **JSON format**.  

---

### **Common HTTP Methods in REST API**  

| Method   | Meaning                        | Example Request |
|----------|--------------------------------|----------------|
| **GET**  | Retrieve data                  | Get a list of users |
| **POST** | Create new data                | Add a new user |
| **PUT**  | Update existing data           | Change user details |
| **DELETE** | Remove data                  | Delete a user |

---

### **Example of a REST API Request**  

If you want to get information about users, you send a **GET request** to this URL:  

```
https://example.com/api/users
```

The server responds with data like this:  

```json
[
  {"id": 1, "name": "Alice"},
  {"id": 2, "name": "Bob"}
]
```

This means the API returned a **list of users** in JSON format.  

---

### **Why Use REST API?**  
**Simple & Easy to Use** – Works with standard HTTP requests.  
**Flexible** – Can be used with web, mobile, or even IoT applications.  
**Scalable** – Can handle many requests efficiently.  

REST APIs help different apps work together smoothly, just like ordering food at a restaurant! 🍽️🚀