# Data Storage

Once data is collected, it needs to be stored for future analysis and accumulation. This section explores different methods for persisting data, from simple text files to robust relational databases.

## Plain Text (CSV-style)

Simple and human-readable, but inefficient for large-scale retrieval or complex searching.

<details>
<summary>View Code: Text File Implementation</summary>

```python
from datetime import datetime

def save_data_text(filename, price, change_value):
    with open(filename, "a+", encoding="utf-8") as file:
        file.write(f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}|{price}|{change_value}\n")

def load_data_text(filename):
    with open(filename, "r", encoding="utf-8") as read_file:
        for lines in read_file.readlines():
            row = lines.rstrip("\n").split("|")
            print(f"Date : {row[0]}, Price : {row[1]}, Percentage : {row[2]}")
```
</details>

*   **Pros**: No special tools required; easy to inspect manually.
*   **Cons**: Slow searching; no data types; difficult to maintain as data grows.

---

## JSON (Structured Data)

Well-structured and natively supported by many web services, but becomes resource-intensive for very large datasets.

<details>
<summary>View Code: JSON Implementation</summary>

```python
import json
from datetime import datetime

def save_data_json(filename, price, percentage):
    # Load existing data
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    # Update and save
    new_entry = {datetime.today().strftime("%Y-%m-%d %H:%M:%S"): f"{price} ({percentage})"}
    data.update(new_entry)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
```
</details>

*   **Pros**: Maintains data structure (hierarchical); human-readable.
*   **Cons**: Reading/writing requires parsing the entire file into memory.

---

## SQLite (Embedded Database)

A lightweight, serverless database that stores everything in a single file. Highly efficient for medium-sized applications.

<details>
<summary>View Code: SQLite Implementation</summary>

```python
import sqlite3

def create_table():
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS coin (
            dt DATETIME PRIMARY KEY DEFAULT CURRENT_TIMESTAMP,
            current_info INTEGER,
            percentage INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def insert_data(curr_point, percentage):
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO coin (current_info, percentage) VALUES (?, ?)', (curr_point, percentage))
    conn.commit()
    conn.close()
```
</details>

*   **Pros**: Full SQL support; fast searching and indexing; no external server needed.
*   **Cons**: Best for single-application use; concurrent write performance is limited.

---

## SQLAlchemy (ORM)

An Object-Relational Mapper (ORM) that allows you to interact with databases (like MySQL or PostgreSQL) using Python objects instead of raw SQL.

<details>
<summary>View Code: SQLAlchemy Implementation</summary>

```python
from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Data(Base):
    __tablename__ = 'coin'
    dt = Column(DateTime, primary_key=True, default=datetime.utcnow)
    current_info = Column(Integer, nullable=False)
    percentage = Column(Float, nullable=False)

# Configuration for MySQL
DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/test_db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
```
</details>

*   **Pros**: Abstraction from raw SQL; easy to switch between different database engines (e.g., SQLite to MySQL).
*   **Cons**: Additional library overhead; higher learning curve for complex queries.
