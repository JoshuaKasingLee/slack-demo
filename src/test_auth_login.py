import pytest
from auth_login import auth_login
from auth_register import auth_register
from other import clear
from error import InputError

# Testing an undefined user
def test_invalid_user():
    with pytest.raises(InputError):
        auth_login("randomemail@gmail.com", "12345")

# Testing an invalid email #1
def test_invalid_email_1():
    with pytest.raises(InputError):
        auth_login("testing@testing@unsw.edu.au", "12345")

# Testing an invalid email #2
def test_invalid_email_2():
    with pytest.raises(InputError):
        auth_login("testing@testing@unsw.edu.au", "12345")

# Testing invalid password
def test_invalid_password():
    auth_register("example@gmail.com", "password", "John", "Smith")
    with pytest.raises(InputError):
        auth_login("example@gmail.com", "wrongpassword")

# Testing successful login attempt !!
def test_login_success():
    auth_register("testmail@gmail.com", "123456", "John", "Smith")
    auth_login("testmail@gmail.com", "123456")

# # Testing double login !! (Not in the assignment spec)
# def test_login_twice():
#     auth_register("example@gmail.com", "password", "John", "Smith")
#     auth_login("example@gmail.com", "password")
#     with pytest.raises(InputError):
#         auth_login("example@gmail.com", "password")