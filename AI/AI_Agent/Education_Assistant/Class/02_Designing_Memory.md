**[🏠 Home](../../../../README.md)** > **[AI](../../../README.md)** > **[AI Agent](../../README.md)** > **[Education Assistant](../README.md)** > **[Class](README.md)** > **Step 2**

# Step 2: Designing the Memory (Database)

An AI Agent is only as good as what it remembers. If it forgets who the students are, it's useless. We need to design a structured way to store information.

## 1. What do we need to remember?
Grab a pen and paper. What entities exist in a classroom?
1.  **Students**: Name, Contact Info, Status (Are they struggling?).
2.  **Schedule**: When is class? What is the topic?
3.  **Tasks/Homework**: What needs to be done?
4.  **Feedback**: What are students saying?

## 2. Schema Design (SQL)
We will use **SQLite** because it requires no server setup.

### Table: Students

| Column | Type | Purpose |
| :--- | :--- | :--- |
| `id` | INTEGER | Unique ID |
| `name` | TEXT | Student's name |
| `contact` | TEXT | Email or Discord ID |
| `tags` | TEXT | Labels like "needs_help", "visual_learner" |

### Table: Schedules

| Column | Type | Purpose |
| :--- | :--- | :--- |
| `event_time` | DATETIME | When is it? |
| `description`| TEXT | "Math Class", "Review Session" |

### Table: Feedback (The "Inbox")

| Column | Type | Purpose |
| :--- | :--- | :--- |
| `student_id` | INTEGER | Who sent it? |
| `message` | TEXT | The content |
| `is_read` | BOOLEAN | Has the teacher seen it? |

## 3. Python Implementation
In `database_manager.py`, we translate this design into code.

```python
import sqlite3

def init_db():
    conn = sqlite3.connect("education_assistant.db")
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (...)''')
    # ... (other tables)
    
    conn.commit()
```

## 4. Educational Goal
By building this, you learn:
-   **Persistent State**: Variables disappear when code stops. Databases stay.
-   **Relational Data**: How `feedback` links to a `student`.
