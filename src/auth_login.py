import re
from error import InputError
from database import master_users

def auth_login(email, password):
    
    # check whether email is valid
    # given regex function from: https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not re.search(regex, email):
        raise InputError(f"Error, {email} is invalid")

    # check if a user is already logged on

    # 





    return {
        'u_id': 1,
        'token': '12345',
    }