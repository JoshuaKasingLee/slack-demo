import re
from error import InputError
from auth_register import auth_register
from database import master_users

def auth_login(email, password):
    
    # check whether email is valid
    # given regex function from: https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not re.search(regex, email):
        raise InputError(f"Error, {email} is invalid")

    # check if a user is already logged on
    # for id in master_users:
    #     if id["log"] == True:
    #         # Loggin in when another user is logged in should raise an input error as follows
    #         raise InputError(f"Error, a user is already logged in")

    # check whether email address is in the database and check if the password is correct
    if len(master_users) == 0:
        raise InputError(f"Error, {email} has not been registered")
    exists = False
    for user in master_users:
        if email == user["email"]:
            exists = True
    if exists == False:
        raise InputError(f"Error, {email} has not been registered")

    # check if password is wrong and raise error
    for user in master_users:
        if email == user["email"]:
            if password != user["password"]:
                raise InputError(f"Error, the password is incorrect")
                
            else:
                id = user["u_id"]
                tok = user["token"]
                user["log"] = True
    return {
        'u_id': id,
        'token': tok,
    }