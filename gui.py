from curses.panel import bottom_panel
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import Canvas, Entry, Button, PhotoImage
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from pathlib import Path
import pandas as pd  
from person import Admin, Teacher  

# ------------------ Paths and Asset Helper ------------------
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets"

# This is made for #Jostrix and #EdmundLYK
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# ------------------ FormWindow Helper Class ------------------
class FormWindow(tk.Toplevel):
    def __init__(self, parent, title, fields, submit_callback):
        super().__init__(parent)
        self.title(title)
        
        # Set window size and center it
        width, height = 1000, 550
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)
        self.configure(bg="#8B0000")
        
        # Make the window modal and transient so it stays on top
        self.transient(parent)
        self.grab_set()
        
        # Create a canvas covering the window
        self.canvas = Canvas(
            self,
            bg="#8B0000",
            height=500,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        # Bottom background image:
        self.carbon_bg = PhotoImage(file=relative_to_assets("image_2.png"))
        self.canvas.carbon_bg = self.carbon_bg
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
            
            lbl = tk.Label(self, text=field_label, font=("Inter", 20), bg="#8B0000", fg="#FFFFFF")
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
        super().__init__(parent, bg="#8B0000")
        self.login_callback = login_callback
        self.configure(width=1000, height=700)
        self.pack_propagate(0)
        
        self.canvas = Canvas(
            self,
            bg="#8B0000",
            height=700,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        # Bottom background: carbon.png
        self.carbon_bg = PhotoImage(file=relative_to_assets("image_2.png"))
        self.canvas.carbon_bg = self.carbon_bg
        self.canvas.create_image(500, 350, image=self.carbon_bg)
        
        # Top background: image_1.png
        self.top_bg = PhotoImage(file=relative_to_assets("image_1.png"))
        self.canvas.top_bg = self.top_bg
        self.canvas.create_image(500, 350, image=self.top_bg)

        self.canvas.create_text(
            170, 29,
            anchor="nw",
            text="University Management System",
            fill="#FFF2F2",
            font=("Roboto Regular", 45 * -1)
        )

        self.canvas.create_text(
            279, 171,
            anchor="nw",
            text="Username",
            fill="#FFF8F8",
            font=("Inter", 16 * -1)
        )

        self.entry_bg_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        self.canvas.create_image(498.5, 184, image=self.entry_bg_1)

        self.username_entry = Entry(
            self,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0,
            font=("Inter", 20)
        )
        self.username_entry.place(x=384, y=150, width=229, height=66)
        self.username_entry.bind("<Return>", lambda event: self.login())

        self.canvas.create_text(
            278, 284,
            anchor="nw",
            text="Password",
            fill="#FFF8F8",
            font=("Inter", 16 * -1)
        )

        self.entry_bg_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        self.canvas.create_image(498.5, 298, image=self.entry_bg_2)

        self.password_entry = Entry(
            self,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0,
            show="*",
            font=("Inter", 20)
        )
        self.password_entry.place(x=384, y=264, width=229, height=66)
        self.password_entry.bind("<Return>", lambda event: self.login())

        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.login_button = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.login,
            relief="flat"
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
        self.parent = parent
        self.configure(width=1000, height=700)
        self.pack_propagate(0)
        
        
        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=700,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        self.bg_image = PhotoImage(file=relative_to_assets("image_2.png"))
        self.canvas.create_image(500, 350, image=self.bg_image)
        
        self.canvas.create_text(
            305, 29,
            anchor="nw",
            text="ADMIN DASHBOARD",
            fill="#FFFFFF",
            font=("InknutAntiqua Bold", 40 * -1)
        )
        
        # Four main buttons
        self.button_image_1 = PhotoImage(file=relative_to_assets("emp.png"))
        self.button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_employee_management,
            relief="flat"
        )
        self.button_1.place(x=124, y=194, width=243, height=118)
        
        self.button_image_3 = PhotoImage(file=relative_to_assets("class.png"))
        self.button_3 = Button(
            self,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_class_management,
            relief="flat"
        )
        self.button_3.place(x=617, y=194, width=243, height=118)
        
        self.button_image_4 = PhotoImage(file=relative_to_assets("std.png"))
        self.button_4 = Button(
            self,
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_student_management,
            relief="flat"
        )
        self.button_4.place(x=124, y=444, width=243, height=118)
        
        self.button_image_2 = PhotoImage(file=relative_to_assets("logout.png"))
        self.button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: parent.show_login(),
            relief="flat"
        )
        self.button_2.place(x=617, y=444, width=243, height=118)
        
        # Container for management frames
        self.management_container = tk.Frame(self)
        self.current_management_frame = None

    def show_management_frame(self, frame_class, *args):
        # Remove any existing management frame
        if self.current_management_frame is not None:
            self.current_management_frame.destroy()
            
        # Create and place the management container if not already visible
        self.management_container = tk.Frame(self, bg="#8B0000", bd=2, relief=tk.RAISED)
        self.management_container.place(relx=0.5, rely=0.5, anchor="center", width=800, height=600)
        
        # Add a close button at the top
        close_btn = tk.Button(self.management_container, text="X", font=("Arial", 12), 
                             command=self.close_management_frame, bg="#FF0000", fg="#FFFFFF")
        close_btn.pack(anchor="ne", padx=5, pady=5)
        
        # Create the new frame
        self.current_management_frame = frame_class(self.management_container, *args)
        self.current_management_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def close_management_frame(self):
        if self.management_container is not None:
            self.management_container.destroy()
            self.current_management_frame = None
    
    def open_employee_management(self):
        self.show_management_frame(EmployeeManagementFrame, self.admin)
    
    def open_student_management(self):
        self.show_management_frame(StudentManagementFrame, self.admin)
    
    def open_class_management(self):
        self.show_management_frame(ClassManagementFrame, self.admin)

