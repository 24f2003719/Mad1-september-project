
import sqlite3
from getpass import getpass
from werkzeug.security import generate_password_hash

DATABASE = "examination.db"

name = input("Enter Admin name: ")
email = input("Enter Admin email: ")
password = getpass("Enter Admin password: ")

if not name.strip() or not email.strip() or not password:
    print("All fields are required.")
else:
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    try: 
        cursor.execute(
            "SELECT id FROM users WHERE role = ?",
            ("admin",)
        )

        if cursor.fetchone():
            print("An Admin account already exists.")
        else:
            password_hash = generate_password_hash(password)

            cursor.execute(
                """
                INSERT INTO users
                (name, email, password_hash, role, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    name.strip(),
                    email.strip().lower(),
                    password_hash,
                    "admin",
                    "active"
                )
            )

            connection.commit()
            print("Admin account created successfully!")

    except sqlite3.IntegrityError:
        connection.rollback()
        print("This email already exists. Try another email.")

    finally:
        connection.close()
