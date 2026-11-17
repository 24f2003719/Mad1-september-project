import sqlite3

connection=sqlite3.connect("examination.db")
cursor=connection.cursor()

create_users_table="""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT  NULL,
    role TEXT NOT NULL CHECK(role IN('admin','examiner','student')),
    status TEXT NOT NULL DEFAULT active);
    """
cursor.execute(create_users_table)
connection .commit()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ")
print(cursor.fetchall())
connection.close()
