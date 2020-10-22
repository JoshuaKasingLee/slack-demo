import re
from error import InputError, AccessError
import jwt
import database

# NON-DATABASE HELPER FUNCTIONS #

def validate_email(email):
    '''check valid email, regex function from: https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/'''
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not re.search(regex, email):
        raise InputError(f"Error, {email} is invalid")

def check_password_length(password):
    if len(password) < 6:
        raise InputError(f"Error, password must be >= 6 characters")

def check_name_length(name_first, name_last):
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(f"Error, first name must be between 1 and 50 characters")
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(f"Error, last name must be between 1 and 50 characters")

def check_handle_length(handle_str):
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError("Handle must be between 3 and 20 characters")