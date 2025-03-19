import pandas as pd
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
    
    def assign_teacher_to_class(self, class_id, teacher_id,):
        if teacher_id not in self.employees['employee_id'].values:
            return False
        schedule_details = {'classID': class_id, 'TeacherID': teacher_id,}        
        self.schedules = pd.concat([self.schedules, pd.DataFrame([schedule_details])], ignore_index=True)
        self.save_data()
    
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
        # First check if the teacher exists
        if teacher_id not in self.employees['employee_id'].values:
            return False
        
        # Then find the row in schedules where classID matches
        if class_id not in self.schedules['classID'].values:
            return False
        
        # Get the index of the class in the schedules DataFrame
        class_index = self.schedules[self.schedules['classID'] == class_id].index[0]
        
        # Update the fields if they are provided
        if class_name:
            self.schedules.at[class_index, 'ClassName'] = class_name
        if date:
            self.schedules.at[class_index, 'Date'] = date
        if duration:
            self.schedules.at[class_index, 'Duration'] = duration
        if max_students:
            self.schedules.at[class_index, 'MaxStudents'] = max_students
        if subject:
            self.schedules.at[class_index, 'Subject'] = subject
        
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
        """
        Generate an analysis report for a specific class_id, including:
        - Attendance statistics (average attendance rate, standard deviation)
        - Student marks statistics (average marks, standard deviation)
        
        Args:
            class_id: The ID of the class to analyze
            
        Returns:
            A dictionary containing the analysis results
        """
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
            }
        }
        
        try:
            # Get class name
            class_info = self.schedules[self.schedules['classID'] == class_id]
            if not class_info.empty:
                report['class_name'] = class_info.iloc[0]['ClassName']
            
            # Analyze attendance
            attendance_data = self.attendance[self.attendance['ClassID'] == class_id]
            if not attendance_data.empty:
                # Convert status to numeric (1 for present, 0 for absent)
                attendance_data['numeric_status'] = attendance_data['Status'].apply(
                    lambda x: 1 if x.lower() == 'present' else 0
                )
                
                report['attendance']['count'] = len(attendance_data)
                report['attendance']['present_rate'] = attendance_data['numeric_status'].mean() * 100
                report['attendance']['std_dev'] = attendance_data['numeric_status'].std() * 100
            
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
        
        except Exception as e:
            report['error'] = str(e)
        
        return report

