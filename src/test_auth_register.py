# tests for auth_register
import pytest
import auth
from auth_register import auth_register
from auth_login import auth_login
#from auth import auth_register, auth_login
from error import InputError

# An email is a string (a subset of ASCII characters) separated into
# two parts by @ symbol, a “personal_info” and a domain, that is
# personal_info@domain.

# TEST INPUT ERRORS

# TEST WHETHER EMAIL IS VALID


#valid normal email
#valid wacky email

# test whether input error is raised when email is invalid

def test_email_invalid():
    with pytest.raises(InputError):
        auth_register("email", "password", "first", "last") # no ampersand or dot
        auth_register("email.com", "password", "first", "last") # no ampersand
        auth_register("email@gmail.organisation", "password", "first", "last") # ending too long
#do these even check all the statements, or returns true after the first statement raises the exception?

# other possible tests
#invalid email: dot before the ampersand?
#invalid email: two dots after the ampersand (not sure what is the domain)
#invalid email: ends with a dot?

# TEST WHETHER EMAIL IS TAKEN
#new email
#already taken email
#new email (but very similar to a taken email)


# test whether input error is raised when password is < 6 characters

def test_password_short():
    with pytest.raises(InputError):
        auth_register("email@gmail.com", "cat", "first", "last")
        auth_register("email@gmail.com", "dog", "first", "last")
        auth_register("email@gmail.com", "short", "first", "last")
        auth_register("email@gmail.com", "a", "first", "last")
# ASSUMES NAMES CAN'T HAVE SYMBOLS AS CHARACTERS

# test whether input error is raised when first name is < 1 character
def test_first_name_short():
    with pytest.raises(InputError):
        auth_register("email@gmail.com", "password", "", "last")

# test whether input error is raised when last name is < 1 character
def test_last_name_short():
    with pytest.raises(InputError):
        auth_register("email@gmail.com", "password", "first", "")

# test whether input error is raised when first name is > 50 characters
def test_first_name_long():
    with pytest.raises(InputError):
        auth_register("email@gmail.com", "password", "extremelylongfirstnamebecauseiamsuperdupertroopercool", "last")
        #auth_register(email@gmail.com, password, ...................................................., last)
        #auth_register(email@gmail.com, password, Adolph Blaine Charles David Earl Frederick Gerald Hubert, last)

# test whether input error is raised when last name is > 50 characters
def test_last_name_long():
    with pytest.raises(InputError):
        auth_register("email@gmail.com", "password", "first", "extremelylonglastnamebecauseiamsuperdupertroopercool")
        auth_register("email@gmail.com", "password", "first", "Wolfeschlegelsteinhausenbergerdorfflongestlastnameever")
        #auth_register(email@gmail.com, password, first, ....................................................)


# TEST OUTPUT ERRORS

# test user handles
# can we even test handles??

# test handles of names that are 20 characters or less
#def test_short():
    #assert(auth_register(abc@domain.com, password, John, Smith) == {'u_id': 1, 'token': 'johnsmith',})
    #assert(auth_register(abc@domain.com, password, JANE, DOE) == {'u_id': 2, 'token': 'janedoe',})
    #assert(auth_register(abc@domain.com, password, !@%^&*, name) == {'u_id': 3, 'token': '!@%^&*name',})

# test handles of names that are over 20 characters
#def test_long():
    #assert(auth_register(abc@domain.com, password, LongFirstName, LongLastName) == {'u_id': 4, 'token': 'longfirstnamelonglast',})
    #assert(auth_register(abc@domain.com, password, JANE, DOE) == {'u_id': 5, 'token': 'janedoe',})
    #assert(auth_register(abc@domain.com, password, !@%^&*, name) == {'u_id': 6, 'token': '!@%^&*name',})

# test modified handles of short names
#def test_mod_short():


#correct concatenation (< 20 characters)
#correct concatenation (> 20 characters)
#correct wacky concatentation
#correct concatenation (produces modified name, as original concatenation has already been taken)
#correct concatenationn (modified name, if several original concatenations have been taken)
#incorrect: concatenation is too long
#incorrect: concatenation already exists
#incorrect: concatenates incorrectly (wrong mix/cut-off)

# do we need to test whether our variable inputs are the right variables (e.g. strings, ints, etc.)

# check whether unique ids are generated
def test_unique_u_id():
    u_id1 = auth_register("sallysmith@gmail.com", "ilikecats", "Sally", "Smith")["u_id"]
    u_id2 = auth_register("bobbybrown@gmail.com", "ilikedogs", "Bobby", "Brown")["u_id"]
    assert(u_id1 != u_id2)

# test whether u_id can log in (check whether the token can log in)
def test_registered_login():
    assert(auth_register("email@gmail.com", "password", "first", "last") == auth_login("email@gmail.com", "password"))

# assume correct number of inputs is given
# assume input types are all correct
# all emails are covered in our regex (is this a reasonable assumption?)
# assume registration will log you in