from error import InputError, AccessError
#from database import master_users
import database
import re
import helper

def user_profile(token, u_id):
    # check if u_id exists in database - if not, return InputError
    found_user = database.token_u_id_check(token, u_id)

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
    id = database.token_check_return(token)

    # if token is valid, check whether first and last names are valid
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(f"Error, first name must be between 1 and 50 characters")
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(f"Error, last name must be between 1 and 50 characters")

    # if names are valid, change name in database
    database.update_first_name(id, name_first)
    database.update_last_name(id, name_last)

    return {
    }

def user_profile_setemail(token, email):
    # check if input token is valid - if not, return AccessError
    id = database.token_check_return(token)

    # check whether email is valid
    helper.validate_email(email)

    # check whether email address is being used by another user
    database.auth_check_email_register(email)  

    # update email
    database.update_email(id, email)

    return {
    }

def user_profile_sethandle(token, handle_str):
     # check if input token is valid - if not, return AccessError
    # valid_token = False
    # for i in range(0, len(master_users)):
    #     if token == master_users[i]["token"] and master_users[i]["log"] == True:
    #         valid_token = True
    #         found_i = i
    # if valid_token == False:
    #     raise AccessError("Token passed in is not a valid token.")
    id = database.token_check_return(token)

    # check whether handle is too long or short
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError("Handle must be between 3 and 20 characters")

    # check whether handle has been taken
    # for user in master_users:
    #     if handle_str == user["handle_str"]:
    #         raise InputError(f"Error, {handle_str} handle has been taken")
    database.check_handle(handle_str)

    # update email
    #master_users[found_i]['handle_str'] = handle_str
    database.update_handle(id, handle_str)

    return {
    }