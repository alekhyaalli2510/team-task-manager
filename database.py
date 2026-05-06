import sqlite3

conn = sqlite3.connect('users.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT,

    password TEXT,

    role TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS projects(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    project_name TEXT,

    created_by TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    task_name TEXT,

    assigned_to TEXT,

    status TEXT,

    project_id INTEGER
)
''')

conn.commit()

conn.close()

print("Database Created Successfully")