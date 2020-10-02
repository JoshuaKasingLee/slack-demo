import pytest
from auth_login import auth_login
from auth_register import auth_register
from auth_logout import auth_logout
from database import clear
from error import InputError

# Tests a successful log-out
def test_successful_logout():
    auth_register("exampletwo@gmail.com", "password", "John", "Smith")
    user_details = auth_login("exampletwo@gmail.com", "password")
    assert(auth_logout(user_details["token"]) == {"is_success": True})
    clear()

def test_failed_no_token():
    assert(auth_logout("") == {"is_success": False})


def test_failed_bad_taken():
    auth_register("cyrussucks@gmail.com", "password", "John", "Smith")
    auth_login("cyrussucks@gmail.com", "password")
    assert(auth_logout("Bad Token") == {"is_success": False})

def test_bad_order():
    user_details_1 = auth_register("example1@gmail.com", "password", "John", "Smith")
    user_details_3 = auth_register("example3@gmail.com", "password", "John", "Smith")
    user_details_2 = auth_register("example2@gmail.com", "password", "John", "Smith")
    assert(auth_logout(user_details_3["token"]) == {"is_success": True})
    assert(auth_logout(user_details_1["token"]) == {"is_success": True})
    assert(auth_logout(user_details_2["token"]) == {"is_success": True})

def test_logout_twice():
    auth_register("exampl3@gmail.com", "password", "John", "Smith")
    user_details = auth_login("exampl3@gmail.com", "password")
    auth_logout(user_details["token"])
    assert(auth_logout(user_details["token"]) == {"is_success": False})


"""
Assumptions:
You can only log out on people who have already logged in
i.e. only tested for people who have logged in
"""