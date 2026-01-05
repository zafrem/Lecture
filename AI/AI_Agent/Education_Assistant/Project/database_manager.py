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

def mark_feedback_read(feedback_ids):
    if not feedback_ids:
        return
    conn = get_connection()
    cursor = conn.cursor()
    placeholders = ','.join('?' * len(feedback_ids))
    cursor.execute(f"UPDATE feedback SET is_read = 1 WHERE id IN ({placeholders})", feedback_ids)
    conn.commit()
    conn.close()