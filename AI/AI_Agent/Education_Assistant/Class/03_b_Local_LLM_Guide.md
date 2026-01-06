# Step 3b: Deep Dive into Local LLMs & Ollama

In the previous step, we talked about giving our Agent a "Brain". Usually, developers use cloud services like OpenAI (ChatGPT) or Google Gemini. However, there is a powerful alternative: **Running the AI locally on your own computer.**

This guide explains what that means, why it matters, and how to do it using a tool called **Ollama**.

---

## 1. Cloud vs. Local AI: What's the difference?

Imagine you need to solve a complex math problem. You have two options:

### Option A: Call a Genius Friend (Cloud AI)
-   **How it works**: You send a text message (API Request) to OpenAI or Google. Their massive supercomputers process it and send back the answer.
-   **Pros**: Extremely smart, no work for your computer.
-   **Cons**:
    -   **Cost**: You often pay per message.
    -   **Privacy**: Your data leaves your computer.
    -   **Dependency**: No internet = No AI.

### Option B: Read a Textbook Yourself (Local AI)
-   **How it works**: You download a smaller version of the "brain" (Model) onto your laptop's hard drive. Your computer's CPU/GPU does the thinking.
-   **Pros**:
    -   **Free**: No monthly fees.
    -   **Private**: Data never leaves your machine.
    -   **Offline**: Works without Wi-Fi.
-   **Cons**:
    -   **Heavy**: Uses a lot of RAM and battery.
    -   **Dumber**: Local models are smaller than Cloud models (like comparing a student to a professor).

---

## 2. What is Ollama?

Running an AI model raw (using Python libraries like `pytorch` or `transformers`) is very complicated. It involves installing huge drivers and writing complex code.

**Ollama** is a tool that simplifies this. Think of it like a "Video Game Player" for AI Models.
-   **Game Cartridge** = The Model (e.g., Llama 3).
-   **Console** = Ollama.

You just tell Ollama "Run Llama 3", and it handles all the complex math and hardware setup for you.

---

## 3. Step-by-Step Setup

### Step 1: Install Ollama
1.  Go to [ollama.com](https://ollama.com).
2.  Download the version for your OS (Mac, Windows, or Linux).
3.  Install it like any normal application.

### Step 2: "Pull" (Download) a Model
In the terminal (or command prompt), you need to download a brain. We call this "pulling".
The most popular open-source model currently is **Llama 3** (created by Meta/Facebook).

Run this command:
```bash
ollama pull llama3
```
*Note: This download is about 4.7 GB. It's a compressed file containing the neural network weights.*

### Step 3: Test it
Once downloaded, you can chat with it directly in your terminal:
```bash
ollama run llama3
```
You will see a prompt. Type "Hi, who are you?" and it should reply!
*(Type `/bye` to exit).*

---

## 4. Connecting Python to Ollama

Now that Ollama is running, how does our Python code talk to it?

Ollama runs a **Local Server** in the background on port `11434`. It listens for messages, just like a website.

### The Code Explanation
In `agent_core.py`, we added this function:

```python
import urllib.request
import json

def _query_ollama(self, user_input):
    # 1. The Address: We look for Ollama on our own computer (localhost)
    url = "http://localhost:11434/api/generate"
    
    # 2. The Message: We prepare the data (Model name + Prompt)
    data = {
        "model": "llama3",       # The specific brain to use
        "prompt": user_input,    # What we want it to do
        "stream": False          # False = Wait for full answer, True = Typewriter effect
    }
    
    # 3. Sending the Letter: We convert data to JSON and send it
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'))
    
    # 4. Reading the Reply
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        return result.get('response', '')
```

### Why use `urllib` instead of `import ollama`?
There is a Python library for Ollama, but using standard tools (`urllib`) is better for learning because:
1.  **No Installation**: It works on every Python setup without `pip install`.
2.  **Transparency**: You see exactly how the "API Request" works (URL + Data -> Response).

---

## 5. Summary

By adding Ollama to our Education Assistant, we created a **Hybrid Agent**:
1.  It tries to use the **Cloud** (Gemini/OpenAI) first, because it's smarter.
2.  If that fails (no keys/internet), it switches to **Local** (Ollama/Llama3).
3.  If even that fails, it falls back to **Regex** (simple rules).

This makes your application incredibly robust and accessible!
