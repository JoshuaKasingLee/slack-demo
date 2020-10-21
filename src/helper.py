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
