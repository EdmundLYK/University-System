class Admin:
    def __init__(self, school, username):
        self.school = school
        self.username = username
        emp = self.school.employees[self.school.employees['username'] == username]
        if not emp.empty:
            self.employee_id = emp['employee_id'].values[0]

    def add_employee(self, name, contact, position, username=None, password=None):
        return self.school.add_employee(name, contact, position, username, password)

    def remove_employee(self, employee_id):
        self.school.remove_employee(employee_id)
    
    def update_employee(self, employee_id, name=None, contact=None, position=None, username=None, password=None):
        return self.school.update_employee(employee_id, name, contact, position, username, password)

    def add_student(self, name, age, class_id):
        return self.school.add_student(name, age, class_id)
    
    def remove_student(self, name):
        self.school.remove_student(name)

    def update_student(self, student_id, name=None, age=None, class_id=None, mark=None):
        return self.school.update_student(student_id, name, age, class_id, mark)

    def assign_teacher_to_class(self, class_id, teacher_id):
        self.school.assign_teacher_to_class( class_id, teacher_id)
    
    def analysis_report(self, class_id):
        return self.school.analysis_report(class_id)

class Teacher:
    def __init__(self, school, username):
        self.school = school
        self.username = username
        emp = self.school.employees[self.school.employees['username'] == username]
        if not emp.empty:
            self.employee_id = emp['employee_id'].values[0]

    def mark_attendance(self, class_id, student_id, date, status):
        self.school.mark_attendance(class_id, student_id, date, status)

    def update_attendance(self, attendance_id, class_id, student_id, date, status):
        return self.school.update_student(self, attendance_id, class_id, student_id, date, status)

    def update_student_mark(self, student_id, mark=None):
        return self.school.update_student(student_id=student_id, name=None, age=None, class_id=None, mark=mark)
    
    def update_teacher(self, name=None, contact=None, username=None, password=None):
        return self.school.update_teacher(self.employee_id, name, contact, username, password)
    
    def update_class_details(self, class_id, teacher_id, class_name, date, duration, max_students, subject):
        return self.school.update_class_details( class_id, teacher_id, class_name, date, duration, max_students, subject)

    def add_lesson_plan(self, teacher_id, class_id, subject, lesson_details, date, learning_objectives, assessment):
        return self.school.add_lesson_plan( teacher_id, class_id, subject, lesson_details, date, learning_objectives, assessment)
    
    def update_lesson_plans(self, lesson_id, teacher_id, class_id, subject, lesson_details, date, learning_objectives, assessment):
        return self.school.add_lesson_plan(lesson_id, teacher_id, class_id, subject, lesson_details, date, learning_objectives, assessment)
    
    def attendance_report(self, class_id, date):
        return self.school.attendance_report(class_id, date)
    
    def analysis_report(self, class_id):
        return self.school.analysis_report(class_id)

    # implement delete function for all
    # implement delete function for all
    # implement delete function for all
    # implement delete function for all
    # implement delete function for all