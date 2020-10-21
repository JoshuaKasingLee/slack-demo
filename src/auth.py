import re
from error import InputError
import database

def auth_login(email, password):

    validate_email(email)
    database.auth_check_email_login(email)
    return database.auth_check_password(email, password)


def auth_logout(token):

    return database.auth_logout_user(token)


def auth_register(email, password, name_first, name_last):

    validate_email(email)
    database.auth_check_email_register(email)

    # check whether password is 6 characters or greater
    if len(password) < 6:
        raise InputError(f"Error, password must be >= 6 characters")

    # check whether first and last name meet character requirements
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(f"Error, first name must be between 1 and 50 characters")
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(f"Error, last name must be between 1 and 50 characters")

    # assign u_id in chronological order of registration
    id = database.auth_assign_id()

    # for iteration 1, let the token be the u_id
    token = str(id)
    
    # create user handle
    handle = name_first + name_last
    handle = handle.lower()
    if len(handle) > 20:
        handle = handle[:20]

    handle = database.auth_assign_user_handle(handle)
    
    # create a master user profile by filling in relevant fields
    master_user = {}
    master_user['u_id'] = id
    master_user['email'] = email
    master_user['name_first'] = name_first
    master_user['name_last'] = name_last
    master_user['password'] = password
    master_user['token'] = token
    master_user['handle_str'] = handle
    master_user['log'] = True # assume that user is logged in after registering
    
    # add new user to the master_users database
    database.auth_add_user(master_user)

    return {
        'u_id': id,
        'token': str(id),
    }

# NON-DATABASE HELPER FUNCTIONS #

def validate_email(email):
    '''check valid email, regex function from: https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/'''
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not re.search(regex, email):
        raise InputError(f"Error, {email} is invalid")
