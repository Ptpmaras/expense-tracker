# main.py
import sqlite3

conn = sqlite3.connect("expenses.db")
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT,
    amount REAL,
    category TEXT,
    date TEXT
)''')

def add_expense():
    desc = input("Description: ")
    amount = float(input("Amount: "))
    category = input("Category: ")
    date = input("Date (YYYY-MM-DD): ")

    c.execute("INSERT INTO expenses (description, amount, category, date) VALUES (?, ?, ?, ?)",
              (desc, amount, category, date))
    conn.commit()
    print("Expense added!")

add_expense()
conn.close()

