
"""
BMI Calculator — Advanced (GUI) Tier
OASIS INFOBYTE — Python Programming Internship — Task 2

Features:
- tkinter GUI (no command line)
- Input fields for name, weight (kg), height (m)
- BMI formula: weight / (height ** 2)
- Category classification with colour-coded feedback
- Multi-user support: BMI records saved per named user
- SQLite database for historical records
- Trend graph (matplotlib) of a user's BMI over time
- Input validation and error handling for bad input / DB failures
"""

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bmi_records.db")


def get_connection():
    """Open a connection to the SQLite database, creating the table if needed."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            weight_kg REAL NOT NULL,
            height_m REAL NOT NULL,
            bmi REAL NOT NULL,
            category TEXT NOT NULL,
            recorded_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def classify_bmi(bmi):
    """Return (category, colour) for a given BMI value."""
    if bmi < 18.5:
        return "Underweight", "#3498db"     # blue
    elif bmi < 25:
        return "Normal", "#2ecc71"          # green
    elif bmi < 30:
        return "Overweight", "#f39c12"      # orange
    else:
        return "Obese", "#e74c3c"           # red


class BMIApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BMI Calculator — OASIS INFOBYTE")
        self.geometry("480x520")
        self.resizable(False, False)
        self.configure(bg="#f5f6fa")

        self._build_widgets()

    def _build_widgets(self):
        title = tk.Label(
            self, text="BMI Calculator", font=("Segoe UI", 20, "bold"),
            bg="#f5f6fa", fg="#2c3e50"
        )
        title.pack(pady=(20, 10))

        form = tk.Frame(self, bg="#f5f6fa")
        form.pack(pady=10)

        tk.Label(form, text="Name:", bg="#f5f6fa", font=("Segoe UI", 11)).grid(
            row=0, column=0, sticky="e", padx=8, pady=8
        )
        self.name_entry = tk.Entry(form, font=("Segoe UI", 11), width=20)
        self.name_entry.grid(row=0, column=1, pady=8)

        tk.Label(form, text="Weight (kg):", bg="#f5f6fa", font=("Segoe UI", 11)).grid(
            row=1, column=0, sticky="e", padx=8, pady=8
        )
        self.weight_entry = tk.Entry(form, font=("Segoe UI", 11), width=20)
        self.weight_entry.grid(row=1, column=1, pady=8)

        tk.Label(form, text="Height (m):", bg="#f5f6fa", font=("Segoe UI", 11)).grid(
            row=2, column=0, sticky="e", padx=8, pady=8
        )
        self.height_entry = tk.Entry(form, font=("Segoe UI", 11), width=20)
        self.height_entry.grid(row=2, column=1, pady=8)

        calc_btn = tk.Button(
            self, text="Calculate", font=("Segoe UI", 12, "bold"),
            bg="#2980b9", fg="white", activebackground="#1f618d",
            padx=20, pady=6, command=self.calculate
        )
        calc_btn.pack(pady=15)

        self.result_label = tk.Label(
            self, text="", font=("Segoe UI", 16, "bold"), bg="#f5f6fa"
        )
        self.result_label.pack(pady=5)

        graph_btn = tk.Button(
            self, text="Show My BMI Trend", font=("Segoe UI", 10),
            command=self.show_trend
        )
        graph_btn.pack(pady=(5, 15))

        tk.Label(
            self, text="History (most recent 8 records)",
            font=("Segoe UI", 11, "bold"), bg="#f5f6fa"
        ).pack()

        columns = ("name", "bmi", "category", "date")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=8)
        for col, label, width in [
            ("name", "Name", 100), ("bmi", "BMI", 60),
            ("category", "Category", 110), ("date", "Date", 150)
        ]:
            self.tree.heading(col, text=label)
            self.tree.column(col, width=width, anchor="center")
        self.tree.pack(pady=10, padx=10, fill="x")

        self.refresh_history()

    def calculate(self):
        name = self.name_entry.get().strip()
        weight_raw = self.weight_entry.get().strip()
        height_raw = self.height_entry.get().strip()

        if not name:
            messagebox.showerror("Input Error", "Please enter a name.")
            return

        try:
            weight = float(weight_raw)
            height = float(height_raw)
        except ValueError:
            messagebox.showerror("Input Error", "Weight and height must be numbers.")
            return

        if weight <= 0 or height <= 0:
            messagebox.showerror("Input Error", "Weight and height must be positive numbers.")
            return

        bmi = weight / (height ** 2)
        category, colour = classify_bmi(bmi)

        self.result_label.config(
            text=f"BMI: {bmi:.2f}  —  {category}", fg=colour
        )

        try:
            conn = get_connection()
            conn.execute(
                "INSERT INTO bmi_records (username, weight_kg, height_m, bmi, category, recorded_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (name, weight, height, round(bmi, 2), category, datetime.now().isoformat(timespec="seconds")),
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not save record: {e}")
            return

        self.refresh_history()

    def refresh_history(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = get_connection()
            rows = conn.execute(
                "SELECT username, bmi, category, recorded_at FROM bmi_records "
                "ORDER BY id DESC LIMIT 8"
            ).fetchall()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not load history: {e}")
            return

        for r in rows:
            self.tree.insert("", "end", values=r)

    def show_trend(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Input Error", "Type a name first, then click 'Show My BMI Trend'.")
            return

        try:
            conn = get_connection()
            rows = conn.execute(
                "SELECT recorded_at, bmi FROM bmi_records WHERE username = ? ORDER BY id ASC",
                (name,),
            ).fetchall()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not load trend data: {e}")
            return

        if len(rows) < 2:
            messagebox.showinfo(
                "Not Enough Data",
                f"Need at least 2 saved records for '{name}' to plot a trend. "
                f"Currently have {len(rows)}."
            )
            return

        try:
            import matplotlib.pyplot as plt
        except ImportError:
            messagebox.showerror("Missing Dependency", "matplotlib is not installed. Run: pip install matplotlib")
            return

        dates = [r[0][:16] for r in rows]
        bmis = [r[1] for r in rows]

        plt.figure(figsize=(7, 4))
        plt.plot(dates, bmis, marker="o", linewidth=2, color="#2980b9")
        plt.xticks(rotation=45, ha="right")
        plt.title(f"BMI Trend for {name}")
        plt.ylabel("BMI")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    app = BMIApp()
    app.mainloop()
