import pandas as pd
import os
import csv

class School:
    def __init__(self):
        # Define CSV files and their path
        self.csv_files = [
            ('csv/employees.csv', ['employee_id', 'name', 'contact', 'position', 'username', 'password', 'role']),
            ('csv/students.csv', ['student_id', 'name', 'age', 'class', 'marks']),
            ('csv/attendance.csv', ['date', 'class', 'student_id', 'status']),
            ('csv/schedules.csv', ['classID', 'TeacherID', 'ClassName', 'Time', 'Day', 'Duration', 'MaxStudents', 'Subject']),
            ('csv/lesson_plan.csv', ['LessonID','TeacherID','ClassID','Subject','LessonDetails','Date','Materials','LearningObjectives','Assessment'])
        ]
        # Ensure all CSV files exist
        for filename, headers in self.csv_files:
            self.ensure_csv_exists(filename, headers)
        # Initialize DataFrames
        self.employees = pd.DataFrame(columns=['employee_id', 'name', 'contact', 'position', 'username', 'password', 'role'])
        self.students = pd.DataFrame(columns=['student_id', 'name', 'age', 'class', 'marks']) 
        self.attendance = pd.DataFrame(columns=['date', 'class', 'student_id', 'status'])
        self.schedules = pd.DataFrame(columns=['classID', 'TeacherID', 'ClassName', 'Time', 'Day', 'Duration', 'MaxStudents', 'Subject'])
        self.load_data()

    def ensure_csv_exists(self, filename, headers=None):
        """Ensure a CSV file exists in the csv subfolder; create it with headers if it doesn't."""
        # Ensure the 'csv' subfolder exists
        os.makedirs('csv', exist_ok=True)
        if not os.path.exists(filename):
            with open(filename, 'w', newline='') as csvfile:
                if headers:
                    writer = csv.writer(csvfile)
                    writer.writerow(headers)

    def load_data(self):
        """Load data from CSV files into DataFrames."""
        for file, attr in [
            ('csv/employees.csv', 'employees'),
            ('csv/students.csv', 'students'),
            ('csv/attendance.csv', 'attendance'),
            ('csv/schedules.csv', 'schedules')
        ]:
            if os.path.exists(file):
                setattr(self, attr, pd.read_csv(file))

    def save_data(self):
        """Save all DataFrames to CSV files."""
        self.employees.to_csv('csv/employees.csv', index=False)
        self.students.to_csv('csv/students.csv', index=False)
        self.attendance.to_csv('csv/attendance.csv', index=False)
        self.schedules.to_csv('csv/schedules.csv', index=False)

    def add_employee(self, name, contact, position, username=None, password=None):
        new_id = 1 if self.employees.empty else self.employees['employee_id'].max() + 1
        role = position if position in ['admin', 'teacher'] else 'staff'
        employee_details = {
            'employee_id': new_id,
            'name': name,
            'contact': contact,
            'position': position,
            'username': username if position in ['admin', 'teacher'] else None,
            'password': password if position in ['admin', 'teacher'] else None,
            'role': role
        }
        self.employees = pd.concat([self.employees, pd.DataFrame([employee_details])], ignore_index=True)
        self.save_data()
        return new_id

    def remove_employee(self, employee_id):
        self.employees = self.employees[self.employees['employee_id'] != employee_id]
        if 'teacher_id' in self.schedules.columns:
            self.schedules = self.schedules[self.schedules['teacher_id'] != employee_id]
        self.save_data()

    def update_employee(self, employee_id, name=None, contact=None, position=None, username=None, password=None):
        if employee_id not in self.employees['employee_id'].values:
            return False
        index = self.employees[self.employees['employee_id'] == employee_id].index[0]

        if name:
            self.employees.at[index, 'name'] = name
        if contact:
            self.employees.at[index, 'contact'] = contact
        if position:
            self.employees.at[index, 'position'] = position
            # Adjust the role based on position
            self.employees.at[index, 'role'] = position if position in ['admin', 'teacher'] else 'staff'
        if username:
            self.employees.at[index, 'username'] = username
        if password:
            self.employees.at[index, 'password'] = password
        self.save_data()

    def add_student(self, age, name, class_id):
        new_id = 1 if self.students.empty else self.students['student_id'].max() + 1
        student_details = {'student_id': new_id, 'name': name, 'age': age, 'class': class_id}
        self.students = pd.concat([self.students, pd.DataFrame([student_details])], ignore_index=True)
        self.save_data()

    def remove_student(self, student_id):
        self.students = self.students[self.students['student_id'] != student_id]
        self.save_data()
    
    def update_student(self, student_id, name=None, age=None, class_id=None, mark=None):
        if student_id not in self.students['student_id'].values:
            return False
        index = self.students[self.students['student_id'] == student_id].index[0]

        if name:
            self.students.at[index, 'name'] = name
        if age:
            self.students.at[index, 'age'] = age
        if class_id:
            self.students.at[index, 'class'] = class_id
        if mark:
            self.students.at[index, 'marks'] = mark
        self.save_data()

    def update_teacher(self, employee_id, name=None, contact=None, username=None, password=None):
        if employee_id not in self.employees['employee_id'].values:
            return False
        index = self.employees[self.employees['employee_id'] == employee_id].index[0]

        if name:
            self.employees.at[index, 'name'] = name
        if contact:
            self.employees.at[index, 'contact'] = contact
        if username:
            self.employees.at[index, 'username'] = username
        if password:
            self.employees.at[index, 'password'] = password
        self.save_data()
    
    # change for schedule
    def assign_teacher_to_class(self, class_id, teacher_id,):
        if teacher_id not in self.employees['employee_id'].values:
            return False
        schedule_details = {'classID': class_id, 'TeacherID': teacher_id,}        
        self.schedules = pd.concat([self.schedules, pd.DataFrame([schedule_details])], ignore_index=True)
        self.save_data()
    
    # havent implement
    def mark_attendance(self, class_name, date, student_id, status, teacher_id):
        if class_name in self.schedules[self.schedules['teacher_id'] == teacher_id]['class'].values:
            attendance_record = {'date': date, 'class': class_name, 'student_id': student_id, 'status': status}
            self.attendance = pd.concat([self.attendance, pd.DataFrame([attendance_record])], ignore_index=True)
            self.save_data()
    
    def update_student_mark(self, student_id, name=None, age=None, class_id=None, mark=None):
        if student_id not in self.students['student_id'].values:
            return False
        index = self.students[self.students['student_id'] == student_id].index[0]

        if name:
            self.students.at[index, 'name'] = name
        if age:
            self.students.at[index, 'age'] = age
        if class_id:
            self.students.at[index, 'class_id'] = class_id
        if mark is not None:  # Use 'is not None' to allow for mark=0
            self.students.at[index, 'mark'] = mark
        self.save_data()

    def update_class_details(self, class_id, teacher_id, class_name, time, day, duration, max_students, subject):
        if teacher_id not in self.employees['employee_id'].values:
            return False
        index = self.employees[self.employees['employee_id'] == teacher_id].index[0]

        if class_name:
            self.schedules.at[index, 'ClassName'] = class_name
        if time:
            self.students.at[index, 'Time'] = time
        if day:
            self.students.at[index, 'Day'] = day
        if duration:
            self.students.at[index, 'Duration'] = duration
        if max_students:
            self.students.at[index, 'MaxStudents'] = max_students
        if subject:
            self.students.at[index, 'Subject'] = subject
        self.save_data()

    def add_lesson_plan(self, teacher_id, class_id, subject, lesson_details, date, materials, learning_objectives, assessment):
        new_id = 1 if self.lesson_plan.empty else self.lesson_plan['LessonID'].max() + 1
        lesson_details = {
            'LessonID': new_id, 
            'TeacherID': teacher_id, 
            'ClassID': class_id, 
            'Subject': subject,
            'LessonDetails': lesson_details, 
            'Date': date, 
            'Materials': materials, 
            'LearningObjectives': learning_objectives, 
            'Assessment': assessment, 
            }
        self.lesson_plan = pd.concat([self.lesson_plan, pd.DataFrame([lesson_details])], ignore_index=True)
        self.save_data()
        return new_id

    def update_lesson_plan(self, lesson_id, teacher_id, class_id, subject, lesson_details, date, materials, learning_objectives, assessment):
        if teacher_id not in self.employees['employee_id'].values:
            return False
        index = self.employees[self.employees['employee_id'] == teacher_id].index[0]

        if lesson_id:
            self.lesson_plan.at[index, 'LessonID'] = lesson_id
        if class_id:
            self.lesson_plan.at[index, 'ClassID'] = class_id
        if subject:
            self.lesson_plan.at[index, 'Subject'] = subject
        if lesson_details:
            self.lesson_plan.at[index, 'LessonDetails'] = lesson_details
        if date:
            self.lesson_plan.at[index, 'Date'] = date
        if materials:
            self.lesson_plan.at[index, 'Materials'] = materials
        if learning_objectives:
            self.lesson_plan.at[index, 'LearningObjectives'] = learning_objectives
        if assessment:
            self.lesson_plan.at[index, 'Assessment'] = assessment
        self.save_data()