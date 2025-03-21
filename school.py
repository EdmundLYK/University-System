import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import os
import csv

class School:
    def __init__(self):
        # Define CSV files and their path
        self.csv_files = [
            ('csv/employees.csv', ['employee_id', 'name', 'contact', 'position', 'username', 'password', 'role']),
            ('csv/students.csv', ['student_id', 'name', 'age', 'class', 'marks']),
            ('csv/attendance.csv', ['AttendanceID', 'ClassID', 'StudentID', 'Date', 'Status']),
            ('csv/schedules.csv', ['classID', 'TeacherID', 'ClassName', 'Date', 'Duration', 'MaxStudents', 'Subject']),
            ('csv/lesson_plan.csv', ['LessonID','TeacherID','ClassID','Subject','LessonDetails','Date','LearningObjectives','Assessment'])
        ]
        # Ensure all CSV files exist
        for filename, headers in self.csv_files:
            self.ensure_csv_exists(filename, headers)
        # Initialize DataFrames
        self.employees = pd.DataFrame(columns=['employee_id', 'name', 'contact', 'position', 'username', 'password', 'role'])
        self.students = pd.DataFrame(columns=['student_id', 'name', 'age', 'class', 'marks']) 
        self.attendance = pd.DataFrame(columns=['date', 'class', 'student_id', 'status'])
        self.schedules = pd.DataFrame(columns=['classID', 'TeacherID', 'ClassName', 'Date', 'Duration', 'MaxStudents', 'Subject'])
        self.lesson_plan = pd.DataFrame(columns=['LessonID','TeacherID','ClassID','Subject','LessonDetails','Date','LearningObjectives','Assessment'])
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
            ('csv/schedules.csv', 'schedules'),
            ('csv/lesson_plan.csv', 'lesson_plan')
        ]:
            if os.path.exists(file):
                setattr(self, attr, pd.read_csv(file))

    def save_data(self):
        """Save all DataFrames to CSV files."""
        self.employees.to_csv('csv/employees.csv', index=False)
        self.students.to_csv('csv/students.csv', index=False)
        self.attendance.to_csv('csv/attendance.csv', index=False)
        self.schedules.to_csv('csv/schedules.csv', index=False)
        self.lesson_plan.to_csv('csv/lesson_plan.csv', index=False)

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
    
    def assign_teacher_to_class(self, class_id, teacher_id, date_str):
        # Convert class_id to integer
        try:
            class_id = int(class_id)
        except ValueError:
            print("Invalid class ID format")
            return False
            
        # First, check if the teacher exists.
        if teacher_id not in self.employees['employee_id'].values:
            return False

        # Find the row in schedules matching both the class_id and the converted date.
        matching_rows = self.schedules[(self.schedules['classID'] == class_id) & (self.schedules['Date'] == date_str)]
        
        # If a matching row exists, update its TeacherID.
        if not matching_rows.empty:
            row_index = matching_rows.index[0]
            self.schedules.at[row_index, 'TeacherID'] = teacher_id
            self.save_data()
            return True
        else:
            # No matching row found; let the caller know so they can retry.
            return True
    
    def mark_attendance(self, class_id, student_id, date, status):
        new_id = 1 if self.attendance.empty else self.attendance['AttendanceID'].max() + 1
        attendance_record = {'AttendanceID': new_id,'ClassID': class_id, 'StudentID': student_id, 'Date': date, 'Status': status}
        self.attendance = pd.concat([self.attendance, pd.DataFrame([attendance_record])], ignore_index=True)
        self.save_data()
    
    def update_attendance(self, attendance_id, class_id, student_id, date, status):
        if attendance_id not in self.attendance['AttendanceID'].values:
            return False
        index = self.attendance[self.attendance['AttendanceID'] == attendance_id].index[0]

        if class_id:
            self.students.at[index, 'ClassID'] = class_id
        if student_id:
            self.students.at[index, 'StudentID'] = student_id
        if date:
            self.students.at[index, 'Date'] = date
        if status:
            self.students.at[index, 'status'] = status
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

    def update_class_details(self, class_id, teacher_id, class_name, date, duration, max_students, subject):
        # First, check if the teacher exists
        if teacher_id not in self.employees['employee_id'].values:
            return False

        # Look for rows in schedules with the matching class_id
        matching_rows = self.schedules[self.schedules['classID'] == class_id]

        if not matching_rows.empty:
            # Check if any of these rows already have the same date
            same_date_rows = matching_rows[matching_rows['Date'] == date]
            if not same_date_rows.empty:
                # If a row with the same date exists, update its fields.
                # (Assuming only one row should be updated; if multiple exist, update the first occurrence.)
                row_index = same_date_rows.index[0]
                if class_name:
                    self.schedules.at[row_index, 'ClassName'] = class_name
                if date:
                    self.schedules.at[row_index, 'Date'] = date
                if duration:
                    self.schedules.at[row_index, 'Duration'] = duration
                if max_students:
                    self.schedules.at[row_index, 'MaxStudents'] = max_students
                if subject:
                    self.schedules.at[row_index, 'Subject'] = subject
            else:
                # No matching date found for this class ID; create a new row.
                new_row = {
                    'classID': class_id,
                    'TeacherID': teacher_id,
                    'ClassName': class_name,
                    'Date': date,
                    'Duration': duration,
                    'MaxStudents': max_students,
                    'Subject': subject
                }
                # Insert at the next available index.
                self.schedules.loc[len(self.schedules)] = new_row
        else:
            # If no row with the given class_id exists, add a new row.
            new_row = {
                'classID': class_id,
                'TeacherID': teacher_id,
                'ClassName': class_name,
                'Date': date,
                'Duration': duration,
                'MaxStudents': max_students,
                'Subject': subject
            }
            self.schedules.loc[len(self.schedules)] = new_row

        self.save_data()
        return True

    def add_lesson_plan(self, teacher_id, class_id, subject, lesson_details, date, learning_objectives, assessment):
        new_id = 1 if self.lesson_plan.empty else self.lesson_plan['LessonID'].max() + 1
        lesson_details = {
        'LessonID': new_id, 
        'TeacherID': teacher_id, 
        'ClassID': class_id, 
        'Subject': subject,
        'LessonDetails': lesson_details, 
        'Date': date, 
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

    def attendance_report(self, class_id, date):
        attendance_data = self.attendance[
            (self.attendance['ClassID'] == class_id) &
            (self.attendance['Date'] == date)
        ]
    
        if attendance_data.empty:
            return None
    
    # Enhance the report with student names
    # Create a copy to avoid SettingWithCopyWarning
        enhanced_report = attendance_data.copy()
    
    # Add student names to the report
        student_names = {}
        for _, row in self.students.iterrows():
            student_names[row['student_id']] = row['name']
    
    # Create a new column with student names
    # Ensure we're using the correct column name for student ID in attendance data
        enhanced_report['Student Name'] = enhanced_report['StudentID'].map(
            lambda sid: student_names.get(sid, 'Unknown')
    )
    
    # Reorder columns for better readability
        columns_order = ['AttendanceID', 'ClassID', 'StudentID', 'Student Name', 'Date', 'Status']
        available_columns = [col for col in columns_order if col in enhanced_report.columns]
        enhanced_report = enhanced_report[available_columns]
    
        return enhanced_report
    
    def import_students_csv(self, file_path):
        """
        Import student records from a CSV file and append them to the existing students DataFrame.
        The CSV must contain at least the following columns: 'name', 'age', 'class'.
        Optionally, a 'marks' column can also be included.
        """
        try:
            df_import = pd.read_csv(file_path)
        except Exception as e:
            raise ValueError(f"Error reading CSV file: {e}")

        # Ensure required columns exist
        required_cols = ['name', 'age', 'class']
        for col in required_cols:
            if col not in df_import.columns:
                raise ValueError(f"Missing required column: {col}")

        # Determine the starting student_id based on existing records
        next_id = 1 if self.students.empty else int(self.students['student_id'].max()) + 1
        new_records = []

        # Iterate over each row in the imported DataFrame
        for _, row in df_import.iterrows():
            student_record = {
                'student_id': next_id,
                'name': row['name'],
                'age': row['age'],
                'class': row['class'],
                # Use the 'marks' column if available; otherwise, set as None
                'marks': row['marks'] if 'marks' in df_import.columns else None
            }
            new_records.append(student_record)
            next_id += 1

        # Append the new records and save the data
        new_students_df = pd.DataFrame(new_records)
        self.students = pd.concat([self.students, new_students_df], ignore_index=True)
        self.save_data()
        return new_records
    
    def analysis_report(self, class_id):
        # Create reports directory if it doesn't exist
        os.makedirs('reports', exist_ok=True)
        
        report = {
            'class_id': class_id,
            'attendance': {
                'count': 0,
                'present_rate': 0,
                'std_dev': 0,
            },
            'marks': {
                'count': 0,
                'average': 0,
                'std_dev': 0,
            },
            'plots': {}
        }
        
        try:
            # Get class name
            class_info = self.schedules[self.schedules['classID'] == class_id]
            if not class_info.empty:
                report['class_name'] = class_info.iloc[0]['ClassName']
            else:
                report['class_name'] = f"Class {class_id}"
            
            # Analyze attendance
            attendance_data = self.attendance[self.attendance['ClassID'] == class_id]
            if not attendance_data.empty:
                # Convert status to numeric (1 for present, 0 for absent)
                attendance_data.loc[:, 'numeric_status'] = attendance_data['Status'].apply(
                    lambda x: 1 if x.lower() == 'present' else 0
                )
                
                report['attendance']['count'] = len(attendance_data)
                report['attendance']['present_rate'] = attendance_data['numeric_status'].mean() * 100
                report['attendance']['std_dev'] = attendance_data['numeric_status'].std() * 100
                
                # Plot attendance data
                plt.figure(figsize=(10, 6))
                
                # Attendance over time
                if 'Date' in attendance_data.columns:
                    # Group by date and calculate attendance rate
                    attendance_by_date = attendance_data.groupby('Date')['numeric_status'].mean() * 100
                    
                    plt.subplot(1, 2, 1)
                    attendance_by_date.plot(kind='line', marker='o')
                    plt.title('Attendance Rate Over Time')
                    plt.xlabel('Date')
                    plt.ylabel('Attendance Rate (%)')
                    plt.grid(True)
                    
                    # Attendance distribution
                    plt.subplot(1, 2, 2)
                    labels = ['Present', 'Absent']
                    counts = [
                        (attendance_data['Status'].str.lower() == 'present').sum(),
                        (attendance_data['Status'].str.lower() == 'absent').sum()
                    ]
                    plt.pie(counts, labels=labels, autopct='%1.1f%%', colors=['#4CAF50', '#F44336'])
                    plt.title('Attendance Distribution')
                
                plt.tight_layout()
                attendance_plot_path = f'reports/class_{class_id}_attendance.png'
                plt.savefig(attendance_plot_path)
                plt.close()
                report['plots']['attendance'] = attendance_plot_path
            
            # Analyze student marks
            # Get students in this class
            class_students = self.students[self.students['class'] == class_id]
            if not class_students.empty:
                # Filter out rows where marks is NaN or None
                marks_data = class_students['marks'].dropna()
                
                # Convert marks to numeric values
                marks_data = pd.to_numeric(marks_data, errors='coerce').dropna()
                
                if not marks_data.empty:
                    report['marks']['count'] = len(marks_data)
                    report['marks']['average'] = marks_data.mean()
                    report['marks']['std_dev'] = marks_data.std()
                    
                    # Plot marks distribution
                    plt.figure(figsize=(10, 6))
                    
                    # Histogram of marks
                    plt.subplot(1, 2, 1)
                    plt.hist(marks_data, bins=10, color='#2196F3', edgecolor='black')
                    plt.axvline(marks_data.mean(), color='red', linestyle='dashed', linewidth=2, 
                            label=f'Mean: {marks_data.mean():.2f}')
                    plt.title('Distribution of Student Marks')
                    plt.xlabel('Marks')
                    plt.ylabel('Number of Students')
                    plt.legend()
                    plt.grid(True)
                    
                    # Grade distribution
                    plt.subplot(1, 2, 2)
                    # Define grade ranges
                    grade_ranges = [
                        (0, 40, 'F'),
                        (40, 50, 'D'),
                        (50, 60, 'C'),
                        (60, 70, 'B'),
                        (70, 80, 'B+'),
                        (80, 90, 'A'),
                        (90, 101, 'A+')
                    ]
                    
                    grades = []
                    for mark in marks_data:
                        for low, high, grade in grade_ranges:
                            if low <= mark < high:
                                grades.append(grade)
                                break
                    
                    grade_counts = {}
                    for grade in set(grades):
                        grade_counts[grade] = grades.count(grade)
                    
                    # Sort grades in proper order
                    sorted_grades = []
                    sorted_counts = []
                    for _, _, grade in grade_ranges:
                        if grade in grade_counts:
                            sorted_grades.append(grade)
                            sorted_counts.append(grade_counts[grade])
                    
                    plt.bar(sorted_grades, sorted_counts, color='#FF9800')
                    plt.title('Grade Distribution')
                    plt.xlabel('Grade')
                    plt.ylabel('Number of Students')
                    plt.grid(True, axis='y')
                    
                    plt.tight_layout()
                    marks_plot_path = f'reports/class_{class_id}_marks.png'
                    plt.savefig(marks_plot_path)
                    plt.close()
                    report['plots']['marks'] = marks_plot_path
                    
                    # Create a summary plot
                    plt.figure(figsize=(12, 8))
                    plt.suptitle(f"Analysis Report for {report['class_name']} (ID: {class_id})", fontsize=16)
                    
                    # Add text summary
                    summary_text = (
                        f"Attendance Statistics:\n"
                        f"  - Total Records: {report['attendance']['count']}\n"
                        f"  - Present Rate: {report['attendance']['present_rate']:.2f}%\n"
                        f"  - Standard Deviation: {report['attendance']['std_dev']:.2f}%\n\n"
                        f"Marks Statistics:\n"
                        f"  - Total Students: {report['marks']['count']}\n"
                        f"  - Average Mark: {report['marks']['average']:.2f}\n"
                        f"  - Standard Deviation: {report['marks']['std_dev']:.2f}"
                    )
                    
                    plt.figtext(0.1, 0.5, summary_text, fontsize=12, 
                            bbox=dict(facecolor='#E3F2FD', alpha=0.5))
                    
                    summary_plot_path = f'reports/class_{class_id}_summary.png'
                    plt.savefig(summary_plot_path)
                    plt.close()
                    report['plots']['summary'] = summary_plot_path
        
        except Exception as e:
            report['error'] = str(e)
        # This is for #Jostrix
        return report

        

