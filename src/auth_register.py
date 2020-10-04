import re
from error import InputError
from database import master_users


def auth_register(email, password, name_first, name_last):

    # check whether email is valid
    # given regex function from: https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not re.search(regex, email):
        raise InputError(f"Error, {email} is invalid")

    # check whether email address is being used by another user
    for id in master_users:
        if email == id["email"]:
            raise InputError(f"Error, {email} has been taken")

    # check whether password is 6 characters or greater
    if len(password) < 6:
        raise InputError(f"Error, password must be >= 6 characters")

    # check whether first and last name meet character requirements
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(f"Error, first name must be between 1 and 50 characters")
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(f"Error, last name must be between 1 and 50 characters")

    # assign u_id in chronological order of registration
    id = len(master_users)

    # for iteration 1, let the token be the u_id
    token = str(id)
    
    # create user handle
    handle = name_first + name_last
    handle.lower()
    if len(handle) > 20:
        handle = handle[:20]

    # create variables that allow us to manipulate the handle string
    handle_list = list(handle)
    i = 1

    # loop to ensure new user handle is new
    for users in master_users:
        # if new user handle exists, tweak it
        if handle == users['handle']:
            if i < 10:
                handle_list[-1] = str(i)
                handle = "".join(handle_list)
                i = i + 1
            elif i < 100:
                handle_list[-2] = str(i)[0]
                handle_list[-1] = str(i)[1]
                handle = "".join(handle_list)
                i = i + 1
    
    # create a master user profile by filling in relevant fields
    master_user = {}
    master_user['u_id'] = id
    master_user['email'] = email
    master_user['name_first'] = name_first
    master_user['name_last'] = name_last
    master_user['password'] = password
    master_user['token'] = token
    master_user['handle'] = handle
    master_user['log'] = True # assume that user is logged in after registering
    
    # add new user to the master_users database
    master_users.append(master_user)

    return {
        'u_id': id,
        'token': str(id),
    }
