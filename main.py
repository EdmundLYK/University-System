import tkinter as tk
from gui import LoginFrame, AdminDashboard, TeacherDashboard
from school import School
from auth import validate_credentials
from person import Admin, Teacher

class SchoolApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("School Management System")
        self.geometry("1000x700")
        self.school = School()
        self.current_frame = None
        self.show_login()

    def show_login(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginFrame(self, self.login_callback)
        self.current_frame.pack(expand=True)

    def login_callback(self, username, password):
        role = validate_credentials(self.school, username, password)
        if role == 'admin':
            self.show_admin_dashboard(username)
        elif role == 'teacher':
            self.show_teacher_dashboard(username)
        else:
            tk.messagebox.showerror("Login Failed", "Invalid credentials")

    def show_admin_dashboard(self, username):
        admin = Admin(self.school, username)
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = AdminDashboard(self, admin)
        self.current_frame.pack(expand=True)

    def show_teacher_dashboard(self, username):
        teacher = Teacher(self.school, username)
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = TeacherDashboard(self, teacher)
        self.current_frame.pack(expand=True)
# This is for #Jostrix and #EdmundLYK
if __name__ == "__main__":
    app = SchoolApp()
    app.mainloop()