# New frame classes for each management type
class EmployeeManagementFrame(tk.Frame):
    def __init__(self, parent, admin):
        super().__init__(parent, bg="#8B0000")
        self.admin = admin
        
        tk.Label(self, text="Employee Management", font=("Arial", 20), bg="#8B0000", fg="#FFFFFF").pack(pady=10)
        
        # Button panel
        button_panel = tk.Frame(self, bg="#8B0000")
        button_panel.pack(pady=10)
        
        btn_font = ("Inter", 16)
        tk.Button(button_panel, text="Add Employee", font=btn_font, command=self.add_employee).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_panel, text="Update Employee", font=btn_font, command=self.update_employee).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_panel, text="Remove Employee", font=btn_font, command=self.remove_employee).grid(row=0, column=2, padx=5, pady=5)
        
        # Add refresh button
        refresh_btn = tk.Button(button_panel, text="🔄", font=btn_font, bg="#4CAF50", fg="white", 
                              command=self.display_employee_data)
        refresh_btn.grid(row=0, column=3, padx=5, pady=5)
        
        # Data view panel
        self.data_panel = tk.Frame(self, bg="#FFFFFF")
        self.data_panel.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Display employee data by default
        self.display_employee_data()
    
    def display_employee_data(self):
    # Clear any existing widgets
        for widget in self.data_panel.winfo_children():
            widget.destroy()
    
        try:
            df = pd.read_csv("csv/employees.csv")
        
        # Create a header with refresh time
            header_frame = tk.Frame(self.data_panel, bg="#FFFFFF")
            header_frame.pack(fill="x")
        
            header = tk.Label(header_frame, text="Employee Details", font=("Arial", 16, "bold"), 
                          bg="#FFFFFF", fg="#000000", pady=5)
            header.pack(side="left")
        
            refresh_time = tk.Label(header_frame, text=f"Last refreshed: {pd.Timestamp.now().strftime('%H:%M:%S')}", 
                               font=("Arial", 10), bg="#FFFFFF", fg="#666666")
            refresh_time.pack(side="right", padx=10)
        
        # Create a scrolled text widget for displaying the data
            st = ScrolledText(self.data_panel, font=("Consolas", 10))
            st.pack(fill="both", expand=True, padx=5, pady=5)
            st.insert(tk.END, df.to_string())
            st.config(state=tk.DISABLED)
        
        except Exception as e:
            error_label = tk.Label(self.data_panel, text=f"Failed to read employees.csv:\n{e}", 
                              bg="#FFFFFF", fg="#FF0000", pady=10)
            error_label.pack(fill="both", expand=True)
    
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
            
            employee_id = self.admin.add_employee(values["Name"], values["Contact"], values["Position"], values["Username"], values["Password"])
            messagebox.showinfo("Success", f"Employee added with ID: {employee_id}")
            # Refresh the display
            self.display_employee_data()
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
            
            self.admin.update_employee(emp_id, values["Name"], values["Contact"], values["Position"], values["Username"], values["Password"])
            messagebox.showinfo("Success", f"Employee ID {emp_id} updated successfully.")
            # Refresh the display
            self.display_employee_data()
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
            # Refresh the display
            self.display_employee_data()
            return True
        
        FormWindow(self, "Remove Employee", fields, submit)

