import sqlite3
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox 
from datetime import datetime

conn = sqlite3.connect("school.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS discipline_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    class_section TEXT,
    incident TEXT,
    action TEXT,
    remarks TEXT,
    date TEXT,
    time TEXT
)
""")

conn.commit()
conn.close()
    
def open_student_window():
    student_window = tk.Toplevel(root)
    student_window.title("Student Discipline")
    student_window.geometry("700x650")
    student_window.state("zoomed")
    student_heading = tk.Label(
        student_window,
        text="Student Discipline",
        font=("Arial", 20, "bold")
    )
    student_heading.pack(pady=20)
    name_label = tk.Label(
    student_window,
    text="Student Name:"
    )
    name_label.pack()

    name_entry = tk.Entry(
    student_window,
    width=40
    )
    name_entry.pack(pady=5)
    
    class_label = tk.Label(
    student_window,
    text="Class & Section:"
    )
    class_label.pack()

    class_entry = tk.Entry(
    student_window,
    width=40
    )
    class_entry.pack(pady=5)
    
    incident_label = tk.Label(
    student_window,
    text="Incident / Misbehavior:"
    )
    incident_label.pack()

    incident_text = tk.Text(
    student_window,
    width=40,
    height=5
    )
    incident_text.pack(pady=5)
    
    action_label = tk.Label(
        student_window,
        text="Warning / Action Taken:"
    )
    action_label.pack()

    action_entry = tk.Entry(
        student_window,
        width=40
    )
    action_entry.pack(pady=5)
    
    remarks_label = tk.Label(
        student_window,
        text="Remarks:"
    )
    remarks_label.pack()

    remarks_text = tk.Text(
        student_window,
        width=40,
        height=3
    )
    remarks_text.pack(pady=5)
    
    def clear_form():
        name_entry.delete(0, tk.END)
        class_entry.delete(0, tk.END)
        incident_text.delete("1.0", tk.END)
        action_entry.delete(0, tk.END)
        remarks_text.delete("1.0", tk.END)

    date_time_label = tk.Label(
        student_window,
        text="Date & Time will be recorded automatically",
        font=("Arial", 11)
    )
    date_time_label.pack(pady=10)
    
    def save_record():
        student_name = name_entry.get().strip()
        class_section = class_entry.get().strip()
        incident = incident_text.get("1.0", tk.END).strip()
        action = action_entry.get().strip()
        remarks = remarks_text.get("1.0", tk.END).strip()

        current_datetime = datetime.now()
        date = current_datetime.strftime("%Y-%m-%d")
        time = current_datetime.strftime("%H:%M:%S")

        conn = sqlite3.connect("school.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO discipline_records
        (student_name, class_section, incident, action, remarks, date, time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (student_name, class_section, incident, action, remarks, date, time))

        conn.commit()
        conn.close()
        
        messagebox.showinfo(
            "Success",
            "Student discipline record saved successfully!"
        )
        clear_form()
        
    save_button = tk.Button(
        student_window,
        text="Save Record",
        font=("Arial", 14, "bold"),
        width=20,
        height=2,
        command=save_record
    )
    save_button.pack(pady=15)
    
    def open_records_window():
        records_window = tk.Toplevel(student_window)
        records_window.title("Student Discipline Records")
        records_window.geometry("1400x700")
        records_window.state("zoomed")
        
        search_label = tk.Label(
            records_window,
            text="Search Student Name:",
            font=("Arial", 13, "bold")
        )
        search_label.pack(pady=(15, 5))

        search_entry = tk.Entry(
            records_window,
            width=40,
            font=("Arial", 13)
        )
        search_entry.pack(pady=5)
        
        def search_records():
            search_name = search_entry.get().strip()

            for item in records_table.get_children():
                records_table.delete(item)

            conn = sqlite3.connect("school.db")
            cursor = conn.cursor()

            cursor.execute("""
            SELECT id, student_name, class_section, incident, action, remarks, date, time
            FROM discipline_records
            WHERE student_name LIKE ?
            ORDER BY id DESC
            """, ("%" + search_name + "%",))

            records = cursor.fetchall()
            conn.close()

            for record in records:
                records_table.insert(
                    "",
                    tk.END,
                    values=record
                )
        
        search_button = tk.Button(
            records_window,
            text="Search",
            font=("Arial", 12, "bold"),
            width=15,
            command=search_records
        )
        search_button.pack(pady=5)
        
        columns = (
            "ID",
            "Student Name",
            "Class & Section",
            "Incident",
            "Action",
            "Remarks",
            "Date",
            "Time"
        )

        records_table = ttk.Treeview(
            records_window,
            columns=columns,
            show="headings"
        )

        for column in columns:
            records_table.heading(
                column,
                text=column,
                anchor="center"
            )
            records_table.column(
                column,
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            records_window,
            orient="horizontal",
            command=records_table.xview
        )

        records_table.configure(
            xscrollcommand=scrollbar.set
        )
        
        records_table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(20, 0)
        )

        scrollbar.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )
        conn = sqlite3.connect("school.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id, student_name, class_section, incident, action, remarks, date, time
        FROM discipline_records
        ORDER BY id DESC
        """)

        records = cursor.fetchall()

        conn.close()

        for record in records:
            records_table.insert(
                "",
                tk.END,
                values=record,
                tags=("center",)
            )
    
    view_button = tk.Button(
        student_window,
        text="View Records",
        font=("Arial", 14, "bold"),
        width=20,
        height=2,
        command=open_records_window
    )
    view_button.pack(pady=10)

    clear_button = tk.Button(
        student_window,
        text="Clear Form",
        font=("Arial", 12),
        width=20,
        command=clear_form
    )
    clear_button.pack(pady=5)

root = tk.Tk()
root.title("Principal Management System")
root.geometry("900x600")
root.state("zoomed")

header = tk.Frame(root, bg="#2E7D5B", height=150)
header.pack(fill="x")

heading = tk.Label(
    header,
    text="Principal Management System",
    font=("Arial", 24, "bold"),
    bg="#2E7D5B",
    fg="white",
    borderwidth=0
)
heading.pack(pady=40)

student_button = tk.Button(
    root,
    text="Student Discipline",
    font=("Arial", 16, "bold"),
    width=30,
    height=3,
    command=open_student_window
)
student_button.pack(pady=10)

teacher_button = tk.Button(
    root,
    text="Teacher Tasks",
    font=("Arial", 16, "bold"),
    width=30,
    height=3,
    command=open_student_window
)

teacher_button.pack(pady=10)

meeting_button = tk.Button(
    root,
    text="Meetings & Schedule",
    font=("Arial", 16, "bold"),
    width=30,
    height=3,
    command=open_student_window
)
meeting_button.pack(pady=10)

notice_button = tk.Button(
    root,
    text="Notices & Announcements",
    font=("Arial", 16, "bold"),
    width=30,
    height=3,
    command=open_student_window
)
notice_button.pack(pady=10)

root.mainloop()
