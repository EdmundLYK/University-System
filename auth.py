def validate_credentials(school, username, password):
    user = school.users[school.users['username'] == username]
    if not user.empty and user['password'].values[0] == password:
        return user['role'].values[0]
    return None