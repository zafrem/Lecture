**[🏠 Home](../../../../README.md)** > **[AI](../../../README.md)** > **[AI Agent](../../README.md)** > **[Education Assistant](../README.md)** > **[Class](README.md)** > **Step 3c**

# Step 3c: Understanding Cloud AI APIs (Gemini & OpenAI)

In Step 3b, we learned about running AI locally. However, our agent is a **Hybrid Agent**, which means it prefers to use powerful "Cloud AI" first if available. 

This guide explains what an **API** is and how we connect to giants like **Google (Gemini)** and **OpenAI (ChatGPT)**.

---

## 1. What is an API? (The Restaurant Analogy)

Imagine you are at a restaurant:
1.  **You (The Customer)**: This is your Python code.
2.  **The Kitchen**: This is OpenAI or Google’s supercomputer. It has the ingredients and chefs to "cook" an answer for you.
3.  **The Waiter (The API)**: You don't go into the kitchen yourself. You give your order to the waiter. The waiter takes it to the kitchen and brings the food back to your table.

**API** stands for *Application Programming Interface*. It is simply the "Waiter" that allows your code to talk to someone else's service.

---

## 2. Meet the "Genius Friends"

Our Education Assistant can talk to two main Cloud APIs:

### 1. OpenAI (The Pioneer)
-   **Model**: GPT-3.5 or GPT-4.
-   **Company**: The creators of ChatGPT.
-   **Vibe**: Very reliable, great at following strict instructions (like outputting JSON).

### 2. Google Gemini (The New Giant)
-   **Model**: Gemini Pro.
-   **Company**: Google.
-   **Vibe**: Very fast, integrated with Google's ecosystem, and often has a very generous "Free Tier" for developers.

---

## 3. What is an API Key?

When you use a Cloud API, they need to know who is "ordering the food" so they can bill you (or track your free usage).

An **API Key** is like a combination of a **Username**, **Password**, and **Credit Card** all in one long string of text.

**Example**: `sk-abc123xyz...`

> ⚠️ **CRITICAL SAFETY RULE**: Never share your API key or upload it to GitHub. If someone steals it, they can use the AI on your bill!

---

## 4. How the Code "Authenticates"

In our project, we don't type the key directly into the code. We use **Environment Variables**. 

**Why?** Because if you share your code with a friend, they can use *their* key instead of yours, and your key stays hidden on your own computer.

### The Python Logic:
```python
import os

# 1. We ask the Operating System: "Do you have a secret called GEMINI_API_KEY?"
key = os.getenv("GEMINI_API_KEY")

if key:
    # 2. If yes, we give that key to the Google library to "log in"
    genai.configure(api_key=key)
    print("Logged in successfully!")
else:
    # 3. If no, the agent says "Okay, I'll use Ollama or Regex instead."
    print("No key found. Switching to Local AI.")
```

---

## 5. How to get your own keys

If you want to try the "Smartest" version of your agent, follow these steps:

### For Google Gemini (Recommended for Beginners):
1.  Go to [Google AI Studio](https://aistudio.google.com/).
2.  Log in with your Google Account.
3.  Click **"Get API Key"**.
4.  Copy the key.

### For OpenAI:
1.  Go to the [OpenAI Platform](https://platform.openai.com/).
2.  Create an account and add a small amount of credit ($5 is usually plenty for months of testing).
3.  Go to **API Keys** and create a new secret key.

---

## 6. Summary

-   **APIs** are waiters that fetch AI answers for us.
-   **Cloud AI** is smarter but requires an **API Key**.
-   **Hybrid Design** is best:
    -   **Step 1**: Look for Cloud Keys (Gemini/OpenAI).
    -   **Step 2**: If no keys, try Local AI (Ollama).
    -   **Step 3**: If no Ollama, use Regex (Simple patterns).

This ensures your Education Assistant works for everyone, regardless of whether they have a paid account or a powerful computer!
