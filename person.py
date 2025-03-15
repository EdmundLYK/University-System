class Admin:
    def __init__(self, school, username):
        self.school = school
        self.username = username
        # Find employee_id based on username (assuming unique names for simplicity)
        user = self.school.users[self.school.users['username'] == username]
        if not user.empty:
            role = user['role'].values[0]
            emp = self.school.employees[self.school.employees['position'] == role]
            if not emp.empty:
                self.employee_id = emp['employee_id'].values[0]

    def add_employee(self, name, contact, position, username=None, password=None):
        return self.school.add_employee(name, contact, position, username, password)

    def remove_employee(self, employee_id):
        self.school.remove_employee(employee_id)

    def add_student(self, name, class_name):
        self.school.add_student(name, class_name)

    def assign_teacher_to_class(self, class_name, teacher_id):
        self.school.assign_teacher_to_class(class_name, teacher_id)

class Teacher:
    def __init__(self, school, username):
        self.school = school
        self.username = username
        # Find employee_id based on username
        user = self.school.users[self.school.users['username'] == username]
        if not user.empty:
            role = user['role'].values[0]
            emp = self.school.employees[self.school.employees['position'] == role]
            if not emp.empty:
                self.employee_id = emp['employee_id'].values[0]

    def mark_attendance(self, class_name, date, student_id, status):
        self.school.mark_attendance(class_name, date, student_id, status, self.employee_id)