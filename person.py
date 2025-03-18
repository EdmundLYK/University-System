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

    # change for schedule
    def assign_teacher_to_class(self, class_name, teacher_id):
        self.school.assign_teacher_to_class(class_name, teacher_id)

class Teacher:
    def __init__(self, school, username):
        self.school = school
        self.username = username
        emp = self.school.employees[self.school.employees['username'] == username]
        if not emp.empty:
            self.employee_id = emp['employee_id'].values[0]

    # havent implement
    def mark_attendance(self, class_name, date, student_id, status):
        self.school.mark_attendance(class_name, date, student_id, status, self.employee_id)

    def update_student_mark(self, student_id, mark=None):
        return self.school.update_student(student_id, mark)
    
    def update_teacher(self, name=None, contact=None, username=None, password=None):
        return self.school.update_teacher(self.employee_id, name, contact, username, password)
