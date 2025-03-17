def validate_credentials(school, username, password):
    emp = school.employees[school.employees['username'] == username]
    if not emp.empty and emp['password'].values[0] == password:
        return emp['role'].values[0]
    return None