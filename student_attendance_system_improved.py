import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date

DB_NAME = "student_attendance.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            gender TEXT,
            email TEXT,
            phone TEXT,
            class_id INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            subject TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_name TEXT NOT NULL,
            section TEXT NOT NULL,
            teacher_id INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            class_id INTEGER,
            attendance_date TEXT NOT NULL,
            status TEXT NOT NULL,
            remarks TEXT,
            UNIQUE(student_id, attendance_date)
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        """, ("admin", "admin123", "Administrator"))

    cursor.execute("SELECT COUNT(*) FROM teachers")
    if cursor.fetchone()[0] == 0:
        teachers = [
            ("T001", "John Smith", "john@example.com", "0300-1111111", "Computer Science"),
            ("T002", "Sarah Ahmed", "sarah@example.com", "0300-2222222", "Mathematics"),
            ("T003", "David Khan", "david@example.com", "0300-3333333", "Information Technology")
        ]
        cursor.executemany("""
            INSERT INTO teachers
            (teacher_id, name, email, phone, subject)
            VALUES (?, ?, ?, ?, ?)
        """, teachers)

    cursor.execute("SELECT COUNT(*) FROM classes")
    if cursor.fetchone()[0] == 0:
        cursor.execute("SELECT id FROM teachers WHERE teacher_id='T001'")
        t1 = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM teachers WHERE teacher_id='T002'")
        t2 = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM teachers WHERE teacher_id='T003'")
        t3 = cursor.fetchone()[0]

        classes = [
            ("BS Computer Science", "A", t1),
            ("BS Information Technology", "A", t3),
            ("BS Mathematics", "A", t2)
        ]
        cursor.executemany("""
            INSERT INTO classes (class_name, section, teacher_id)
            VALUES (?, ?, ?)
        """, classes)

    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            SELECT id FROM classes
            WHERE class_name='BS Computer Science'
        """)
        cs_class = cursor.fetchone()[0]

        cursor.execute("""
            SELECT id FROM classes
            WHERE class_name='BS Information Technology'
        """)
        it_class = cursor.fetchone()[0]

        students = [
            ("S001", "Ali Hassan", "Male", "ali@example.com", "0300-1111111", cs_class),
            ("S002", "Ayesha Khan", "Female", "ayesha@example.com", "0300-2222222", cs_class),
            ("S003", "Ahmed Raza", "Male", "ahmed@example.com", "0300-3333333", cs_class),
            ("S004", "Fatima Noor", "Female", "fatima@example.com", "0300-4444444", it_class),
            ("S005", "Usman Ali", "Male", "usman@example.com", "0300-5555555", it_class),
            ("S006", "Hina Malik", "Female", "hina@example.com", "0300-6666666", it_class)
        ]

        cursor.executemany("""
            INSERT INTO students
            (student_id, name, gender, email, phone, class_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, students)

    cursor.execute("SELECT COUNT(*) FROM attendance")
    if cursor.fetchone()[0] == 0:
        student_ids = {}
        for sid in ["S001", "S002", "S003", "S004", "S005", "S006"]:
            cursor.execute("SELECT id FROM students WHERE student_id=?", (sid,))
            student_ids[sid] = cursor.fetchone()[0]

        cursor.execute("""
            SELECT id FROM classes
            WHERE class_name='BS Computer Science'
        """)
        cs_class = cursor.fetchone()[0]

        cursor.execute("""
            SELECT id FROM classes
            WHERE class_name='BS Information Technology'
        """)
        it_class = cursor.fetchone()[0]

        attendance_data = [
            (student_ids["S001"], cs_class, "2026-09-15", "Present", ""),
            (student_ids["S002"], cs_class, "2026-09-15", "Present", ""),
            (student_ids["S003"], cs_class, "2026-09-15", "Absent", "Sick"),
            (student_ids["S004"], it_class, "2026-09-15", "Present", ""),
            (student_ids["S005"], it_class, "2026-09-15", "Absent", "No reason"),
            (student_ids["S006"], it_class, "2026-09-15", "Present", ""),
            (student_ids["S001"], cs_class, "2026-09-16", "Present", ""),
            (student_ids["S002"], cs_class, "2026-09-16", "Absent", "Medical"),
            (student_ids["S003"], cs_class, "2026-09-16", "Present", ""),
            (student_ids["S004"], it_class, "2026-09-16", "Present", ""),
            (student_ids["S005"], it_class, "2026-09-16", "Present", ""),
            (student_ids["S006"], it_class, "2026-09-16", "Absent", "Personal")
        ]

        cursor.executemany("""
            INSERT INTO attendance
            (student_id, class_id, attendance_date, status, remarks)
            VALUES (?, ?, ?, ?, ?)
        """, attendance_data)

    conn.commit()
    conn.close()


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Attendance Management System")
        self.root.geometry("500x430")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f6f8")

        header = tk.Frame(self.root, bg="#1f4e78", height=110)
        header.pack(fill="x")

        tk.Label(
            header, text="STUDENT ATTENDANCE",
            bg="#1f4e78", fg="white",
            font=("Arial", 21, "bold")
        ).pack(pady=(22, 2))

        tk.Label(
            header, text="Management System",
            bg="#1f4e78", fg="#dbeafe",
            font=("Arial", 12)
        ).pack()

        card = tk.Frame(
            self.root, bg="white", bd=1, relief="solid"
        )
        card.pack(padx=55, pady=25, fill="x")

        tk.Label(
            card, text="Login",
            bg="white", fg="#1f2937",
            font=("Arial", 17, "bold")
        ).pack(pady=(18, 15))

        tk.Label(
            card, text="Username",
            bg="white", fg="#374151",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", padx=35)

        self.username = ttk.Entry(card, width=35)
        self.username.pack(padx=35, pady=(5, 12))

        tk.Label(
            card, text="Password",
            bg="white", fg="#374151",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", padx=35)

        self.password = ttk.Entry(card, width=35, show="*")
        self.password.pack(padx=35, pady=(5, 15))

        ttk.Button(
            card, text="LOGIN", command=self.login
        ).pack(pady=(0, 15), ipadx=45, ipady=4)

        tk.Label(
            card,
            text="Demo Login: admin / admin123",
            bg="white", fg="#6b7280",
            font=("Arial", 9)
        ).pack(pady=(0, 18))

        self.username.focus()
        self.root.bind("<Return>", lambda event: self.login())

    def login(self):
        username = self.username.get().strip()
        password = self.password.get()

        if not username or not password:
            messagebox.showwarning(
                "Login", "Please enter username and password."
            )
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT username, role
            FROM users
            WHERE username=? AND password=?
        """, (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.root.destroy()
            main_root = tk.Tk()
            AttendanceSystem(main_root, user[0], user[1])
            main_root.mainloop()
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )


class AttendanceSystem:
    def __init__(self, root, username, role):
        self.root = root
        self.username = username
        self.role = role

        self.root.title("Student Attendance Management System")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        self.root.configure(bg="#f4f6f8")

        self.setup_style()
        self.create_header()
        self.create_sidebar()
        self.create_main_area()
        self.create_dashboard()

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except:
            pass

        style.configure(
            "Treeview",
            background="white",
            foreground="#1f2937",
            rowheight=30,
            fieldbackground="white",
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#1f4e78",
            foreground="white",
            font=("Arial", 10, "bold"),
            padding=7
        )

        style.map(
            "Treeview",
            background=[("selected", "#dbeafe")],
            foreground=[("selected", "#111827")]
        )

        style.configure(
            "TButton",
            font=("Arial", 10, "bold"),
            padding=(10, 7)
        )

        style.configure("TEntry", padding=6)
        style.configure("TCombobox", padding=5)

    def create_header(self):
        header = tk.Frame(
            self.root, bg="#1f4e78", height=65
        )
        header.pack(fill="x", side="top")

        tk.Label(
            header,
            text="Student Attendance Management System",
            bg="#1f4e78",
            fg="white",
            font=("Arial", 18, "bold")
        ).pack(side="left", padx=20, pady=17)

        user_frame = tk.Frame(header, bg="#1f4e78")
        user_frame.pack(side="right", padx=20)

        tk.Label(
            user_frame, text=self.username,
            bg="#1f4e78", fg="white",
            font=("Arial", 10, "bold")
        ).pack(anchor="e")

        tk.Label(
            user_frame, text=self.role,
            bg="#1f4e78", fg="#dbeafe",
            font=("Arial", 9)
        ).pack(anchor="e")

    def create_sidebar(self):
        self.sidebar = tk.Frame(
            self.root, bg="#243447", width=190
        )
        self.sidebar.pack(side="left", fill="y")

        tk.Label(
            self.sidebar, text="NAVIGATION",
            bg="#243447", fg="#9fb3c8",
            font=("Arial", 9, "bold")
        ).pack(pady=(20, 10))

        buttons = [
            ("Dashboard", self.create_dashboard),
            ("Students", self.student_management),
            ("Teachers", self.teacher_management),
            ("Classes", self.class_management),
            ("Attendance", self.attendance_recording),
            ("View Attendance", self.attendance_view),
            ("Reports", self.attendance_reports),
            ("Notifications", self.absence_notifications)
        ]

        for text, command in buttons:
            button = tk.Button(
                self.sidebar,
                text=text,
                command=command,
                bg="#243447",
                fg="white",
                activebackground="#1f4e78",
                activeforeground="white",
                relief="flat",
                bd=0,
                anchor="w",
                padx=20,
                font=("Arial", 10),
                cursor="hand2"
            )
            button.pack(fill="x", pady=1, ipady=7)

        tk.Frame(self.sidebar, bg="#243447").pack(
            fill="both", expand=True
        )

        tk.Button(
            self.sidebar,
            text="Logout",
            command=self.logout,
            bg="#9b2c2c",
            fg="white",
            activebackground="#7f1d1d",
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(fill="x", padx=10, pady=15, ipady=7)

    def create_main_area(self):
        self.main_area = tk.Frame(
            self.root, bg="#f4f6f8"
        )
        self.main_area.pack(
            side="right", fill="both", expand=True
        )

        self.content = tk.Frame(
            self.main_area, bg="#f4f6f8"
        )
        self.content.pack(
            fill="both", expand=True,
            padx=20, pady=20
        )

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def page_title(self, title, subtitle=""):
        tk.Label(
            self.content,
            text=title,
            bg="#f4f6f8",
            fg="#1f2937",
            font=("Arial", 21, "bold")
        ).pack(anchor="w", pady=(0, 3))

        if subtitle:
            tk.Label(
                self.content,
                text=subtitle,
                bg="#f4f6f8",
                fg="#6b7280",
                font=("Arial", 10)
            ).pack(anchor="w", pady=(0, 15))

    def create_dashboard(self):
        self.clear_content()

        self.page_title(
            "Dashboard",
            "Overview of the student attendance system"
        )

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM students")
        students = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM teachers")
        teachers = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM classes")
        classes = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*) FROM attendance
            WHERE status='Absent'
        """)
        absences = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*) FROM attendance
            WHERE status='Present'
        """)
        presents = cursor.fetchone()[0]

        conn.close()

        cards_frame = tk.Frame(
            self.content, bg="#f4f6f8"
        )
        cards_frame.pack(fill="x", pady=10)

        self.dashboard_card(
            cards_frame, "Students", students, 0, "#1f4e78"
        )
        self.dashboard_card(
            cards_frame, "Teachers", teachers, 1, "#2e7d32"
        )
        self.dashboard_card(
            cards_frame, "Classes", classes, 2, "#6a1b9a"
        )
        self.dashboard_card(
            cards_frame, "Absences", absences, 3, "#c62828"
        )
        self.dashboard_card(
            cards_frame, "Present", presents, 4, "#1565c0"
        )

        welcome = tk.Frame(
            self.content,
            bg="white",
            bd=1,
            relief="solid"
        )
        welcome.pack(fill="x", pady=25)

        tk.Label(
            welcome,
            text=f"Welcome, {self.username}!",
            bg="white",
            fg="#1f2937",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", padx=20, pady=(18, 5))

        tk.Label(
            welcome,
            text=(
                "Use the navigation menu to manage students, "
                "teachers, classes and attendance records."
            ),
            bg="white",
            fg="#6b7280",
            font=("Arial", 10)
        ).pack(anchor="w", padx=20, pady=(0, 18))

    def dashboard_card(self, parent, title, value, column, accent):
        card = tk.Frame(
            parent,
            bg="white",
            bd=1,
            relief="solid",
            width=150,
            height=110
        )
        card.grid(
            row=0, column=column,
            padx=6, sticky="nsew"
        )
        parent.grid_columnconfigure(column, weight=1)

        tk.Frame(
            card, bg=accent, width=6
        ).pack(side="left", fill="y")

        inner = tk.Frame(card, bg="white")
        inner.pack(fill="both", expand=True)

        tk.Label(
            inner, text=title,
            bg="white", fg="#6b7280",
            font=("Arial", 10, "bold")
        ).pack(pady=(17, 3))

        tk.Label(
            inner, text=str(value),
            bg="white", fg=accent,
            font=("Arial", 24, "bold")
        ).pack()

    def student_management(self):
        self.clear_content()
        self.page_title(
            "Student Management",
            "Add and view student information"
        )

        form = tk.LabelFrame(
            self.content,
            text=" Add Student ",
            bg="white",
            fg="#1f4e78",
            font=("Arial", 10, "bold"),
            bd=1,
            relief="solid"
        )
        form.pack(fill="x", pady=(0, 15))

        labels = [
            "Student ID", "Name", "Gender", "Email", "Phone"
        ]
        self.student_entries = []

        for i, label in enumerate(labels):
            tk.Label(
                form, text=label,
                bg="white", fg="#374151",
                font=("Arial", 9, "bold")
            ).grid(
                row=0, column=i,
                padx=8, pady=(12, 4), sticky="w"
            )

            if label == "Gender":
                entry = ttk.Combobox(
                    form,
                    values=["Male", "Female", "Other"],
                    width=15,
                    state="readonly"
                )
                entry.set("Male")
            else:
                entry = ttk.Entry(form, width=18)

            entry.grid(
                row=1, column=i,
                padx=8, pady=(0, 12)
            )
            self.student_entries.append(entry)

        ttk.Button(
            form, text="Add Student",
            command=self.add_student
        ).grid(row=1, column=5, padx=10, pady=10)

        table_frame = tk.Frame(
            self.content, bg="white",
            bd=1, relief="solid"
        )
        table_frame.pack(fill="both", expand=True)

        self.student_table = ttk.Treeview(
            table_frame,
            columns=(
                "ID", "Student ID", "Name",
                "Gender", "Email", "Phone"
            ),
            show="headings"
        )

        widths = {
            "ID": 60,
            "Student ID": 100,
            "Name": 170,
            "Gender": 100,
            "Email": 210,
            "Phone": 150
        }

        for column in self.student_table["columns"]:
            self.student_table.heading(
                column, text=column
            )
            self.student_table.column(
                column, width=widths.get(column, 120)
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.student_table.yview
        )
        self.student_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.student_table.pack(
            side="left", fill="both", expand=True
        )
        scrollbar.pack(side="right", fill="y")

        self.load_students()

    def add_student(self):
        values = [
            entry.get().strip()
            for entry in self.student_entries
        ]

        if not values[0] or not values[1]:
            messagebox.showwarning(
                "Required Fields",
                "Student ID and Name are required."
            )
            return

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT id FROM classes LIMIT 1"
            )
            class_row = cursor.fetchone()
            class_id = class_row[0] if class_row else None

            cursor.execute("""
                INSERT INTO students
                (student_id, name, gender, email, phone, class_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (*values, class_id))

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Student added successfully."
            )
            self.student_management()

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Error",
                "Student ID already exists."
            )
        finally:
            conn.close()

    def load_students(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, student_id, name,
                   gender, email, phone
            FROM students
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.student_table.insert(
                "", "end", values=row
            )

    def teacher_management(self):
        self.clear_content()

        self.page_title(
            "Teacher Management",
            "Add and view teacher information"
        )

        form = tk.LabelFrame(
            self.content,
            text=" Add Teacher ",
            bg="white",
            fg="#1f4e78",
            font=("Arial", 10, "bold")
        )
        form.pack(fill="x", pady=(0, 15))

        fields = [
            "Teacher ID", "Name", "Email", "Phone", "Subject"
        ]
        self.teacher_entries = []

        for i, field in enumerate(fields):
            tk.Label(
                form, text=field,
                bg="white", fg="#374151",
                font=("Arial", 9, "bold")
            ).grid(
                row=0, column=i,
                padx=8, pady=(12, 4), sticky="w"
            )

            entry = ttk.Entry(form, width=20)
            entry.grid(
                row=1, column=i,
                padx=8, pady=(0, 12)
            )
            self.teacher_entries.append(entry)

        ttk.Button(
            form, text="Add Teacher",
            command=self.add_teacher
        ).grid(row=1, column=5, padx=10)

        table_frame = tk.Frame(
            self.content, bg="white",
            bd=1, relief="solid"
        )
        table_frame.pack(fill="both", expand=True)

        self.teacher_table = ttk.Treeview(
            table_frame,
            columns=(
                "ID", "Teacher ID", "Name",
                "Email", "Phone", "Subject"
            ),
            show="headings"
        )

        for column in self.teacher_table["columns"]:
            self.teacher_table.heading(
                column, text=column
            )
            self.teacher_table.column(
                column, width=150
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.teacher_table.yview
        )
        self.teacher_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.teacher_table.pack(
            side="left", fill="both", expand=True
        )
        scrollbar.pack(side="right", fill="y")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, teacher_id, name,
                   email, phone, subject
            FROM teachers
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.teacher_table.insert(
                "", "end", values=row
            )

    def add_teacher(self):
        values = [
            e.get().strip()
            for e in self.teacher_entries
        ]

        if not values[0] or not values[1]:
            messagebox.showwarning(
                "Required Fields",
                "Teacher ID and Name are required."
            )
            return

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO teachers
                (teacher_id, name, email, phone, subject)
                VALUES (?, ?, ?, ?, ?)
            """, values)

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Teacher added successfully."
            )
            self.teacher_management()

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Error",
                "Teacher ID already exists."
            )
        finally:
            conn.close()

    def class_management(self):
        self.clear_content()

        self.page_title(
            "Class Management",
            "Add and view academic classes"
        )

        form = tk.LabelFrame(
            self.content,
            text=" Add Class ",
            bg="white",
            fg="#1f4e78",
            font=("Arial", 10, "bold")
        )
        form.pack(fill="x", pady=(0, 15))

        tk.Label(
            form, text="Class Name",
            bg="white",
            font=("Arial", 9, "bold")
        ).grid(row=0, column=0, padx=15, pady=(12, 4))

        self.class_name = ttk.Entry(
            form, width=30
        )
        self.class_name.grid(
            row=1, column=0,
            padx=15, pady=(0, 12)
        )

        tk.Label(
            form, text="Section",
            bg="white",
            font=("Arial", 9, "bold")
        ).grid(row=0, column=1, padx=15, pady=(12, 4))

        self.section = ttk.Entry(
            form, width=20
        )
        self.section.grid(
            row=1, column=1,
            padx=15, pady=(0, 12)
        )

        ttk.Button(
            form, text="Add Class",
            command=self.add_class
        ).grid(row=1, column=2, padx=15)

        table_frame = tk.Frame(
            self.content, bg="white",
            bd=1, relief="solid"
        )
        table_frame.pack(fill="both", expand=True)

        self.class_table = ttk.Treeview(
            table_frame,
            columns=("ID", "Class", "Section", "Teacher"),
            show="headings"
        )

        for column in self.class_table["columns"]:
            self.class_table.heading(
                column, text=column
            )
            self.class_table.column(
                column, width=200
            )

        self.class_table.pack(
            fill="both", expand=True
        )

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT classes.id,
                   classes.class_name,
                   classes.section,
                   teachers.name
            FROM classes
            LEFT JOIN teachers
            ON classes.teacher_id = teachers.id
            ORDER BY classes.id DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.class_table.insert(
                "", "end", values=row
            )

    def add_class(self):
        name = self.class_name.get().strip()
        section = self.section.get().strip()

        if not name or not section:
            messagebox.showwarning(
                "Required Fields",
                "Class name and section are required."
            )
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM teachers LIMIT 1"
        )
        teacher = cursor.fetchone()
        teacher_id = teacher[0] if teacher else None

        cursor.execute("""
            INSERT INTO classes
            (class_name, section, teacher_id)
            VALUES (?, ?, ?)
        """, (name, section, teacher_id))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Class added successfully."
        )
        self.class_management()

    def attendance_recording(self):
        self.clear_content()

        self.page_title(
            "Attendance Recording",
            "Record daily student attendance"
        )

        top = tk.Frame(
            self.content, bg="#f4f6f8"
        )
        top.pack(fill="x", pady=(0, 10))

        tk.Label(
            top,
            text="Attendance Date:",
            bg="#f4f6f8",
            fg="#374151",
            font=("Arial", 10, "bold")
        ).pack(side="left")

        self.attendance_date = ttk.Entry(
            top, width=18
        )
        self.attendance_date.insert(
            0, date.today().strftime("%Y-%m-%d")
        )
        self.attendance_date.pack(
            side="left", padx=10
        )

        tk.Label(
            top,
            text="Format: YYYY-MM-DD",
            bg="#f4f6f8",
            fg="#6b7280",
            font=("Arial", 9)
        ).pack(side="left")

        table_frame = tk.Frame(
            self.content, bg="white",
            bd=1, relief="solid"
        )
        table_frame.pack(
            fill="both", expand=True
        )

        self.attendance_table = ttk.Treeview(
            table_frame,
            columns=("ID", "Student ID", "Name", "Status"),
            show="headings",
            selectmode="extended"
        )

        widths = {
            "ID": 80,
            "Student ID": 150,
            "Name": 250,
            "Status": 150
        }

        for column in self.attendance_table["columns"]:
            self.attendance_table.heading(
                column, text=column
            )
            self.attendance_table.column(
                column, width=widths[column]
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.attendance_table.yview
        )
        self.attendance_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.attendance_table.pack(
            side="left", fill="both", expand=True
        )
        scrollbar.pack(side="right", fill="y")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, student_id, name
            FROM students
            ORDER BY student_id
        """)

        students = cursor.fetchall()
        conn.close()

        for student in students:
            self.attendance_table.insert(
                "", "end",
                values=(
                    student[0],
                    student[1],
                    student[2],
                    "Present"
                )
            )

        button_frame = tk.Frame(
            self.content, bg="#f4f6f8"
        )
        button_frame.pack(fill="x", pady=12)

        ttk.Button(
            button_frame,
            text="Mark Selected as Absent",
            command=self.mark_absent
        ).pack(side="left")

        ttk.Button(
            button_frame,
            text="Mark Selected as Present",
            command=self.mark_present
        ).pack(side="left", padx=10)

        ttk.Button(
            button_frame,
            text="Save Attendance",
            command=self.save_attendance
        ).pack(side="right")

    def mark_absent(self):
        selected = self.attendance_table.selection()

        if not selected:
            messagebox.showwarning(
                "Selection",
                "Please select at least one student."
            )
            return

        for item in selected:
            values = list(
                self.attendance_table.item(
                    item, "values"
                )
            )
            values[3] = "Absent"
            self.attendance_table.item(
                item, values=values
            )

    def mark_present(self):
        selected = self.attendance_table.selection()

        if not selected:
            messagebox.showwarning(
                "Selection",
                "Please select at least one student."
            )
            return

        for item in selected:
            values = list(
                self.attendance_table.item(
                    item, "values"
                )
            )
            values[3] = "Present"
            self.attendance_table.item(
                item, values=values
            )

    def save_attendance(self):
        attendance_date = (
            self.attendance_date.get().strip()
        )

        try:
            date.fromisoformat(attendance_date)
        except ValueError:
            messagebox.showerror(
                "Invalid Date",
                "Please enter the date as YYYY-MM-DD."
            )
            return

        conn = get_connection()
        cursor = conn.cursor()

        for item in self.attendance_table.get_children():
            values = self.attendance_table.item(
                item, "values"
            )

            student_id = values[0]
            status = values[3]

            cursor.execute("""
                SELECT class_id
                FROM students
                WHERE id=?
            """, (student_id,))

            result = cursor.fetchone()
            class_id = result[0] if result else None

            cursor.execute("""
                INSERT OR REPLACE INTO attendance
                (student_id, class_id,
                 attendance_date, status, remarks)
                VALUES (?, ?, ?, ?, ?)
            """, (
                student_id,
                class_id,
                attendance_date,
                status,
                ""
            ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Attendance saved successfully."
        )

    def attendance_view(self):
        self.clear_content()

        self.page_title(
            "View Attendance",
            "Search and review attendance records"
        )

        search_frame = tk.Frame(
            self.content, bg="#f4f6f8"
        )
        search_frame.pack(
            fill="x", pady=(0, 12)
        )

        tk.Label(
            search_frame,
            text="Search:",
            bg="#f4f6f8",
            font=("Arial", 10, "bold")
        ).pack(side="left")

        self.search_entry = ttk.Entry(
            search_frame, width=35
        )
        self.search_entry.pack(
            side="left", padx=10
        )

        ttk.Button(
            search_frame,
            text="Search",
            command=self.search_attendance
        ).pack(side="left")

        ttk.Button(
            search_frame,
            text="Show All",
            command=self.load_attendance
        ).pack(side="left", padx=5)

        table_frame = tk.Frame(
            self.content, bg="white",
            bd=1, relief="solid"
        )
        table_frame.pack(
            fill="both", expand=True
        )

        self.view_table = ttk.Treeview(
            table_frame,
            columns=(
                "ID", "Student ID", "Student",
                "Date", "Status", "Remarks"
            ),
            show="headings"
        )

        for column in self.view_table["columns"]:
            self.view_table.heading(
                column, text=column
            )
            self.view_table.column(
                column, width=140
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.view_table.yview
        )
        self.view_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.view_table.pack(
            side="left", fill="both", expand=True
        )
        scrollbar.pack(side="right", fill="y")

        self.load_attendance()

    def load_attendance(self):
        for item in self.view_table.get_children():
            self.view_table.delete(item)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT attendance.id,
                   students.student_id,
                   students.name,
                   attendance.attendance_date,
                   attendance.status,
                   attendance.remarks
            FROM attendance
            JOIN students
            ON attendance.student_id=students.id
            ORDER BY attendance.attendance_date DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.view_table.insert(
                "", "end", values=row
            )

    def search_attendance(self):
        keyword = self.search_entry.get().strip()

        if not keyword:
            self.load_attendance()
            return

        for item in self.view_table.get_children():
            self.view_table.delete(item)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT attendance.id,
                   students.student_id,
                   students.name,
                   attendance.attendance_date,
                   attendance.status,
                   attendance.remarks
            FROM attendance
            JOIN students
            ON attendance.student_id=students.id
            WHERE students.name LIKE ?
               OR students.student_id LIKE ?
               OR attendance.status LIKE ?
               OR attendance.attendance_date LIKE ?
            ORDER BY attendance.attendance_date DESC
        """, (
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        ))

        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.view_table.insert(
                "", "end", values=row
            )

    def attendance_reports(self):
        self.clear_content()

        self.page_title(
            "Attendance Reports",
            "Attendance summary for each student"
        )

        table_frame = tk.Frame(
            self.content, bg="white",
            bd=1, relief="solid"
        )
        table_frame.pack(
            fill="both", expand=True
        )

        report_table = ttk.Treeview(
            table_frame,
            columns=(
                "Student ID", "Student", "Present",
                "Absent", "Total", "Percentage"
            ),
            show="headings"
        )

        widths = {
            "Student ID": 120,
            "Student": 220,
            "Present": 110,
            "Absent": 110,
            "Total": 110,
            "Percentage": 130
        }

        for column in report_table["columns"]:
            report_table.heading(
                column, text=column
            )
            report_table.column(
                column, width=widths[column]
            )

        report_table.pack(
            fill="both", expand=True
        )

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                students.student_id,
                students.name,

                SUM(
                    CASE
                    WHEN attendance.status='Present'
                    THEN 1 ELSE 0
                    END
                ) AS present_count,

                SUM(
                    CASE
                    WHEN attendance.status='Absent'
                    THEN 1 ELSE 0
                    END
                ) AS absent_count,

                COUNT(attendance.id) AS total

            FROM students

            LEFT JOIN attendance
            ON students.id=attendance.student_id

            GROUP BY students.id
            ORDER BY students.student_id
        """)

        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            present = row[2] or 0
            absent = row[3] or 0
            total = row[4] or 0

            percentage = (
                (present / total) * 100
                if total > 0 else 0
            )

            report_table.insert(
                "",
                "end",
                values=(
                    row[0],
                    row[1],
                    present,
                    absent,
                    total,
                    f"{percentage:.2f}%"
                )
            )

    def absence_notifications(self):
        self.clear_content()

        self.page_title(
            "Absence Notifications",
            "Students who have been marked absent"
        )

        table_frame = tk.Frame(
            self.content, bg="white",
            bd=1, relief="solid"
        )
        table_frame.pack(
            fill="both", expand=True
        )

        notification_table = ttk.Treeview(
            table_frame,
            columns=(
                "Student ID", "Student",
                "Email", "Date", "Status"
            ),
            show="headings"
        )

        widths = {
            "Student ID": 130,
            "Student": 220,
            "Email": 250,
            "Date": 150,
            "Status": 120
        }

        for column in notification_table["columns"]:
            notification_table.heading(
                column, text=column
            )
            notification_table.column(
                column, width=widths[column]
            )

        notification_table.pack(
            fill="both", expand=True
        )

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT students.student_id,
                   students.name,
                   students.email,
                   attendance.attendance_date,
                   attendance.status
            FROM attendance
            JOIN students
            ON attendance.student_id=students.id
            WHERE attendance.status='Absent'
            ORDER BY attendance.attendance_date DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            notification_table.insert(
                "", "end", values=row
            )

        tk.Label(
            self.content,
            text=(
                "The list above identifies students "
                "who require absence notification."
            ),
            bg="#f4f6f8",
            fg="#6b7280",
            font=("Arial", 10)
        ).pack(anchor="w", pady=10)

    def logout(self):
        result = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )

        if result:
            self.root.destroy()
            root = tk.Tk()
            LoginWindow(root)
            root.mainloop()


if __name__ == "__main__":
    create_database()
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