class StudentManagementFrame(tk.Frame):
    def __init__(self, parent, admin):
        super().__init__(parent, bg="#8B0000")
        self.admin = admin
        
        tk.Label(self, text="Student Management", font=("Arial", 20), bg="#8B0000", fg="#FFFFFF").pack(pady=10)
        
        # Button panel
        button_panel = tk.Frame(self, bg="#8B0000")
        button_panel.pack(pady=10)
        
        btn_font = ("Inter", 16)
        tk.Button(button_panel, text="Add Student", font=btn_font, command=self.add_student).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_panel, text="Update Student", font=btn_font, command=self.update_student).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_panel, text="Remove Student", font=btn_font, command=self.remove_student).grid(row=0, column=2, padx=5, pady=5)
        
        # Add Import Students button
        import_btn = tk.Button(button_panel, text="Import Students", font=btn_font, bg="#007BFF", fg="white", 
                             command=self.import_students)
        import_btn.grid(row=0, column=3, padx=5, pady=5)
        
        # Add refresh button
        refresh_btn = tk.Button(button_panel, text="🔄", font=btn_font, bg="#4CAF50", fg="white", 
                              command=self.display_student_data)
        refresh_btn.grid(row=0, column=4, padx=5, pady=5)
        
        # Data view panel
        self.data_panel = tk.Frame(self, bg="#FFFFFF")
        self.data_panel.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Display student data by default
        self.display_student_data()
        
    # Add the import_students method
    def import_students(self):
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        
        if not file_path:  # User canceled the file dialog
            return
            
        try:
            # Use the import_students_csv method from school class
            new_records = self.admin.school.import_students_csv(file_path)
            
            # Show success message with count of imported records
            messagebox.showinfo("Import Successful", f"Successfully imported {len(new_records)} student records.")
            
            # Refresh the display
            self.display_student_data()
            
        except Exception as e:
            messagebox.showerror("Import Error", str(e))
            
    def display_student_data(self):
    # Clear any existing widgets
        for widget in self.data_panel.winfo_children():
            widget.destroy()
    
        try:
            df = pd.read_csv("csv/students.csv")
        
        # Create a header with refresh time
            header_frame = tk.Frame(self.data_panel, bg="#FFFFFF")
            header_frame.pack(fill="x")
        
            header = tk.Label(header_frame, text="Student Profiles", font=("Arial", 16, "bold"), 
                          bg="#FFFFFF", fg="#000000", pady=5)
            header.pack(side="left")
        
            refresh_time = tk.Label(header_frame, text=f"Last refreshed: {pd.Timestamp.now().strftime('%H:%M:%S')}", 
                               font=("Arial", 10), bg="#FFFFFF", fg="#666666")
            refresh_time.pack(side="right", padx=10)
        
        # Create a scrolled text widget for displaying the data
            st = ScrolledText(self.data_panel, font=("Consolas", 10))
            st.pack(fill="both", expand=True, padx=5, pady=5)
            st.insert(tk.END, df.to_string())
            st.config(state=tk.DISABLED)
        
        except Exception as e:
            error_label = tk.Label(self.data_panel, text=f"Failed to read students.csv:\n{e}", 
                              bg="#FFFFFF", fg="#FF0000", pady=10)
            error_label.pack(fill="both", expand=True)
    
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
            # Refresh the display
            self.display_student_data()
            return True
        
        FormWindow(self, "Add Student", fields, submit)
    
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
            # Refresh the display
            self.display_student_data()
            return True
        
        FormWindow(self, "Update Student", fields, submit)
    
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
            # Refresh the display
            self.display_student_data()
            return True
        
        FormWindow(self, "Remove Student", fields, submit)

