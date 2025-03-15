import tkinter as tk
from tkinter import messagebox, simpledialog
from person import Admin, Teacher

class LoginFrame(tk.Frame):
    def __init__(self, parent, login_callback):
        super().__init__(parent)
        self.login_callback = login_callback

        tk.Label(self, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Login", command=self.login).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.login_callback(username, password)

class AdminDashboard(tk.Frame):
    def __init__(self, parent, admin):
        super().__init__(parent)
        self.admin = admin

        tk.Label(self, text="Admin Dashboard", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Add Employee", command=self.add_employee).pack(pady=5)
        tk.Button(self, text="Remove Employee", command=self.remove_employee).pack(pady=5)
        tk.Button(self, text="Add Student", command=self.add_student).pack(pady=5)
        tk.Button(self, text="Assign Teacher to Class", command=self.assign_teacher).pack(pady=5)
        tk.Button(self, text="Logout", command=parent.show_login).pack(pady=5)

    def add_employee(self):
        name = simpledialog.askstring("Input", "Enter name:")
        if not name:
            return
        contact = simpledialog.askstring("Input", "Enter contact:")
        if not contact:
            return
        position = simpledialog.askstring("Input", "Enter position (admin/teacher/staff):")
        if not position:
            return
        username = None
        password = None
        if position in ['admin', 'teacher']:
            username = simpledialog.askstring("Input", "Enter username:")
            if not username or username in self.admin.school.users['username'].values:
                messagebox.showerror("Error", "Username invalid or already taken")
                return
            password = simpledialog.askstring("Input", "Enter password:", show='*')
            if not password:
                return
        employee_id = self.admin.add_employee(name, contact, position, username, password)
        messagebox.showinfo("Success", f"Employee added with ID: {employee_id}")

    def remove_employee(self):
        employee_id = simpledialog.askinteger("Input", "Enter employee ID to remove:")
        if employee_id:
            self.admin.remove_employee(employee_id)
            messagebox.showinfo("Success", "Employee removed")

    def add_student(self):
        name = simpledialog.askstring("Input", "Enter student name:")
        if not name:
            return
        class_name = simpledialog.askstring("Input", "Enter class:")
        if not class_name:
            return
        self.admin.add_student(name, class_name)
        messagebox.showinfo("Success", "Student added")

    def assign_teacher(self):
        class_name = simpledialog.askstring("Input", "Enter class name:")
        if not class_name:
            return
        teacher_id = simpledialog.askinteger("Input", "Enter teacher ID:")
        if teacher_id:
            self.admin.assign_teacher_to_class(class_name, teacher_id)
            messagebox.showinfo("Success", "Teacher assigned to class")

class TeacherDashboard(tk.Frame):
    def __init__(self, parent, teacher):
        super().__init__(parent)
        self.teacher = teacher

        tk.Label(self, text="Teacher Dashboard", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Mark Attendance", command=self.mark_attendance).pack(pady=5)
        tk.Button(self, text="Logout", command=parent.show_login).pack(pady=5)

    def mark_attendance(self):
        class_name = simpledialog.askstring("Input", "Enter class name:")
        if not class_name:
            return
        date = simpledialog.askstring("Input", "Enter date (e.g., YYYY-MM-DD):")
        if not date:
            return
        student_id = simpledialog.askinteger("Input", "Enter student ID:")
        if not student_id:
            return
        status = simpledialog.askstring("Input", "Enter status (present/absent):")
        if status in ['present', 'absent']:
            self.teacher.mark_attendance(class_name, date, student_id, status)
            messagebox.showinfo("Success", "Attendance marked")
        else:
            messagebox.showerror("Error", "Status must be 'present' or 'absent'")