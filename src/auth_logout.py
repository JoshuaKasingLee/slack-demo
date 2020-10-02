from error import InputError
from auth_register import auth_register
from database import master_users

def auth_logout(token):
    return {
        'is_success': True,
    }