class ClassManagementFrame(tk.Frame):
    def __init__(self, parent, admin):
        super().__init__(parent, bg="#8B0000")
        self.admin = admin
        
        tk.Label(self, text="Class Management", font=("Arial", 20), bg="#8B0000", fg="#FFFFFF").pack(pady=10)
        
        # Button panel
        button_panel = tk.Frame(self, bg="#8B0000")
        button_panel.pack(pady=10)
        
        btn_font = ("Inter", 16)
        # Changed from pack to grid to align with the refresh button
        tk.Button(button_panel, text="Assign Teacher to Class", font=btn_font, 
                 command=self.assign_teacher).grid(row=0, column=0, padx=5, pady=5)
          
           # New Generate Report button
        tk.Button(button_panel, text="Attendance Report", font=btn_font, 
                 command=self.generate_report).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Button(button_panel, text="Academic Report", font=btn_font, 
                 command=self.generate_class_report).grid(row=0, column=2, padx=5, pady=5)

        # Add refresh button
        refresh_btn = tk.Button(button_panel, text="🔄", font=btn_font, bg="#4CAF50", fg="white", 
                              command=self.display_class_schedules)
        refresh_btn.grid(row=0, column=3, padx=5, pady=5)
        
        # Data view panel
        self.data_panel = tk.Frame(self, bg="#FFFFFF")
        self.data_panel.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Display class schedules by default
        self.display_class_schedules()
    
    def display_class_schedules(self):
    # Clear any existing widgets
        for widget in self.data_panel.winfo_children():
            widget.destroy()

        try:
            df = pd.read_csv("csv/schedules.csv")
        
        # Create a header with refresh time
            header_frame = tk.Frame(self.data_panel, bg="#FFFFFF")
            header_frame.pack(fill="x")
        
            header = tk.Label(header_frame, text="Class Schedules", font=("Arial", 16, "bold"), 
                          bg="#FFFFFF", fg="#000000", pady=5)
            header.pack(side="left")
        
            refresh_time = tk.Label(header_frame, text=f"Last refreshed: {pd.Timestamp.now().strftime('%H:%M:%S')}", 
                               font=("Arial", 10), bg="#FFFFFF", fg="#666666")
            refresh_time.pack(side="right", padx=10)
        
        # Create a scrolled text widget for displaying the data
            st = ScrolledText(self.data_panel, font=("Consolas", 10))
            st.pack(fill="both", expand=True, padx=5, pady=5)
            st.insert(tk.END, df.to_string())
            st.config(state=tk.DISABLED)
        
        except Exception as e:
            error_label = tk.Label(self.data_panel, text=f"Failed to read schedules.csv:\n{e}", 
                              bg="#FFFFFF", fg="#FF0000", pady=10)
            error_label.pack(fill="both", expand=True)
    
    def assign_teacher(self):
        fields = [
            ("Class ID", ""),
            ("Teacher ID", ""),
            ("Date (YYYY-MM-DD)", ""),  # Updated the label to the standard format.
        ]
        
        def submit(values):
            try:
                teacher_id = int(values["Teacher ID"])
            except ValueError:
                messagebox.showerror("Error", "Invalid Teacher ID.")
                return False
            
            class_id = values["Class ID"].strip()  # Optionally strip extra whitespace.
            date_input = values["Date (YYYY-MM-DD)"].strip()
            
            # Call the function that checks class_id and date before updating.
            result = self.admin.assign_teacher_to_class(class_id, teacher_id, date_input)
            if result:
                messagebox.showinfo("Success", "Teacher assigned to class.")
                # Refresh the display.
                self.display_class_schedules()
                return True
            else:
                self.display_class_schedules()
                return True
        
        FormWindow(self, "Assign Teacher", fields, submit)
            
    def generate_report(self):
        # New function to generate the attendance report
        fields = [
            ("Class ID", ""),
            ("Date (YYYY-MM-DD)", "")
        ]
        
        def submit(values):
            try:
                class_id = int(values["Class ID"])
            except ValueError:
                messagebox.showerror("Error", "Class ID must be an integer.")
                return False
            
            date_str = values["Date (YYYY-MM-DD)"]
            # Call the attendance_report method from the school object
            report = self.admin.school.attendance_report(class_id, date_str)
            
            if report is None:
                messagebox.showinfo("No Data", "No attendance data found for the given class and date.")
            else:
                # Create a new window to display the report
                report_window = tk.Toplevel(self)
                report_window.title("Attendance Report")
                st = ScrolledText(report_window, font=("Consolas", 10))
                st.pack(fill="both", expand=True)
                st.insert(tk.END, report.to_string())
                st.config(state=tk.DISABLED)
            
            return True
        
        FormWindow(self, "Generate Attendance Report", fields, submit)

    def generate_class_report(self):
        fields = [
            ("Class ID", "")
        ]
        
        def submit(values):
            try:
                class_id = int(values["Class ID"])
                
                # Generate the report
                report = self.admin.analysis_report(class_id)
                
                if 'error' in report:
                    messagebox.showerror("Error", f"Failed to generate report: {report['error']}")
                    return False
                
                # Create a new window to display the report
                report_window = tk.Toplevel()
                report_window.title(f"Analysis Report for {report.get('class_name', f'Class {class_id}')}")
                report_window.geometry("800x600")
                
                # Create a notebook for tabs
                notebook = ttk.Notebook(report_window)
                notebook.pack(fill="both", expand=True, padx=10, pady=10)
                
                # Summary tab
                summary_tab = tk.Frame(notebook)
                notebook.add(summary_tab, text="Summary")
                
                # Display summary information
                summary_text = (
                    f"Class: {report.get('class_name', f'Class {class_id}')}\n\n"
                    f"Attendance Statistics:\n"
                    f"  - Total Records: {report['attendance']['count']}\n"
                    f"  - Present Rate: {report['attendance']['present_rate']:.2f}%\n"
                    f"  - Standard Deviation: {report['attendance']['std_dev']:.2f}%\n\n"
                    f"Marks Statistics:\n"
                    f"  - Total Students: {report['marks']['count']}\n"
                    f"  - Average Mark: {report['marks']['average']:.2f}\n"
                    f"  - Standard Deviation: {report['marks']['std_dev']:.2f}"
                )
                
                summary_label = tk.Label(summary_tab, text=summary_text, justify="left", 
                                        font=("Arial", 12), padx=20, pady=20)
                summary_label.pack(anchor="nw")
                
                # Display summary plot if available
                if 'summary' in report['plots']:
                    summary_img = tk.PhotoImage(file=report['plots']['summary'])
                    summary_img_label = tk.Label(summary_tab, image=summary_img)
                    summary_img_label.image = summary_img  # Keep a reference to prevent garbage collection
                    summary_img_label.pack(pady=10)
                
                # Attendance tab
                if 'attendance' in report['plots']:
                    attendance_tab = tk.Frame(notebook)
                    notebook.add(attendance_tab, text="Attendance")
                    
                    attendance_img = tk.PhotoImage(file=report['plots']['attendance'])
                    attendance_img_label = tk.Label(attendance_tab, image=attendance_img)
                    attendance_img_label.image = attendance_img  # Keep a reference
                    attendance_img_label.pack(pady=10)
                
                # Marks tab
                if 'marks' in report['plots']:
                    marks_tab = tk.Frame(notebook)
                    notebook.add(marks_tab, text="Marks")
                    
                    marks_img = tk.PhotoImage(file=report['plots']['marks'])
                    marks_img_label = tk.Label(marks_tab, image=marks_img)
                    marks_img_label.image = marks_img  # Keep a reference
                    marks_img_label.pack(pady=10)
                
                # Ensure the window comes to the front
                report_window.lift()
                report_window.attributes('-topmost', True)
                report_window.after_idle(report_window.attributes, '-topmost', False)
                
                # Focus on the window
                report_window.focus_force()
                
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
                return False
        
        FormWindow(self, "Generate Analysis Report", fields, submit)

