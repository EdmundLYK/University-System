import pandas as pd
import os
import csv

class School:
    def __init__(self):
        # Define CSV files and their headers
        self.csv_files = [
            ('employees.csv', ['employee_id', 'name', 'contact', 'position']),
            ('students.csv', ['student_id', 'name', 'class']),
            ('users.csv', ['username', 'password', 'role']),
            ('attendance.csv', ['date', 'class', 'student_id', 'status']),
            ('schedules.csv', ['class', 'teacher_id'])
        ]
        # Ensure all CSV files exist
        for filename, headers in self.csv_files:
            self.ensure_csv_exists(filename, headers)
        # Initialize DataFrames
        self.employees = pd.DataFrame(columns=['employee_id', 'name', 'contact', 'position'])
        self.students = pd.DataFrame(columns=['student_id', 'name', 'class'])
        self.users = pd.DataFrame(columns=['username', 'password', 'role'])
        self.attendance = pd.DataFrame(columns=['date', 'class', 'student_id', 'status'])
        self.schedules = pd.DataFrame(columns=['class', 'teacher_id'])
        self.load_data()

    def ensure_csv_exists(self, filename, headers=None):
        """Ensure a CSV file exists; create it with headers if it doesn't."""
        if not os.path.exists(filename):
            with open(filename, 'w', newline='') as csvfile:
                if headers:
                    writer = csv.writer(csvfile)
                    writer.writerow(headers)

    def load_data(self):
        """Load data from CSV files into DataFrames."""
        for file, attr in [
            ('employees.csv', 'employees'),
            ('students.csv', 'students'),
            ('users.csv', 'users'),
            ('attendance.csv', 'attendance'),
            ('schedules.csv', 'schedules')
        ]:
            if os.path.exists(file):
                setattr(self, attr, pd.read_csv(file))

    def save_data(self):
        """Save all DataFrames to CSV files."""
        self.employees.to_csv('employees.csv', index=False)
        self.students.to_csv('students.csv', index=False)
        self.users.to_csv('users.csv', index=False)
        self.attendance.to_csv('attendance.csv', index=False)
        self.schedules.to_csv('schedules.csv', index=False)

    def add_employee(self, name, contact, position, username=None, password=None):
        new_id = 1 if self.employees.empty else self.employees['employee_id'].max() + 1
        employee_details = {'employee_id': new_id, 'name': name, 'contact': contact, 'position': position}
        self.employees = pd.concat([self.employees, pd.DataFrame([employee_details])], ignore_index=True)
        if position in ['teacher', 'admin'] and username and password:
            user_details = {'username': username, 'password': password, 'role': position}
            self.users = pd.concat([self.users, pd.DataFrame([user_details])], ignore_index=True)
        self.save_data()
        return new_id

    def remove_employee(self, employee_id):
        self.employees = self.employees[self.employees['employee_id'] != employee_id]
        self.schedules = self.schedules[self.schedules['teacher_id'] != employee_id]
        self.save_data()

    def add_student(self, name, class_name):
        new_id = 1 if self.students.empty else self.students['student_id'].max() + 1
        student_details = {'student_id': new_id, 'name': name, 'class': class_name}
        self.students = pd.concat([self.students, pd.DataFrame([student_details])], ignore_index=True)
        self.save_data()

    def assign_teacher_to_class(self, class_name, teacher_id):
        if teacher_id in self.employees['employee_id'].values:
            schedule = {'class': class_name, 'teacher_id': teacher_id}
            self.schedules = pd.concat([self.schedules, pd.DataFrame([schedule])], ignore_index=True)
            self.save_data()

    def mark_attendance(self, class_name, date, student_id, status, teacher_id):
        if class_name in self.schedules[self.schedules['teacher_id'] == teacher_id]['class'].values:
            attendance_record = {'date': date, 'class': class_name, 'student_id': student_id, 'status': status}
            self.attendance = pd.concat([self.attendance, pd.DataFrame([attendance_record])], ignore_index=True)
            self.save_data()