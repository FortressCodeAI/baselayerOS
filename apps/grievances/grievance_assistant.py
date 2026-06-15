#!/usr/bin/env python3
"""
Grievance Assistant (Desktop Version)

- Keeps everything on this computer (no internet needed)
- Stores grievances in a local file called grievances.db
- Shows a simple list of grievances and lets you add/update them

James: to run on your machine first:
    python grievance_assistant.py

Then you can package it as an .exe for your mom later.
"""

import os
import sqlite3
from datetime import datetime, timedelta
from contextlib import closing
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

APP_TITLE = "Grievance Assistant"
DB_PATH = os.path.join(os.path.dirname(__file__), "grievances.db")

STAGES = [
    "Intake",
    "Step 1",
    "Step 2",
    "Mediation/Settlement",
    "Arbitration",
    "Closed",
    "Withdrawn",
]

STATUSES = ["Open", "Closed", "Withdrawn"]
DEFAULT_DEADLINE_DAYS = 14


# ---------------------- Database helpers ---------------------- #

def init_db():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS grievances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                grievor_name TEXT NOT NULL,
                worksite TEXT NOT NULL,
                issue_type TEXT NOT NULL,
                description TEXT NOT NULL,
                remedy TEXT,
                stage TEXT NOT NULL,
                status TEXT NOT NULL,
                filing_date TEXT NOT NULL,
                next_deadline TEXT NOT NULL,
                notes TEXT
            )
            """
        )
        conn.commit()


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def compute_next_deadline(filing_date_str: str) -> str:
    try:
        filing_date = datetime.strptime(filing_date_str, "%Y-%m-%d")
    except ValueError:
        filing_date = datetime.today()
    deadline = filing_date + timedelta(days=DEFAULT_DEADLINE_DAYS)
    return deadline.strftime("%Y-%m-%d")


def deadline_status(next_deadline_str: str):
    try:
        d = datetime.strptime(next_deadline_str, "%Y-%m-%d")
    except ValueError:
        return "Unknown"
    today = datetime.today().date()
    delta = (d.date() - today).days
    if delta < 0:
        return "Overdue"
    if delta <= 3:
        return "Due soon"
    return "OK"


# ---------------------- UI: Main Application ---------------------- #

class GrievanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("900x500")
        self.minsize(800, 450)

        self.conn = get_conn()

        self.create_widgets()
        self.load_grievances()

    def create_widgets(self):
        # Top frame with title and buttons
        top_frame = ttk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        title_label = ttk.Label(top_frame, text="Grievances", font=("Segoe UI", 14, "bold"))
        title_label.pack(side=tk.LEFT)

        btn_new = ttk.Button(top_frame, text="New grievance", command=self.open_new_window)
        btn_new.pack(side=tk.RIGHT, padx=5)

        btn_refresh = ttk.Button(top_frame, text="Refresh", command=self.load_grievances)
        btn_refresh.pack(side=tk.RIGHT, padx=5)

        # Main frame with list and details hint
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # List of grievances
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        columns = ("id", "grievor", "worksite", "issue", "stage", "deadline", "status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("id", text="ID")
        self.tree.heading("grievor", text="Grievor")
        self.tree.heading("worksite", text="Worksite")
        self.tree.heading("issue", text="Issue")
        self.tree.heading("stage", text="Stage")
        self.tree.heading("deadline", text="Next deadline")
        self.tree.heading("status", text="Status")

        self.tree.column("id", width=40, anchor=tk.CENTER)
        self.tree.column("grievor", width=150)
        self.tree.column("worksite", width=150)
        self.tree.column("issue", width=150)
        self.tree.column("stage", width=120)
        self.tree.column("deadline", width=110, anchor=tk.CENTER)
        self.tree.column("status", width=80, anchor=tk.CENTER)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set) # type: ignore
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Right-side panel with actions
        side_frame = ttk.Frame(main_frame)
        side_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))

        info_label = ttk.Label(
            side_frame,
            text="Tip:\n\nSelect a grievance in the list\nand click 'Open' to view\nor update details.",
            justify=tk.LEFT
        )
        info_label.pack(pady=10)

        btn_open = ttk.Button(side_frame, text="Open selected", command=self.open_selected)
        btn_open.pack(fill=tk.X, pady=(5, 0))

    def load_grievances(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        cur = self.conn.cursor()
        cur.execute(
            "SELECT * FROM grievances ORDER BY status != 'Open', next_deadline ASC, id ASC"
        )
        rows = cur.fetchall()
        for r in rows:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    r["id"],
                    r["grievor_name"],
                    r["worksite"],
                    r["issue_type"],
                    r["stage"],
                    r["next_deadline"],
                    r["status"],
                ),
            )

    def open_new_window(self):
        NewGrievanceWindow(self, self.conn, on_saved=self.load_grievances)

    def open_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("No selection", "Please select a grievance first.")
            return
        item = self.tree.item(selected[0])
        grievance_id = item["values"][0]
        DetailWindow(self, self.conn, grievance_id, on_saved=self.load_grievances)


# ---------------------- UI: New Grievance Window ---------------------- #

class NewGrievanceWindow(tk.Toplevel):
    def __init__(self, parent, conn, on_saved=None):
        super().__init__(parent)
        self.title("New grievance")
        self.conn = conn
        self.on_saved = on_saved

        self.geometry("600x500")
        self.grab_set()

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Grievor name
        ttk.Label(frame, text="Grievor name *").grid(row=0, column=0, sticky="w")
        self.entry_grievor = ttk.Entry(frame)
        self.entry_grievor.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        # Worksite
        ttk.Label(frame, text="Worksite *").grid(row=2, column=0, sticky="w")
        self.entry_worksite = ttk.Entry(frame)
        self.entry_worksite.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        # Issue type
        ttk.Label(frame, text="Issue type *").grid(row=4, column=0, sticky="w")
        self.entry_issue = ttk.Entry(frame)
        self.entry_issue.insert(0, "e.g., Discipline, Scheduling, Pay")
        self.entry_issue.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        # Filing date
        ttk.Label(frame, text="Filing date * (YYYY-MM-DD)").grid(row=6, column=0, sticky="w")
        self.entry_filing = ttk.Entry(frame)
        self.entry_filing.insert(0, datetime.today().strftime("%Y-%m-%d"))
        self.entry_filing.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        # Description
        ttk.Label(frame, text="Description of issue *").grid(row=8, column=0, sticky="w")
        self.text_description = scrolledtext.ScrolledText(frame, height=5, wrap=tk.WORD)
        self.text_description.grid(row=9, column=0, columnspan=2, sticky="nsew", pady=(0, 8))

        # Remedy
        ttk.Label(frame, text="Remedy sought").grid(row=10, column=0, sticky="w")
        self.text_remedy = scrolledtext.ScrolledText(frame, height=3, wrap=tk.WORD)
        self.text_remedy.grid(row=11, column=0, columnspan=2, sticky="nsew", pady=(0, 8))

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=12, column=0, columnspan=2, sticky="e", pady=(10, 0))

        btn_save = ttk.Button(btn_frame, text="Save grievance", command=self.save)
        btn_save.pack(side=tk.RIGHT, padx=(5, 0))

        btn_cancel = ttk.Button(btn_frame, text="Cancel", command=self.destroy)
        btn_cancel.pack(side=tk.RIGHT)

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(9, weight=1)
        frame.rowconfigure(11, weight=1)

    def save(self):
        grievor = self.entry_grievor.get().strip()
        worksite = self.entry_worksite.get().strip()
        issue = self.entry_issue.get().strip()
        filing_date = self.entry_filing.get().strip()
        description = self.text_description.get("1.0", tk.END).strip()
        remedy = self.text_remedy.get("1.0", tk.END).strip()

        if not (grievor and worksite and issue and filing_date and description):
            messagebox.showerror("Missing information", "Please fill in all required fields (*).")
            return

        try:
            datetime.strptime(filing_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid date", "Filing date must be in the format YYYY-MM-DD.")
            return

        next_deadline = compute_next_deadline(filing_date)

        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO grievances
            (grievor_name, worksite, issue_type, description, remedy,
             stage, status, filing_date, next_deadline, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                grievor,
                worksite,
                issue,
                description,
                remedy,
                "Intake",
                "Open",
                filing_date,
                next_deadline,
                "",
            ),
        )
        self.conn.commit()

        if self.on_saved:
            self.on_saved()

        messagebox.showinfo("Saved", "Grievance has been saved.")
        self.destroy()


# ---------------------- UI: Detail / Edit Window ---------------------- #

class DetailWindow(tk.Toplevel):
    def __init__(self, parent, conn, grievance_id, on_saved=None):
        super().__init__(parent)
        self.title(f"Grievance #{grievance_id}")
        self.conn = conn
        self.grievance_id = grievance_id
        self.on_saved = on_saved

        self.geometry("700x550")
        self.grab_set()

        self.g = self.load_grievance()
        if not self.g:
            messagebox.showerror("Error", "Grievance not found.")
            self.destroy()
            return

        self.create_widgets()

    def load_grievance(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM grievances WHERE id = ?", (self.grievance_id,))
        return cur.fetchone()

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        header = ttk.Label(
            frame,
            text=f"Grievance #{self.g['id']} – {self.g['grievor_name']} ({self.g['worksite']})",
            font=("Segoe UI", 12, "bold"),
        )
        header.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # Issue
        ttk.Label(frame, text="Issue").grid(row=1, column=0, sticky="w")
        self.entry_issue = ttk.Entry(frame)
        self.entry_issue.insert(0, self.g["issue_type"])
        self.entry_issue.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        # Description
        ttk.Label(frame, text="Description").grid(row=3, column=0, sticky="w")
        self.text_description = scrolledtext.ScrolledText(frame, height=5, wrap=tk.WORD)
        self.text_description.insert("1.0", self.g["description"])
        self.text_description.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=(0, 8))

        # Remedy
        ttk.Label(frame, text="Remedy sought").grid(row=5, column=0, sticky="w")
        self.text_remedy = scrolledtext.ScrolledText(frame, height=3, wrap=tk.WORD)
        self.text_remedy.insert("1.0", self.g["remedy"] or "")
        self.text_remedy.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=(0, 8))

        # Stage
        ttk.Label(frame, text="Stage").grid(row=7, column=0, sticky="w")
        self.combo_stage = ttk.Combobox(frame, values=STAGES, state="readonly")
        self.combo_stage.set(self.g["stage"])
        self.combo_stage.grid(row=8, column=0, sticky="ew", pady=(0, 8))

        # Status
        ttk.Label(frame, text="Status").grid(row=7, column=1, sticky="w")
        self.combo_status = ttk.Combobox(frame, values=STATUSES, state="readonly")
        self.combo_status.set(self.g["status"])
        self.combo_status.grid(row=8, column=1, sticky="ew", pady=(0, 8))

        # Filing date
        ttk.Label(frame, text="Filing date (YYYY-MM-DD)").grid(row=9, column=0, sticky="w")
        self.entry_filing = ttk.Entry(frame)
        self.entry_filing.insert(0, self.g["filing_date"])
        self.entry_filing.grid(row=10, column=0, sticky="ew", pady=(0, 8))

        # Next deadline
        ttk.Label(frame, text="Next deadline (YYYY-MM-DD)").grid(row=9, column=1, sticky="w")
        self.entry_deadline = ttk.Entry(frame)
        self.entry_deadline.insert(0, self.g["next_deadline"])
        self.entry_deadline.grid(row=10, column=1, sticky="ew", pady=(0, 8))

        # Notes
        ttk.Label(frame, text="Notes").grid(row=11, column=0, sticky="w")
        self.text_notes = scrolledtext.ScrolledText(frame, height=4, wrap=tk.WORD)
        self.text_notes.insert("1.0", self.g["notes"] or "")
        self.text_notes.grid(row=12, column=0, columnspan=2, sticky="nsew", pady=(0, 8))

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=13, column=0, columnspan=2, sticky="e", pady=(10, 0))

        btn_save = ttk.Button(btn_frame, text="Save changes", command=self.save)
        btn_save.pack(side=tk.RIGHT, padx=(5, 0))

        btn_close = ttk.Button(btn_frame, text="Close window", command=self.destroy)
        btn_close.pack(side=tk.RIGHT)

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(4, weight=1)
        frame.rowconfigure(6, weight=1)
        frame.rowconfigure(12, weight=1)

    def save(self):
        issue = self.entry_issue.get().strip()
        description = self.text_description.get("1.0", tk.END).strip()
        remedy = self.text_remedy.get("1.0", tk.END).strip()
        stage = self.combo_stage.get()
        status = self.combo_status.get()
        filing_date = self.entry_filing.get().strip()
        next_deadline = self.entry_deadline.get().strip()
        notes = self.text_notes.get("1.0", tk.END).strip()

        if not (issue and description and filing_date and next_deadline):
            messagebox.showerror("Missing information", "Issue, description, filing date, and deadline are required.")
            return

        try:
            datetime.strptime(filing_date, "%Y-%m-%d")
            datetime.strptime(next_deadline, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid date", "Dates must be in the format YYYY-MM-DD.")
            return

        cur = self.conn.cursor()
        cur.execute(
            """
            UPDATE grievances
            SET issue_type = ?, description = ?, remedy = ?, stage = ?,
                status = ?, filing_date = ?, next_deadline = ?, notes = ?
            WHERE id = ?
            """,
            (
                issue,
                description,
                remedy,
                stage,
                status,
                filing_date,
                next_deadline,
                notes,
                self.grievance_id,
            ),
        )
        self.conn.commit()

        if self.on_saved:
            self.on_saved()

        messagebox.showinfo("Saved", "Changes have been saved.")
        self.destroy()


# ---------------------- Main ---------------------- #

def main():
    init_db()
    app = GrievanceApp()
    app.mainloop()


if __name__ == "__main__":
    main()