# ------------------ Teacher Dashboard ------------------
class TeacherDashboard(tk.Frame):
    def __init__(self, parent, teacher):
        super().__init__(parent)
        self.teacher = teacher
        self.parent = parent
        self.configure(width=1000, height=700)
        self.pack_propagate(0)
        
        
        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=700,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        self.bg_image = PhotoImage(file=relative_to_assets("image_2.png"))
        self.canvas.create_image(500, 350, image=self.bg_image)
        
        self.canvas.create_text(
            220, 16,
            anchor="nw",
            text= f"TEACHER {self.teacher.username}'s DASHBOARD",
            fill="#FFFFFF",
            font=("InknutAntiqua Bold", 40 * -1)
        )
        
        # Four main buttons 
        self.button_image_1 = PhotoImage(file=relative_to_assets("attd.png")) 
        self.button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_attendance_management,
            relief="flat"
        )
        self.button_1.place(x=124, y=194, width=243, height=118)
        
        # Add text overlay on button 1
        self.canvas.create_text(
            180, 230,
            anchor="nw",
            text="Attendance\nManagement",
            fill="#FFFFFF",
            font=("Inter Bold", 18 * -1)
        )
        
        self.button_image_3 = PhotoImage(file=relative_to_assets("ass.png"))
        self.button_3 = Button(
            self,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_student_assessment,
            relief="flat"
        )
        self.button_3.place(x=617, y=194, width=243, height=118)
        
        # Add text overlay on button 3
        self.canvas.create_text(
            680, 230,
            anchor="nw",
            text="Student\nAssessment",
            fill="#FFFFFF",
            font=("Inter Bold", 18 * -1)
        )
        
        self.button_image_4 = PhotoImage(file=relative_to_assets("prof.png"))
        self.button_4 = Button(
            self,
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_profile_management,
            relief="flat"
        )
        self.button_4.place(x=124, y=444, width=243, height=118)
        
        # Add text overlay on button 4
        self.canvas.create_text(
            180, 480,
            anchor="nw",
            text="Profile\nManagement",
            fill="#FFFFFF",
            font=("Inter Bold", 18 * -1)
        )
        
        self.button_image_2 = PhotoImage(file=relative_to_assets("logout.png"))
        self.button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: parent.show_login(),
            relief="flat"
        )
        self.button_2.place(x=617, y=444, width=243, height=118)
        
        # Add text overlay on button 2
        self.canvas.create_text(
            700, 480,
            anchor="nw",
            text="Logout",
            fill="#FFFFFF",
            font=("Inter Bold", 18 * -1)
        )
        
        # Container for management frames
        self.management_container = tk.Frame(self)
        self.current_management_frame = None

    def show_management_frame(self, frame_class, *args):
        # Remove any existing management frame
        if self.current_management_frame is not None:
            self.current_management_frame.destroy()
            
        # Create and place the management container if not already visible
        self.management_container = tk.Frame(self, bg="#8B0000", bd=2, relief=tk.RAISED)
        self.management_container.place(relx=0.5, rely=0.5, anchor="center", width=800, height=600)
        
        # Add a close button at the top
        close_btn = tk.Button(self.management_container, text="X", font=("Arial", 12), 
                             command=self.close_management_frame, bg="#FF0000", fg="#FFFFFF")
        close_btn.pack(anchor="ne", padx=5, pady=5)
        
        # Create the new frame
        self.current_management_frame = frame_class(self.management_container, *args)
        self.current_management_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def close_management_frame(self):
        if self.management_container is not None:
            self.management_container.destroy()
            self.current_management_frame = None
    
    def open_attendance_management(self):
        self.show_management_frame(AttendanceManagementFrame, self.teacher)
    
    def open_student_assessment(self):
        self.show_management_frame(StudentAssessmentFrame, self.teacher)
    
    def open_profile_management(self):
        self.show_management_frame(ProfileManagementFrame, self.teacher)
    

