# Education Assistant Agent (Source Code)

This directory contains the complete source code for the Education Assistant. This documentation explains exactly how the code works, file by file.

## 📂 Project Structure & File Explanation

| File | Role | Description |
| :--- | :--- | :--- |
| **`agent_core.py`** | The Brain | The central logic unit. It decides *what* to do. It handles the "Hybrid AI" logic (Gemini -> OpenAI -> Ollama -> Regex). |
| **`database_manager.py`** | The Memory | Handles all SQLite database operations: storing students, schedules, and active tutoring sessions. |
| **`discord_interface.py`** | The Ears | The connection to Discord. It listens for messages and forwards them to the Agent. |
| **`email_service.py`** | The Hands | A utility script to send emails via SMTP. Includes a "Mock Mode" for safe testing. |
| **`main.py`** | The Simulation | A standalone script to run the entire agent in your terminal without needing Discord or Email keys. |

---

## 🔍 Code Deep Dive

### 1. `agent_core.py` (The Intelligent Core)
This is where the magic happens. The `EducationAgent` class has three main responsibilities:

#### A. Understanding Language (`process_teacher_command`)
Instead of hard-coding commands, it tries to understand natural language using a **Waterfall Approach**:
1.  **Gemini/OpenAI**: If API keys are present, it sends the text to the cloud.
2.  **Ollama (Local)**: If cloud fails, it tries to hit `localhost:11434` to ask Llama 3.
3.  **Regex (Fallback)**: If no AI is available, it uses strict pattern matching.

```python
# Pseudo-code logic
if has_gemini: return query_gemini(text)
elif has_ollama: return query_ollama(text)
else: return regex_match(text)
```

#### B. The Daily Monitor (`run_daily_monitor`)
This function simulates the agent "waking up" to check for issues.
-   It looks for students with the `needs_help` tag.
-   **New Feature**: It proactively starts a **Tutoring Session** for them in the database and generates a custom starting question.

#### C. AI Tutoring Logic (`_handle_tutoring_response`)
When a student replies, this function acts as the teacher.
-   It sends the student's answer + context to the LLM.
-   **Prompt**: *"Evaluate if the answer is correct. If yes, say [PASS]. If no, explain and ask again."*
-   It loops until the student understands.

---

### 2. `database_manager.py` (The State Machine)
We use **SQLite** because it's built into Python (no installation needed).

**Key Tables:**
-   `students`: Names, emails, and tags (like `needs_help`).
-   `schedules`: Class times.
-   `tutoring_sessions`: **(New)** Tracks the state of an active AI tutoring conversation (Student ID -> Current Context).
-   `feedback`: Stores anonymous messages.

---

### 3. `discord_interface.py` (The User Interface)
This script uses `discord.py` to make the agent usable by real people.

-   **Teacher Channel**: Only listens to commands (`!agent ...`) from a specific channel ID.
-   **Student DMs**: If a user DMs the bot, it treats it as:
    1.  **Tutoring Answer**: If they are in an active session.
    2.  **Anonymous Feedback**: If they are not.

---

## 🚀 How to Run

### Option A: The Simulation (Recommended First)
Run the agent in your terminal to see the logic flow instantly.
```bash
python main.py
```
*Output: You will see the agent add students, schedule classes, and simulate a conversation with "Charlie" to test the tutoring logic.*

### Option B: The Real Discord Bot
1.  **Install Requirements**:
    ```bash
    pip install discord.py google-generativeai openai
    ```
2.  **Set Environment Variables**:
    ```bash
    export DISCORD_TOKEN="your_discord_token"
    export TEACHER_CHANNEL_ID="123456789"
    export GEMINI_API_KEY="your_key"  # Optional
    ```
3.  **Run**:
    ```bash
    python discord_interface.py
    ```

---

## 🛠 Hybrid AI Configuration
The code automatically detects which AI to use.

1.  **Cloud**: Set `GEMINI_API_KEY` or `OPENAI_API_KEY`.
2.  **Local**: Install Ollama and run `ollama run llama3`.
3.  **Offline**: Do nothing. The agent will use Regex.
