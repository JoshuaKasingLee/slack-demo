# since no function returns reset_code, we cannot test whether the
# correct code has been given
# hence, these tests only test for the validity of the new password

import pytest
from auth import auth_register, auth_login, auth_logout, auth_passwordreset_reset
from user import user_profile
from other import clear
from error import InputError
import database

# we are using a helper function auth_passwordreset_return to test
# this function acts the same as auth_passwordreset_request, but instead
# of emailing the reset code, the reset code is returned instead

# test whether input error is raised when password is < 6 characters
def test_password_short_1():
    clear()
    user = auth_register("cyruschow@gmail.com", "ilikecookies", "Cyrus", "Chow")
    profile = user_profile(user['token'], user['u_id'])
    auth_logout(user['token'])
    code = database.auth_passwordreset_return(profile['user']['email'])
    with pytest.raises(InputError):
        auth_passwordreset_reset(code, "123")
    clear()

def test_password_short_2():
    clear()
    user = auth_register("joshualee@icloud.org", "randypopping", "Josh", "Lee")
    profile = user_profile(user['token'], user['u_id'])
    auth_logout(user['token'])
    code = database.auth_passwordreset_return(profile['user']['email'])
    with pytest.raises(InputError):
        auth_passwordreset_reset(code, "short")
    clear()

def test_password_short_3():
    clear()
    user = auth_register("nickdodd@gmail.com", "doddthegod", "Nick", "Dodd")
    profile = user_profile(user['token'], user['u_id'])
    auth_logout(user['token'])
    code = database.auth_passwordreset_return(profile['user']['email'])
    with pytest.raises(InputError):
        auth_passwordreset_reset(code, "")
    clear()

def test_password_reset_success():
    clear()
    user = auth_register("cyruschow@gmail.com", "ilikecookies", "Cyrus", "Chow")
    profile = user_profile(user['token'], user['u_id'])
    auth_logout(user['token'])
    code = database.auth_passwordreset_return(profile['user']['email'])
    auth_passwordreset_reset(code, "password123")
    auth_login("cyruschow@gmail.com", "password123")
    #profile = user_profile(user['token'], user['u_id'])
    #assert(profile['user']['password'] == 'password123')
    clear()
    
def test_multiple_reset_success():
    clear()
    # register users
    user1 = auth_register("sallysmith@gmail.com", "ilikecats", "Sally", "Smith")
    user2 = auth_register("bobbybrown@gmail.com", "ilikedogs", "Bobby", "Brown")
    user3 = auth_register("janedoe@gmail.com", "plainjane", "Jane", "Doe")
    # change password
    profile3 = user_profile(user3['token'], user3['u_id'])
    auth_logout(user3['token'])
    code3 = database.auth_passwordreset_return(profile3['user']['email'])
    auth_passwordreset_reset(code3, "imcool")
    auth_login("janedoe@gmail.com", "imcool")
    # with logout
    profile1 = user_profile(user1['token'], user1['u_id'])
    auth_logout(user1['token'])
    code1 = database.auth_passwordreset_return(profile1['user']['email'])
    auth_passwordreset_reset(code1, "password123")
    auth_login("sallysmith@gmail.com", "password123")
    # without logout
    profile2 = user_profile(user2['token'], user2['u_id'])
    code2 = database.auth_passwordreset_return(profile2['user']['email'])
    auth_passwordreset_reset(code2, "bobbyis thebest!")
    auth_login("bobbybrown@gmail.com", "bobbyis thebest!")
    # update password again
    code2 = database.auth_passwordreset_return(profile2['user']['email'])
    auth_passwordreset_reset(code2, "bobbyis thebestest!")
    auth_login("bobbybrown@gmail.com", "bobbyis thebestest!")
    clear()

def test_reset_correct_password():
    clear()
    user1 = auth_register("sallysmith@gmail.com", "ilikecats", "Sally", "Smith")
    user2 = auth_register("bobbybrown@gmail.com", "ilikedogs", "Bobby", "Brown")
    profile1 = user_profile(user1['token'], user1['u_id'])
    auth_logout(user1['token'])
    code1 = database.auth_passwordreset_return(profile1['user']['email'])
    auth_passwordreset_reset(code1, "password123")
    auth_login("sallysmith@gmail.com", "password123")
    with pytest.raises(InputError):
        auth_login("bobbybrown@gmail.com", "password123")
    clear()