class AttendanceManagementFrame(tk.Frame):
    def __init__(self, parent, teacher):
        super().__init__(parent, bg="#8B0000")
        self.teacher = teacher
        
        tk.Label(self, text="Attendance Management", font=("Arial", 20), bg="#8B0000", fg="#FFFFFF").pack(pady=10)
        
        # Button panel
        button_panel = tk.Frame(self, bg="#8B0000")
        button_panel.pack(pady=10)
        
        btn_font = ("Inter", 16)
        tk.Button(button_panel, text="Mark Attendance", font=btn_font, command=self.mark_attendance).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_panel, text="View Attendance Records", font=btn_font, command=self.view_attendance).grid(row=0, column=1, padx=5, pady=5)
        
        # Add refresh button
        refresh_btn = tk.Button(button_panel, text="🔄", font=btn_font, bg="#4CAF50", fg="white", 
                              command=self.display_attendance_data)
        refresh_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Data view panel
        self.data_panel = tk.Frame(self, bg="#FFFFFF")
        self.data_panel.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Display attendance data by default
        self.display_attendance_data()
    
    def display_attendance_data(self):
        # Clear any existing widgets
        for widget in self.data_panel.winfo_children():
            widget.destroy()
        
        try:
            df = pd.read_csv("csv/attendance.csv")
            
            # Create a header with refresh time
            header_frame = tk.Frame(self.data_panel, bg="#FFFFFF")
            header_frame.pack(fill="x")
            
            header = tk.Label(header_frame, text="Attendance Records", font=("Arial", 16, "bold"), 
                              bg="#FFFFFF", fg="#000000", pady=5)
            header.pack(side="left")
            
            refresh_time = tk.Label(header_frame, text=f"Last refreshed: {pd.Timestamp.now().strftime('%H:%M:%S')}", 
                                   font=("Arial", 10), bg="#FFFFFF", fg="#666666")
            refresh_time.pack(side="right", padx=10)
            
            # Create a scrolled text widget for displaying the data
            st = ScrolledText(self.data_panel, font=("Consolas", 10))
            st.pack(fill="both", expand=True, padx=5, pady=5)
            st.insert(tk.END, df.to_string())
            st.config(state=tk.DISABLED)
            
        except Exception as e:
            error_label = tk.Label(self.data_panel, text=f"Failed to read attendance.csv:\n{e}", 
                                  bg="#FFFFFF", fg="#FF0000", pady=10)
            error_label.pack(fill="both", expand=True)
    
    def mark_attendance(self):
        fields = [
            ("Class ID", ""),
            ("Date (YYYY-MM-DD)", ""),
            ("Student ID", ""),
            ("Status", "")
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
            
            self.teacher.mark_attendance(values["Class ID"], values["Date (YYYY-MM-DD)"], std_id, values["Status"])
            messagebox.showinfo("Success", "Attendance marked.")
            self.display_attendance_data()  # Refresh after making changes
            return True
        
        FormWindow(self, "Mark Attendance", fields, submit)
    
    def view_attendance(self):
        # New function to generate the attendance report
        fields = [
            ("Class ID", ""),
            ("Date (YYYY-MM-DD)", "")
        ]
        
        def submit(values):
            try:
                class_id = int(values["Class ID"])
            except ValueError:
                messagebox.showerror("Error", "Class ID must be an integer.")
                return False
            
            date_str = values["Date (YYYY-MM-DD)"]
            # Call the attendance_report method from the school object
            report = self.teacher.school.attendance_report(class_id, date_str)
            
            if report is None:
                messagebox.showinfo("No Data", "No attendance data found for the given class and date.")
            else:
                # Create a new window to display the report
                report_window = tk.Toplevel(self)
                report_window.title("Attendance Report")
                st = ScrolledText(report_window, font=("Consolas", 10))
                st.pack(fill="both", expand=True)
                st.insert(tk.END, report.to_string())
                st.config(state=tk.DISABLED)
            
            return True
        
        FormWindow(self, "Generate Attendance Report", fields, submit)

class StudentAssessmentFrame(tk.Frame):
    def __init__(self, parent, teacher):
        super().__init__(parent, bg="#8B0000")
        self.teacher = teacher
        
        tk.Label(self, text="Student Assessment", font=("Arial", 20), bg="#8B0000", fg="#FFFFFF").pack(pady=10)
        
        # Button panel
        button_panel = tk.Frame(self, bg="#8B0000")
        button_panel.pack(pady=10)
        
        btn_font = ("Inter", 16)
        tk.Button(button_panel, text="Update Student Mark", font=btn_font, command=self.update_student_mark).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_panel, text="View Class Report", font=btn_font, command=self.view_class_report).grid(row=0, column=1, padx=5, pady=5)
        
        # Add refresh button
        refresh_btn = tk.Button(button_panel, text="🔄", font=btn_font, bg="#4CAF50", fg="white", 
                              command=self.display_marks_data)
        refresh_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Data view panel
        self.data_panel = tk.Frame(self, bg="#FFFFFF")
        self.data_panel.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Display marks data by default
        self.display_marks_data()
    
    def display_marks_data(self):
        # Clear any existing widgets
        for widget in self.data_panel.winfo_children():
            widget.destroy()
        
        try:
            # Read students.csv which contains marks
            df = pd.read_csv("csv/students.csv")
            
            # Create a header with refresh time
            header_frame = tk.Frame(self.data_panel, bg="#FFFFFF")
            header_frame.pack(fill="x")
            
            header = tk.Label(header_frame, text="Student Marks", font=("Arial", 16, "bold"), 
                              bg="#FFFFFF", fg="#000000", pady=5)
            header.pack(side="left")
            
            refresh_time = tk.Label(header_frame, text=f"Last refreshed: {pd.Timestamp.now().strftime('%H:%M:%S')}", 
                                   font=("Arial", 10), bg="#FFFFFF", fg="#666666")
            refresh_time.pack(side="right", padx=10)
            
            # Create a scrolled text widget for displaying the data
            st = ScrolledText(self.data_panel, font=("Consolas", 10))
            st.pack(fill="both", expand=True, padx=5, pady=5)
            st.insert(tk.END, df.to_string())
            st.config(state=tk.DISABLED)
            
        except Exception as e:
            error_label = tk.Label(self.data_panel, text=f"Failed to read students.csv:\n{e}", 
                                  bg="#FFFFFF", fg="#FF0000", pady=10)
            error_label.pack(fill="both", expand=True)
    
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
            
            try:
                mark = float(values["Mark"])
                if mark < 0 or mark > 100:
                    raise ValueError("Mark must be between 0 and 100")
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid mark: {e}")
                return False
            
            self.teacher.update_student_mark(std_id, values["Mark"])
            messagebox.showinfo("Success", f"Student ID {std_id} mark updated successfully.")
            self.display_marks_data()  # Refresh after making changes
            return True
        
        FormWindow(self, "Update Student Mark", fields, submit)
    
    def view_class_report(self):
        fields = [
            ("Class ID", "")
        ]
        
        def submit(values):
            try:
                class_id = int(values["Class ID"])
                
                # Generate the report
                report = self.teacher.analysis_report(class_id)
                
                if 'error' in report:
                    messagebox.showerror("Error", f"Failed to generate report: {report['error']}")
                    return False
                
                # Create a new window to display the report
                report_window = tk.Toplevel()
                report_window.title(f"Analysis Report for {report.get('class_name', f'Class {class_id}')}")
                report_window.geometry("800x600")
                
                # Create a notebook for tabs
                notebook = ttk.Notebook(report_window)
                notebook.pack(fill="both", expand=True, padx=10, pady=10)
                
                # Summary tab
                summary_tab = tk.Frame(notebook)
                notebook.add(summary_tab, text="Summary")
                
                # Display summary information
                summary_text = (
                    f"Class: {report.get('class_name', f'Class {class_id}')}\n\n"
                    f"Attendance Statistics:\n"
                    f"  - Total Records: {report['attendance']['count']}\n"
                    f"  - Present Rate: {report['attendance']['present_rate']:.2f}%\n"
                    f"  - Standard Deviation: {report['attendance']['std_dev']:.2f}%\n\n"
                    f"Marks Statistics:\n"
                    f"  - Total Students: {report['marks']['count']}\n"
                    f"  - Average Mark: {report['marks']['average']:.2f}\n"
                    f"  - Standard Deviation: {report['marks']['std_dev']:.2f}"
                )
                
                summary_label = tk.Label(summary_tab, text=summary_text, justify="left", 
                                        font=("Arial", 12), padx=20, pady=20)
                summary_label.pack(anchor="nw")
                
                # Display summary plot if available
                if 'summary' in report['plots']:
                    summary_img = tk.PhotoImage(file=report['plots']['summary'])
                    summary_img_label = tk.Label(summary_tab, image=summary_img)
                    summary_img_label.image = summary_img  # Keep a reference to prevent garbage collection
                    summary_img_label.pack(pady=10)
                
                # Attendance tab
                if 'attendance' in report['plots']:
                    attendance_tab = tk.Frame(notebook)
                    notebook.add(attendance_tab, text="Attendance")
                    
                    attendance_img = tk.PhotoImage(file=report['plots']['attendance'])
                    attendance_img_label = tk.Label(attendance_tab, image=attendance_img)
                    attendance_img_label.image = attendance_img  # Keep a reference
                    attendance_img_label.pack(pady=10)
                
                # Marks tab
                if 'marks' in report['plots']:
                    marks_tab = tk.Frame(notebook)
                    notebook.add(marks_tab, text="Marks")
                    
                    marks_img = tk.PhotoImage(file=report['plots']['marks'])
                    marks_img_label = tk.Label(marks_tab, image=marks_img)
                    marks_img_label.image = marks_img  # Keep a reference
                    marks_img_label.pack(pady=10)
                
                # Ensure the window comes to the front
                report_window.lift()
                report_window.attributes('-topmost', True)
                report_window.after_idle(report_window.attributes, '-topmost', False)
                
                # Focus on the window
                report_window.focus_force()
                
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
                return False
        
        FormWindow(self, "Generate Analysis Report", fields, submit)



