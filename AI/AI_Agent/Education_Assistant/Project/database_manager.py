import sqlite3
import datetime

DB_NAME = "education_assistant.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    """Initialize the database with necessary tables."""
    conn = get_connection()
    cursor = conn.cursor()

    # Students table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact_info TEXT,
        tags TEXT -- e.g., 'needs_math_help, visual_learner'
    )
    ''')

    # Schedule table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_time DATETIME NOT NULL,
        description TEXT NOT NULL,
        event_type TEXT DEFAULT 'class' -- class, meeting, etc.
    )
    ''')

    # Tasks/Homework table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        due_date DATETIME,
        target_student_id INTEGER, -- NULL for all students
        status TEXT DEFAULT 'pending'
    )
    ''')
    
    # Feedback/Inbox table (for anonymous student messages)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER, -- kept for record, but displayed anonymously
        message TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        is_read BOOLEAN DEFAULT 0
    )
    ''')

    # Tutoring Session table (Active learning loop)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tutoring_sessions (
        student_id INTEGER PRIMARY KEY, -- One active session per student
        topic TEXT,
        status TEXT DEFAULT 'active', -- active, completed
        context TEXT -- JSON or string to store last question/history
    )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized.")

def add_student(name, contact_info, tags=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, contact_info, tags) VALUES (?, ?, ?)", 
                   (name, contact_info, tags))
    conn.commit()
    conn.close()

def add_schedule(event_time, description, event_type="class"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO schedules (event_time, description, event_type) VALUES (?, ?, ?)", 
                   (event_time, description, event_type))
    conn.commit()
    conn.close()

def add_task(description, due_date, target_student_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (description, due_date, target_student_id) VALUES (?, ?, ?)", 
                   (description, due_date, target_student_id))
    conn.commit()
    conn.close()

def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_upcoming_schedule():
    conn = get_connection()
    cursor = conn.cursor()
    # Get schedules for the next 7 days
    now = datetime.datetime.now()
    next_week = now + datetime.timedelta(days=7)
    cursor.execute("SELECT * FROM schedules WHERE event_time BETWEEN ? AND ? ORDER BY event_time", 
                   (now, next_week))
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_feedback(student_id, message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback (student_id, message) VALUES (?, ?)", 
                   (student_id, message))
    conn.commit()
    conn.close()

def get_unread_feedback():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, student_id, message, timestamp FROM feedback WHERE is_read = 0")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_emails():
    """
    Retrieves the email addresses (contact_info) of all students.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT contact_info FROM students WHERE contact_info IS NOT NULL AND contact_info != 'No contact'")
    rows = cursor.fetchall()
    conn.close()
    # Flatten list of tuples to list of strings
    return [row[0] for row in rows]

def mark_feedback_read(feedback_ids):
    if not feedback_ids:
        return
    conn = get_connection()
    cursor = conn.cursor()
    placeholders = ','.join('?' * len(feedback_ids))
    cursor.execute(f"UPDATE feedback SET is_read = 1 WHERE id IN ({placeholders})", feedback_ids)
    conn.commit()
    conn.close()

# --- Tutoring Session Management ---

def start_tutoring_session(student_id, topic, initial_context):
    conn = get_connection()
    cursor = conn.cursor()
    # Upsert: Replace if exists
    cursor.execute("INSERT OR REPLACE INTO tutoring_sessions (student_id, topic, status, context) VALUES (?, ?, 'active', ?)", 
                   (student_id, topic, initial_context))
    conn.commit()
    conn.close()

def get_active_tutoring_session(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT topic, context FROM tutoring_sessions WHERE student_id = ? AND status = 'active'", (student_id,))
    row = cursor.fetchone()
    conn.close()
    return row # (topic, context) or None

def update_tutoring_context(student_id, new_context):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tutoring_sessions SET context = ? WHERE student_id = ?", (new_context, student_id))
    conn.commit()
    conn.close()

def end_tutoring_session(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tutoring_sessions WHERE student_id = ?", (student_id,))
    conn.commit()
    conn.close()
