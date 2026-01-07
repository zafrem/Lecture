**[🏠 Home](../../../../README.md)** > **[AI](../../../README.md)** > **[AI Agent](../../README.md)** > **[Education Assistant](../README.md)** > **[Class](README.md)** > **Step 3**

# Step 3: Building the Brain (Agent Logic)

Now that we have memory, we need logic. The "Brain" needs to do three main things:
1.  **Understand Commands**: Translate human language into database actions.
2.  **Monitor the World**: Proactively check for problems.
3.  **Teach**: Actively tutor students who need help.

## 1. Parsing Language (The "Ears")
Teachers speak in natural language: *"Schedule a review session for Friday."*
The code needs strict instructions: `INSERT INTO schedule VALUES ('2023-10-27')`.

### The Hybrid Approach
We use a tiered system for "thinking":
1.  **Cloud AI (Gemini/OpenAI)**: Best for complex reasoning.
2.  **Local AI (Ollama)**: Great for privacy and free usage. (Model: `llama3` or `olmo`)
3.  **Regex Fallback**: Simple pattern matching if AI fails.

```python
# Pseudo-code logic
if has_gemini: call_gemini()
elif has_ollama: call_local_ollama()
else: use_regex()
```

## 2. The Daily Monitor (The "Conscience")
This is what makes it an **Agent** and not just a chatbot. It acts *without* being asked.

**Logic Flow:**
1.  Wake up (e.g., every morning).
2.  **Check Schedule**: Is there class tomorrow? -> *Queue Notification*.
3.  **Equity Check**: Does anyone have the `needs_help` tag? 
    -   *Old Way*: Send a static PDF.
    -   *New AI Way*: **Initiate a Tutoring Session**.

## 3. The AI Tutor Loop
Instead of just flagging a student, the Agent enters an interactive loop:
1.  **Start**: Agent generates a concept question.
2.  **Wait**: Student responds (handled via `process_student_message`).
3.  **Evaluate**: Agent (Ollama/Gemini) checks the answer.
    -   *Correct*: "Great job!" (End Session)
    -   *Incorrect*: Explain concept -> Ask new question -> Repeat.

## 4. Educational Goal
By building this, you learn:
-   **Parsing**: Converting unstructured text (human) to structured data (machine).
-   **Local LLMs**: Running AI models like Llama 3 locally using Ollama.
-   **Stateful Interactions**: Managing long-running "Tutoring Sessions" in a database.