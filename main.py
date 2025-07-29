import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Load Google Sheet ID from config.json
with open("config.json", "r") as f:
    config = json.load(f)
SHEET_ID = config["sheet_id"]

# Setup Google Sheets connection
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1  # Use the first sheet

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        self.root.geometry("400x350")
        self.root.configure(padx=20, pady=20)

        # Labels
        tk.Label(root, text="Description:", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
        tk.Label(root, text="Amount (RM):", font=("Arial", 12)).grid(row=1, column=0, sticky="w")
        tk.Label(root, text="Category:", font=("Arial", 12)).grid(row=2, column=0, sticky="w")

        # Inputs
        self.desc_entry = tk.Entry(root, width=30, font=("Arial", 12))
        self.amount_entry = tk.Entry(root, width=30, font=("Arial", 12))
        self.category_entry = tk.Entry(root, width=30, font=("Arial", 12))

        self.desc_entry.grid(row=0, column=1, pady=5)
        self.amount_entry.grid(row=1, column=1, pady=5)
        self.category_entry.grid(row=2, column=1, pady=5)

        # Submit Button
        tk.Button(root, text="Add Expense", command=self.add_expense, font=("Arial", 12), bg="#4CAF50", fg="white").grid(row=3, column=0, columnspan=2, pady=20)

    def add_expense(self):
        desc = self.desc_entry.get().strip()
        amount = self.amount_entry.get().strip()
        category = self.category_entry.get().strip()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not desc or not amount or not category:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            amount_float = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
            return

        try:
            sheet.append_row([date, desc, amount_float, category])
            messagebox.showinfo("Success", "Expense logged to Google Sheet.")
            self.desc_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Google Sheets Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()


