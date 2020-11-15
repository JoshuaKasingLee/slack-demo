from error import InputError
import database
import hashlib
import jwt
import helper


# auth functions

def auth_login(email, password):
    helper.validate_email(email)
    database.auth_check_email_login(email)
    return database.auth_check_password(email, password)


def auth_logout(token):
    return database.auth_logout_user(token)


def auth_register(email, password, name_first, name_last):
    helper.validate_email(email)
    database.auth_check_email_register(email)

    # check whether password is 6 characters or greater
    helper.check_password_length(password)

    # check whether first and last name meet character requirements
    helper.check_name_length(name_first, name_last)

    # assign u_id in chronological order of registration
    id = database.auth_assign_id()

    # let the token be an encoded u_id dictionary
    token = jwt.encode({"u_id": id}, database.SECRET, algorithm='HS256').decode('utf-8')
    
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
    master_user['password'] = hashlib.sha256(password.encode()).hexdigest()
    master_user['token'] = token
    master_user['handle_str'] = handle
    master_user['log'] = True # assume that user is logged in after registering
    
    # add new user to the master_users database
    database.add_blocklist(id)
    database.auth_add_user(master_user)

    return {
        'u_id': id,
        'token': token,
    }