class ProfileManagementFrame(tk.Frame):
    def __init__(self, parent, teacher):
        super().__init__(parent, bg="#8B0000")
        self.teacher = teacher
        
        tk.Label(self, text="Profile Management", font=("Arial", 20), bg="#8B0000", fg="#FFFFFF").pack(pady=10)
        
        # Button panel
        button_panel = tk.Frame(self, bg="#8B0000")
        button_panel.pack(pady=10)
        
        btn_font = ("Inter", 16)
        tk.Button(button_panel, text="Update Profile", font=btn_font, command=self.update_profile).pack(pady=5)
        tk.Button(button_panel, text="View Assigned Classes", font=btn_font, command=self.view_assigned_classes).pack(pady=5)
        
        # Add new buttons for class schedules and lesson plans
        tk.Button(button_panel, text="Manage Class Schedules", font=btn_font, command=self.manage_class_schedules).pack(pady=5)
        tk.Button(button_panel, text="Create Lesson Plans", font=btn_font, command=self.create_lesson_plans).pack(pady=5)
        
        # Profile info display
        profile_frame = tk.Frame(self, bg="#FFFFFF", bd=2, relief=tk.RAISED)
        profile_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Display teacher profile data
        self.display_profile_data(profile_frame)
    
    def display_profile_data(self, frame):
    # Show teacher profile information
        try:
        # Read the employees CSV directly
            employees_df = pd.read_csv("csv/employees.csv")
        
        # Filter for this teacher's employee_id
            teacher_data = employees_df[employees_df['employee_id'] == self.teacher.employee_id]
        
            if not teacher_data.empty:
            # Get the first (and presumably only) row
                teacher_row = teacher_data.iloc[0]
            
            # Display profile
                profile_data = {
                "ID": teacher_row['employee_id'],
                "Name": teacher_row['name'],
                "Contact": teacher_row['contact'],
                "Position": teacher_row['position'],
                "Username": self.teacher.username,  # This we know is available
                "Role": teacher_row['role']
                }
            
                header = tk.Label(frame, text="Teacher Profile", font=("Arial", 16, "bold"), 
                            bg="#FFFFFF", fg="#000000", pady=5)
                header.pack(pady=10)
            
            # Display each field
                for field, value in profile_data.items():
                    field_frame = tk.Frame(frame, bg="#FFFFFF")
                    field_frame.pack(fill="x", padx=20, pady=5)
                
                    label = tk.Label(field_frame, text=f"{field}:", font=("Arial", 12, "bold"), 
                                bg="#FFFFFF", width=15, anchor="w")
                    label.pack(side="left")
                
                    value_label = tk.Label(field_frame, text=str(value), font=("Arial", 12), 
                                    bg="#FFFFFF", anchor="w")
                    value_label.pack(side="left", fill="x", expand=True)
            else:
                error_label = tk.Label(frame, text=f"Teacher with ID {self.teacher.employee_id} not found.", 
                                bg="#FFFFFF", fg="#FF0000", pady=10)
                error_label.pack(fill="both", expand=True)
            
        except Exception as e:
            error_label = tk.Label(frame, text=f"Failed to load profile data:\n{e}", 
                            bg="#FFFFFF", fg="#FF0000", pady=10)
            error_label.pack(fill="both", expand=True)
    
    def update_profile(self):
        fields = [
            ("Name", self.teacher.name if hasattr(self.teacher, 'name') else ""),
            ("Contact", self.teacher.contact if hasattr(self.teacher, 'contact') else ""),
            ("Username", self.teacher.username if hasattr(self.teacher, 'username') else ""),
            ("Password", "")
        ]
        
        def submit(values):
            result = self.teacher.update_teacher(values["Name"], values["Contact"], values["Username"], values["Password"])
            if result is None or result:
                messagebox.showinfo("Success", "Profile updated successfully.")
                # Refresh the profile display
                for widget in self.winfo_children():
                    if isinstance(widget, tk.Frame) and widget != bottom_panel:
                        widget.destroy()
                
                profile_frame = tk.Frame(self, bg="#FFFFFF", bd=2, relief=tk.RAISED)
                profile_frame.pack(fill="both", expand=True, padx=10, pady=10)
                self.display_profile_data(profile_frame)
                return True
            else:
                messagebox.showerror("Error", "Failed to update profile.")
                return False
        
        FormWindow(self, "Update Profile", fields, submit)
    
    def view_assigned_classes(self):
        # Create a new window to display assigned classes
        view_window = tk.Toplevel(self)
        view_window.title("Assigned Classes")
        
        width, height = 600, 400
        x = (view_window.winfo_screenwidth() - width) // 2
        y = (view_window.winfo_screenheight() - height) // 2
        view_window.geometry(f"{width}x{height}+{x}+{y}")
        view_window.configure(bg="#FFFFFF")
        
        try:
            # Read schedules to find classes assigned to this teacher
            schedules_df = pd.read_csv("csv/schedules.csv")
            
            # Filter for this teacher's ID
            teacher_classes = schedules_df[schedules_df['TeacherID'] == self.teacher.employee_id]
            
            if teacher_classes.empty:
                message = "No classes currently assigned to you."
            else:
                message = "Your assigned classes:\n\n" + teacher_classes.to_string()
            
            # Display the data
            tk.Label(view_window, text="Assigned Classes", font=("Arial", 16, "bold"), 
                   bg="#FFFFFF", pady=10).pack()
                   
            st = ScrolledText(view_window, font=("Consolas", 10))
            st.pack(fill="both", expand=True, padx=10, pady=10)
            st.insert(tk.END, message)
            st.config(state=tk.DISABLED)
            
        except Exception as e:
            tk.Label(view_window, text=f"Failed to load class data:\n{e}", 
                   bg="#FFFFFF", fg="#FF0000", pady=10).pack(fill="both", expand=True)
        
        # Add close button
        tk.Button(view_window, text="Close", font=("Inter", 12), command=view_window.destroy).pack(pady=10)

    def manage_class_schedules(self):
        fields = [
            ("Class ID", ""),
            ("Class Name", ""),
            ("Date(YYYY-MM-DD)", ""),
            ("Duration(Mins)", ""),
            ("Max Students", ""),
            ("Subject", "")
        ]
        
        def submit(values):
            try:
                class_id = int(values["Class ID"])
                max_students = int(values["Max Students"])
            except ValueError:
                messagebox.showerror("Error", "Class ID and Max Students must be numbers.")
                return False
            
            # Update class details in the database
            result = self.teacher.update_class_details(
                class_id, 
                self.teacher.employee_id, 
                values["Class Name"], 
                values["Date(YYYY-MM-DD)"], 
                values["Duration(Mins)"], 
                max_students, 
                values["Subject"]
            )
            
            if result is None or result:
                messagebox.showinfo("Success", "Class schedule updated successfully.")
                return True
            else:
                messagebox.showerror("Error", "Failed to update class schedule.")
                return False
        
        FormWindow(self, "Manage Class Schedule", fields, submit)
    
    def create_lesson_plans(self):
        fields = [
            ("Class ID", ""),
            ("Subject", ""),
            ("Lesson Details", ""),
            ("Date (YYYY-MM-DD)", ""),
            ("Learning Objectives", ""),
            ("Assessment Method", "")
        ]
        
        def submit(values):
            try:
                class_id = int(values["Class ID"])
            except ValueError:
                messagebox.showerror("Error", "Class ID must be a number.")
                return False
            
            # Add lesson plan to the database
            new_lesson_id = self.teacher.add_lesson_plan(
                self.teacher.employee_id,
                class_id,
                values["Subject"],
                values["Lesson Details"],
                values["Date (YYYY-MM-DD)"],
                values["Learning Objectives"],
                values["Assessment Method"]
            )
            
            if new_lesson_id:
                messagebox.showinfo("Success", f"Lesson plan created with ID: {new_lesson_id}")
                return True
            else:
                messagebox.showerror("Error", "Failed to create lesson plan.")
                return False
        
        FormWindow(self, "Create Lesson Plan", fields, submit)

# ------------------ Main Application Controller ------------------
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("University Management System")
        
        width, height = 1000, 700
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)
        
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