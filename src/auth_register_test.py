import pytest
from auth import auth_login, auth_logout, auth_register
from other import clear
from error import InputError

# 1. TEST INPUT ERRORS

# test whether input error is raised when email is invalid
# assume regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
def test_email_invalid_1():
    with pytest.raises(InputError):
        auth_register("email", "password", "first", "last") # no ampersand or dot
def test_email_invalid_2():
    with pytest.raises(InputError):
        auth_register("email.com", "password", "first", "last") # no ampersand
def test_email_invalid_3():
    with pytest.raises(InputError):
        auth_register("email@gmail.organisation", "password", "first", "last") # ending too long
def test_email_invalid_4():
    with pytest.raises(InputError):
        auth_register("email@gmail@organisation.com", "password", "first", "last") # two ampersands
def test_email_invalid_5():
    with pytest.raises(InputError):
        auth_register("email@gmail.com.org", "password", "first", "last") # two dots after ampersand
def test_email_invalid_6():
    with pytest.raises(InputError):
        auth_register("EMAIL@GMAIL.COM", "password", "first", "last") # capitals

# test whether input error is thrown when registering with an already registered email
def test_email_taken_1():
    auth_register("icecreamisyummy@gmail.com", "frozen", "Ice", "Cream")
    with pytest.raises(InputError):
        auth_register("icecreamisyummy@gmail.com", "milkduds", "Icy", "Poles")
    clear()
def test_email_taken_2():
    result = auth_register("ilikesummer@gmail.com", "bestseason", "Summer", "Days")
    assert(auth_logout(result["token"]) == {"is_success": True})
    with pytest.raises(InputError):
        auth_register("ilikesummer@gmail.com", "bestseason", "Summer", "Days")
    clear()

# test whether input error is raised when password is < 6 characters
def test_password_short_1():
    with pytest.raises(InputError):
        auth_register("email@gmail.com", "cat", "first", "last")
def test_password_short_2():
    with pytest.raises(InputError):
        auth_register("email@gmail.com", "short", "first", "last")
def test_password_short_3():
    with pytest.raises(InputError):
        auth_register("email@gmail.com", "a", "first", "last")

# test whether input error is raised when first name is < 1 character
def test_first_name_short():
    with pytest.raises(InputError):
        auth_register("email@gmail.com", "password", "", "last")

# test whether input error is raised when last name is < 1 character
def test_last_name_short():
    with pytest.raises(InputError):
        auth_register("email@gmail.com", "password", "first", "")

# test whether input error is raised when first name is > 50 characters
def test_first_name_long_1(): # very long name
    with pytest.raises(InputError):
        auth_register("email@gmail.com", "password", "extremelylongfirstnamebecauseiamsuperdupertroopercool", "last")
def test_first_name_long_2(): # only characters
    with pytest.raises(InputError):
        auth_register("email@gmail.com", "password", ".....................................................", "last")
def test_first_name_long_3(): # name with spaces
    with pytest.raises(InputError):
        auth_register("email@gmail.com", "password", "Adolph Blaine Charles David Earl Frederick Gerald Hubert", "last")

# test whether input error is raised when last name is > 50 characters
def test_last_name_long():
    with pytest.raises(InputError):
        auth_register("email@gmail.com", "password", "first", "extremelylonglastnamebecauseiamsuperdupertroopercool")


# 2. TEST OUTPUT

# test valid registrations are successful
def test_valid_rego():
    auth_register("cyruschow@gmail.com", "ilikecookies", "Cyrus", "Chow")
    auth_register("kellyzhou@gmail.com", "pink=bestcolour", "Kelly", "Zhou")
    auth_register("andreeavissarion@hotmail.com", "coolestshoes!!", "Andreea", "Vissarion")
    auth_register("joshualee@icloud.org", "randypopping", "Josh", "Lee")
    auth_register("nickdodd@gmail.com", "doddthegod", "Nick", "Dodd")
    clear()

# test whether unique ids are generated
def test_unique_u_id():
    u_id1 = auth_register("sallysmith@gmail.com", "ilikecats", "Sally", "Smith")["u_id"]
    u_id2 = auth_register("bobbybrown@gmail.com", "ilikedogs", "Bobby", "Brown")["u_id"]
    u_id3 = auth_register("janedoe@gmail.com", "plainjane", "Jane", "Doe")["u_id"]
    assert(u_id1 != u_id2)
    assert(u_id1 != u_id3)
    assert(u_id2 != u_id3)
    clear()

# test whether registered user can log in and logout
def test_registered_login():
    auth_register("email@gmail.com", "password", "first", "last")
    result = auth_login("email@gmail.com", "password")
    assert(auth_logout(result["token"]) == {"is_success": True})
    clear()


# we cannot blackbox test generated handles in this iteration since the "user.py" file has not been implemented
# however, once user.py is implemented, tests similar to below can be created:
# correct concatenation (< 20 characters)
# correct concatenation (> 20 characters)
# correct concatenation (produces modified name, as original concatenation has already been taken)
# correct concatenationn (modified name, if several original concatenations have been taken)
# incorrect: concatenation is too long
# incorrect: concatenation already exists
# incorrect: concatenates incorrectly (wrong mix/cut-off)