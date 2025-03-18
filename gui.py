import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from tkinter import Canvas, Entry, Button, PhotoImage
from person import Admin, Teacher  # Ensure these classes are defined

# ------------------ Paths and Asset Helper ------------------
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# ------------------ FormWindow Helper Class ------------------
class FormWindow(tk.Toplevel):
    """
    A Toplevel window (1000x500) with a background made of two layered images:
    - The bottom layer: carbon.png
    - The top layer: image_1.png
    A vertical form is generated based on the provided fields.
    When the user presses "Submit" or Enter, the form's values are passed to submit_callback.
    If submit_callback returns True, the window closes; otherwise it remains open.
    This window is modal and centered on the screen.
    """
    def __init__(self, parent, title, fields, submit_callback):
        super().__init__(parent)
        self.title(title)
        # Set window size and center it
        width, height = 1000, 500
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)
        self.configure(bg="#330000")
        
        # Make the window modal and transient so it stays on top of the dashboard
        self.transient(parent)
        self.grab_set()
        
        # Create a canvas covering the window
        self.canvas = Canvas(self, bg="#330000", height=500, width=1000, bd=0, 
                             highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        
        # Bottom background image: carbon.png
        self.carbon_bg = PhotoImage(file=relative_to_assets("carbon.png"))
        self.canvas.carbon_bg = self.carbon_bg  # Keep a reference
        self.canvas.create_image(500, 250, image=self.carbon_bg)
        
        # Top overlapping background image: image_1.png
        self.top_bg = PhotoImage(file=relative_to_assets("image_1.png"))
        self.canvas.top_bg = self.top_bg
        self.canvas.create_image(500, 250, image=self.top_bg)
        
        # Create form fields (labels and entries)
        self.entries = {}
        y_start = 100
        y_gap = 60
        for i, (field_label, default_val) in enumerate(fields):
            y_pos = y_start + i * y_gap
            lbl = tk.Label(self, text=field_label, font=("Inter", 20), bg="#330000", fg="#FFFFFF")
            self.canvas.create_window(200, y_pos, window=lbl, anchor="w")
            ent = tk.Entry(self, font=("Inter", 20), fg="#000716", bd=2)
            if default_val is not None:
                ent.insert(0, default_val)
            self.entries[field_label] = ent
            self.canvas.create_window(500, y_pos, window=ent, anchor="w", width=300, height=40)
        
        # Submission function
        def on_submit():
            result = submit_callback(self.get_values())
            if result:
                self.destroy()
        
        # Bind the Return key to submission
        self.bind("<Return>", lambda event: on_submit())
        
        # Submit Button
        submit_btn = tk.Button(self, text="Submit", font=("Inter", 20), command=on_submit)
        self.canvas.create_window(500, y_pos + 80, window=submit_btn, anchor="center", width=150, height=50)
    
    def get_values(self):
        values = {}
        for key, ent in self.entries.items():
            values[key] = ent.get().strip()
        return values

# ------------------ Login Page (Canvas-based) ------------------
class LoginFrame(tk.Frame):
    def __init__(self, parent, login_callback):
        super().__init__(parent, bg="#330000")  # Dark red background
        self.login_callback = login_callback
        self.configure(width=1000, height=700)
        self.pack_propagate(0)

        # Create canvas for the login design
        self.canvas = Canvas(self, bg="#330000", height=700, width=1000, bd=0, 
                             highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        # Bottom background: carbon.png
        self.carbon_bg = PhotoImage(file=relative_to_assets("carbon.png"))
        self.canvas.carbon_bg = self.carbon_bg
        self.canvas.create_image(500, 350, image=self.carbon_bg)
        # Top overlapping background: image_1.png
        self.top_bg = PhotoImage(file=relative_to_assets("image_1.png"))
        self.canvas.top_bg = self.top_bg
        self.canvas.create_image(500, 350, image=self.top_bg)

        # Title text
        self.canvas.create_text(
            170, 29, anchor="nw", 
            text="University Management System", 
            fill="#FFF2F2", font=("Roboto Regular", 45 * -1)
        )

        # Username label and entry background
        self.canvas.create_text(
            279, 171, anchor="nw", 
            text="Username", fill="#FFF8F8", font=("Inter", 16 * -1)
        )
        self.entry_bg_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        self.canvas.create_image(498.5, 184, image=self.entry_bg_1)
        self.username_entry = Entry(
            self, bd=0, bg="#D9D9D9", fg="#000716",
            highlightthickness=0, font=("Inter", 20)
        )
        self.username_entry.place(x=384, y=150, width=229, height=66)
        self.username_entry.bind("<Return>", lambda event: self.login())

        # Password label and entry background
        self.canvas.create_text(
            278, 284, anchor="nw", 
            text="Password", fill="#FFF8F8", font=("Inter", 16 * -1)
        )
        self.entry_bg_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        self.canvas.create_image(498.5, 298, image=self.entry_bg_2)
        self.password_entry = Entry(
            self, bd=0, bg="#D9D9D9", fg="#000716", 
            highlightthickness=0, show="*", font=("Inter", 20)
        )
        self.password_entry.place(x=384, y=264, width=229, height=66)
        self.password_entry.bind("<Return>", lambda event: self.login())

        # Login button with hover feature
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.login_button = Button(
            self, image=self.button_image_1, borderwidth=0, highlightthickness=0,
            command=self.login, relief="flat"
        )
        self.login_button.place(x=427, y=393, width=111, height=46)
        self.button_image_hover_1 = PhotoImage(file=relative_to_assets("button_hover_1.png"))
        self.login_button.bind('<Enter>', self.on_hover)
        self.login_button.bind('<Leave>', self.on_leave)

    def on_hover(self, event):
        self.login_button.config(image=self.button_image_hover_1)

    def on_leave(self, event):
        self.login_button.config(image=self.button_image_1)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.login_callback(username, password)

# ------------------ Admin Dashboard ------------------
class AdminDashboard(tk.Frame):
    def __init__(self, parent, admin):
        super().__init__(parent)
        self.admin = admin
        self.configure(width=1000, height=700)
        self.pack_propagate(0)
        
        # Create a canvas for the dashboard background with dark red as bg
        self.canvas = Canvas(self, width=1000, height=700, bd=0, highlightthickness=0, relief="ridge", bg="#330000")
        self.canvas.pack(fill="both", expand=True)
        # Bottom layer: carbon.png
        self.carbon_bg = PhotoImage(file=relative_to_assets("carbon.png"))
        self.canvas.carbon_bg = self.carbon_bg
        self.canvas.create_image(500, 350, image=self.carbon_bg)
        # Top layer: image_1.png
        self.top_bg = PhotoImage(file=relative_to_assets("image_1.png"))
        self.canvas.top_bg = self.top_bg
        self.canvas.create_image(500, 350, image=self.top_bg)
        
        # Create a frame on top to hold dashboard widgets with dark red background
        content_frame = tk.Frame(self.canvas, bg="#330000")
        self.canvas.create_window(500, 350, window=content_frame, anchor="center")
        
        tk.Label(content_frame, text="Admin Dashboard", font=("Arial", 24), bg="#330000", fg="#FFFFFF").pack(pady=10)
        btn_font = ("Inter", 20)
        tk.Button(content_frame, text="Add Employee", font=btn_font, command=self.add_employee).pack(pady=5)
        tk.Button(content_frame, text="Update Employee", font=btn_font, command=self.update_employee).pack(pady=5)
        tk.Button(content_frame, text="Remove Employee", font=btn_font, command=self.remove_employee).pack(pady=5)
        tk.Button(content_frame, text="Add Student", font=btn_font, command=self.add_student).pack(pady=5)
        tk.Button(content_frame, text="Remove Student", font=btn_font, command=self.remove_student).pack(pady=5)
        tk.Button(content_frame, text="Update Student", font=btn_font, command=self.update_student).pack(pady=5)
        tk.Button(content_frame, text="Assign Teacher to Class", font=btn_font, command=self.assign_teacher).pack(pady=5)
        tk.Button(content_frame, text="Logout", font=btn_font, command=parent.show_login).pack(pady=5)

    def add_employee(self):
        fields = [
            ("Name", ""),
            ("Contact", ""),
            ("Position", ""),
            ("Username", ""),
            ("Password", "")
        ]
        def submit(values):
            if not values["Name"] or not values["Contact"] or not values["Position"]:
                messagebox.showerror("Error", "Name, Contact, and Position are required.")
                return False
            if values["Position"].lower() in ['admin', 'teacher'] and (not values["Username"] or not values["Password"]):
                messagebox.showerror("Error", "Username and Password are required for admin/teacher positions.")
                return False
            employee_id = self.admin.add_employee(values["Name"], values["Contact"], values["Position"],
                                                  values["Username"], values["Password"])
            messagebox.showinfo("Success", f"Employee added with ID: {employee_id}")
            return True
        FormWindow(self, "Add Employee", fields, submit)
    
    def update_employee(self):
        fields = [
            ("Employee ID", ""),
            ("Name", ""),
            ("Contact", ""),
            ("Position", ""),
            ("Username", ""),
            ("Password", "")
        ]
        def submit(values):
            try:
                emp_id = int(values["Employee ID"])
            except ValueError:
                messagebox.showerror("Error", "Invalid Employee ID.")
                return False
            if emp_id not in self.admin.school.employees['employee_id'].values:
                messagebox.showerror("Error", "Employee ID not found.")
                return False
            self.admin.update_employee(emp_id, values["Name"], values["Contact"],
                                       values["Position"], values["Username"], values["Password"])
            messagebox.showinfo("Success", f"Employee ID {emp_id} updated successfully.")
            return True
        FormWindow(self, "Update Employee", fields, submit)

    def remove_employee(self):
        fields = [("Employee ID", "")]
        def submit(values):
            try:
                emp_id = int(values["Employee ID"])
            except ValueError:
                messagebox.showerror("Error", "Invalid Employee ID.")
                return False
            self.admin.remove_employee(emp_id)
            messagebox.showinfo("Success", "Employee removed.")
            return True
        FormWindow(self, "Remove Employee", fields, submit)

    def add_student(self):
        fields = [
            ("Student Name", ""),
            ("Age", ""),
            ("Class", "")
        ]
        def submit(values):
            if not values["Student Name"] or not values["Age"] or not values["Class"]:
                messagebox.showerror("Error", "All fields are required.")
                return False
            try:
                age = int(values["Age"])
            except ValueError:
                messagebox.showerror("Error", "Age must be a number.")
                return False
            self.admin.add_student(values["Student Name"], age, values["Class"])
            messagebox.showinfo("Success", "Student added.")
            return True
        FormWindow(self, "Add Student", fields, submit)

    def remove_student(self):
        fields = [("Student ID", "")]
        def submit(values):
            try:
                std_id = int(values["Student ID"])
            except ValueError:
                messagebox.showerror("Error", "Invalid Student ID.")
                return False
            self.admin.remove_student(std_id)
            messagebox.showinfo("Success", "Student removed.")
            return True
        FormWindow(self, "Remove Student", fields, submit)

    def update_student(self):
        fields = [
            ("Student ID", ""),
            ("Name", ""),
            ("Age", ""),
            ("Class", ""),
            ("Marks", "")
        ]
        def submit(values):
            try:
                std_id = int(values["Student ID"])
            except ValueError:
                messagebox.showerror("Error", "Invalid Student ID.")
                return False
            if std_id not in self.admin.school.students['student_id'].values:
                messagebox.showerror("Error", "Student ID not found.")
                return False
            self.admin.update_student(std_id, values["Name"], values["Age"], values["Class"], values["Marks"])
            messagebox.showinfo("Success", f"Student ID {std_id} updated successfully.")
            return True
        FormWindow(self, "Update Student", fields, submit)

    def assign_teacher(self):
        fields = [
            ("Class Name", ""),
            ("Teacher ID", "")
        ]
        def submit(values):
            try:
                teacher_id = int(values["Teacher ID"])
            except ValueError:
                messagebox.showerror("Error", "Invalid Teacher ID.")
                return False
            self.admin.assign_teacher_to_class(values["Class Name"], teacher_id)
            messagebox.showinfo("Success", "Teacher assigned to class.")
            return True
        FormWindow(self, "Assign Teacher", fields, submit)

# ------------------ Teacher Dashboard ------------------
class TeacherDashboard(tk.Frame):
    def __init__(self, parent, teacher):
        super().__init__(parent)
        self.teacher = teacher
        self.configure(width=1000, height=700)
        self.pack_propagate(0)
        
        self.canvas = Canvas(self, width=1000, height=700, bd=0, highlightthickness=0, relief="ridge", bg="#330000")
        self.canvas.pack(fill="both", expand=True)
        # Bottom background: carbon.png
        self.carbon_bg = PhotoImage(file=relative_to_assets("carbon.png"))
        self.canvas.carbon_bg = self.carbon_bg
        self.canvas.create_image(500, 350, image=self.carbon_bg)
        # Top overlapping background: image_1.png
        self.top_bg = PhotoImage(file=relative_to_assets("image_1.png"))
        self.canvas.top_bg = self.top_bg
        self.canvas.create_image(500, 350, image=self.top_bg)
        
        header_text = f"Teacher ({self.teacher.username})'s Dashboard"
        content_frame = tk.Frame(self.canvas, bg="#330000")
        self.canvas.create_window(500, 350, window=content_frame, anchor="center")
        
        tk.Label(content_frame, text=header_text, font=("Arial", 24), bg="#330000", fg="#FFFFFF").pack(pady=10)
        btn_font = ("Inter", 20)
        tk.Button(content_frame, text="Mark Attendance", font=btn_font, command=self.mark_attendance).pack(pady=5)
        tk.Button(content_frame, text="Update Profile", font=btn_font, command=self.update_teacher).pack(pady=5)
        tk.Button(content_frame, text="Update Student Mark", font=btn_font, command=self.update_student_mark).pack(pady=5)
        tk.Button(content_frame, text="Logout", font=btn_font, command=parent.show_login).pack(pady=5)

    def mark_attendance(self):
        fields = [
            ("Class Name", ""),
            ("Date (YYYY-MM-DD)", ""),
            ("Student ID", ""),
            ("Status (present/absent)", "")
        ]
        def submit(values):
            try:
                std_id = int(values["Student ID"])
            except ValueError:
                messagebox.showerror("Error", "Invalid Student ID.")
                return False
            if values["Status"].lower() not in ['present', 'absent']:
                messagebox.showerror("Error", "Status must be 'present' or 'absent'.")
                return False
            self.teacher.mark_attendance(values["Class Name"], values["Date (YYYY-MM-DD)"], std_id, values["Status"])
            messagebox.showinfo("Success", "Attendance marked.")
            return True
        FormWindow(self, "Mark Attendance", fields, submit)

    def update_teacher(self):
        fields = [
            ("Name", ""),
            ("Contact", ""),
            ("Username", ""),
            ("Password", "")
        ]
        def submit(values):
            # If update_teacher returns None or True, treat it as success.
            result = self.teacher.update_teacher(values["Name"], values["Contact"],
                                                 values["Username"], values["Password"])
            if result is None or result:
                messagebox.showinfo("Success", "Profile updated successfully.")
                return True
            else:
                messagebox.showerror("Error", "Failed to update profile.")
                return False
        FormWindow(self, "Update Profile", fields, submit)

    def update_student_mark(self):
        fields = [
            ("Student ID", ""),
            ("Mark", "")
        ]
        def submit(values):
            try:
                std_id = int(values["Student ID"])
            except ValueError:
                messagebox.showerror("Error", "Invalid Student ID.")
                return False
            self.teacher.school.update_student(std_id, values["Mark"])
            messagebox.showinfo("Success", f"Student ID {std_id} mark updated successfully.")
            return True
        FormWindow(self, "Update Student Mark", fields, submit)

# ------------------ Main Application Controller ------------------
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Universdity management system")
        # Set main window size to 1000x700 and center it
        width, height = 1000, 700
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)

        # Container to hold pages
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.current_frame = None
        self.show_login()

    def show_frame(self, frame_class, *args):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame_class(self.container, *args)
        self.current_frame.pack(fill="both", expand=True)

    def show_login(self):
        self.show_frame(LoginFrame, self.login_callback)

    def show_admin_dashboard(self, admin):
        self.show_frame(AdminDashboard, admin)

    def show_teacher_dashboard(self, teacher):
        self.show_frame(TeacherDashboard, teacher)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
