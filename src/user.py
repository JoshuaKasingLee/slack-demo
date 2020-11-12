from error import InputError, AccessError
import database
import re
import helper

def user_profile(token, u_id):
    # check if u_id exists in database - if not, return InputError
    found_user = database.check_token_u_id_match(token, u_id)
    # if u_id exists and input token is valid, return as required
    return {
        'user': {
        	'u_id': found_user["u_id"],
        	'email': found_user["email"],
        	'name_first': found_user["name_first"],
        	'name_last': found_user["name_last"],
        	'handle_str': found_user["handle_str"]
        }
    }

def user_profile_setname(token, name_first, name_last):
    # check if input token and name lengths are valid
    id = database.return_token_u_id(token)
    helper.check_name_length(name_first, name_last)

    # if names are valid, change name in database
    database.update_first_name(id, name_first)
    database.update_last_name(id, name_last)
    return {
    }

def user_profile_setemail(token, email):
    # check if input token and email is valid
    id = database.return_token_u_id(token)
    helper.validate_email(email)
    database.auth_check_email_register(email)  

    # update email
    database.update_email(id, email)
    return {
    }

def user_profile_sethandle(token, handle_str):
     # check if input token is valid - if not, return AccessError
    id = database.return_token_u_id(token)

    # check whether handle is too long or short
    helper.check_handle_length(handle_str)
    
    # check whether handle has been taken
    database.check_handle(handle_str)

    # update handle
    database.update_handle(id, handle_str)

    return {
    }