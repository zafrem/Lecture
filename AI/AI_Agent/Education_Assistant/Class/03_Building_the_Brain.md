# Step 3: Building the Brain (Agent Logic)

Now that we have memory, we need logic. The "Brain" needs to do two main things:
1.  **Understand Commands**: Translate human language into database actions.
2.  **Monitor the World**: Proactively check for problems.

## 1. Parsing Language (The "Ears")
Teachers speak in natural language: *"Schedule a review session for Friday."*
The code needs strict instructions: `INSERT INTO schedule VALUES ('2023-10-27')`.

### The "Regex" Approach (Level 1)
For this prototype, we use Regular Expressions (Regex) to find patterns.
-   Pattern: `Schedule class on [DATE] for [TOPIC]`
-   Code finds: `2026-05-20` and `Math`
-   Action: Calls `database_manager.add_schedule(...)`

### The "LLM" Approach (Level 2 - Future)
In a production system, we would send the user's text to OpenAI/Gemini:
> "Extract the date and topic from this text."

## 2. The Daily Monitor (The "Conscience")
This is what makes it an **Agent** and not just a chatbot. It acts *without* being asked.

**Logic Flow:**
1.  Wake up (e.g., every morning).
2.  **Check Schedule**: Is there class tomorrow? -> *Queue Notification*.
3.  **Check Students**: Does anyone have the `needs_help` tag? -> *Queue Support Material*.
4.  **Check Inbox**: Any new anonymous messages? -> *Add to Report*.

## 3. Python Implementation
In `agent_core.py`, we implement `process_teacher_command()` and `run_daily_monitor()`.

```python
def run_daily_monitor(self):
    logs = []
    # 1. Check for struggling students
    students = db.get_all_students()
    for s in students:
        if "needs_help" in s.tags:
            send_material(s)
            logs.append(f"Sent help to {s.name}")
    return logs
```

## 4. Educational Goal
By building this, you learn:
-   **Parsing**: Converting unstructured text (human) to structured data (machine).
-   **Automation**: Writing code that runs in the background (Cron jobs/Loops).
