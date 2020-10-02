import pytest
from auth_login import auth_login
from auth_register import auth_register
from auth_logout import auth_logout
from database import clear
from error import InputError

# Tests a successful log-out
def test_successful_logout():
    auth_register("example@gmail.com", "password", "John", "Smith")
    user_details = auth_login("example@gmail.com", "password")
    assert(auth_logout(user_details["token"]) == True)

def test_failed_no_token():
    assert(auth_logout("") == False)


def test_failed_bad_taken():
    auth_register("cyrussucks@gmail.com", "password", "John", "Smith")
    auth_login("cyrussucks@gmail.com", "password")
    assert(auth_logout("Bad Token") == False)

def test_bad_order():
    user_details_1 = auth_register("example1@gmail.com", "password", "John", "Smith")
    user_details_3 = auth_register("example3@gmail.com", "password", "John", "Smith")
    user_details_2 = auth_register("example2@gmail.com", "password", "John", "Smith")
    assert(auth_logout(user_details_3["token"]) == True)
    assert(auth_logout(user_details_1["token"]) == True)
    assert(auth_logout(user_details_2["token"]) == True)

def test_logout_twice():
    auth_register("example@gmail.com", "password", "John", "Smith")
    user_details = auth_login("example@gmail.com", "password")
    auth_logout(user_details["token"])
    assert(auth_logout(user_details["token"]) == False)


"""
Assumptions:
You can only log out on people who have already logged in
i.e. only tested for people who have logged in
"""