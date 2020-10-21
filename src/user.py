from error import InputError, AccessError
from database import master_users
import re

def user_profile(token, u_id):
    # check if u_id exists in database - if not, return InputError
    user_exists = False
    for user in master_users:
        if u_id == user["u_id"]:
            user_exists = True
            found_user = user
            break
    if user_exists == False:
        raise InputError(f"User with u_id {u_id} is not a valid user")

    # check if input token is valid - if not, return AccessError
    if not (token == found_user["token"] and found_user["log"] == True):
        raise AccessError("Token passed in is not a valid token.")

    # if u_id exists and input token is valid, return as required
    return {
        'user': {
        	'u_id': found_user["u_id"],
        	'email': found_user["email"],
        	'name_first': found_user["name_first"],
        	'name_last': found_user["name_last"],
        	'handle_str': found_user["handle_str"],
        },
    }

def user_profile_setname(token, name_first, name_last):
    # check if input token is valid - if not, return AccessError
    valid_token = False
    for i in range(0, len(master_users)):
        if token == master_users[i]["token"] and master_users[i]["log"] == True:
            valid_token = True
            found_i = i
    if valid_token == False:
        raise AccessError("Token passed in is not a valid token.")

    # if token is valid, check whether first and last names are valid
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(f"Error, first name must be between 1 and 50 characters")
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(f"Error, last name must be between 1 and 50 characters")

    # if names are valid, change name in database
    master_users[found_i]['name_first'] = name_first
    master_users[found_i]['name_last'] = name_last

    return {
    }

def user_profile_setemail(token, email):
    # check if input token is valid - if not, return AccessError
    valid_token = False
    for i in range(0, len(master_users)):
        if token == master_users[i]["token"] and master_users[i]["log"] == True:
            valid_token = True
            found_i = i
    if valid_token == False:
        raise AccessError("Token passed in is not a valid token.")

    # check whether email is valid
    # given regex function from: https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not re.search(regex, email):
        raise InputError(f"Error, {email} is invalid")

    # check whether email address is being used by another user
    for id in master_users:
        if email == id["email"]:
            raise InputError(f"Error, {email} has been taken")
            
    # update email
    master_users[found_i]['email'] = email

    return {
    }

def user_profile_sethandle(token, handle_str):
     # check if input token is valid - if not, return AccessError
    valid_token = False
    for i in range(0, len(master_users)):
        if token == master_users[i]["token"] and master_users[i]["log"] == True:
            valid_token = True
            found_i = i
    if valid_token == False:
        raise AccessError("Token passed in is not a valid token.")

    # check whether handle is too long or short
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError("Handle must be between 3 and 20 characters")

    # check whether handle has been taken
    for id in master_users:
        if handle_str == id["handle_str"]:
            raise InputError(f"Error, {handle_str} handle has been taken")
      
    # update email
    master_users[found_i]['handle_str'] = handle_str

    return {
    }