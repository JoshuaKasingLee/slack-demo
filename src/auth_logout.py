from error import InputError
from auth_register import auth_register
from database import master_users

def auth_logout(token):
    # check to see if token exists
    # if the token is active, log the user out
    for users in master_users:
        if token == users["token"] and users["log"] == True:
            users["log"] = False
            return {
            'is_success': True,
        }
    # else, the token is inactive, return false
    return {
        'is_success': False,
    }