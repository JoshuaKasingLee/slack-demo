import pytest
from auth import auth_register
from user import user_profile, user_profile_setemail
from other import clear
from error import InputError, AccessError

def test_change_valid_email():
    clear()
    user_details = auth_register("alphabetnumbers@gmail.com", "123456", "Alphabet", "Numbers")
    user_profile_setemail(user_details["token"], "numbersalphabet@gmail.com")
    profile = user_profile(user_details["token"], user_details["u_id"])
    assert(profile["user"]["email"] == "numbersalphabet@gmail.com")
    assert(profile["user"]["name_first"] == "Alphabet")
    assert(profile["user"]["handle_str"] == "alphabetnumbers")
    clear()

def test_change_multiple_emails():
    clear()
    user_details = auth_register("alphabetnumbers@gmail.com", "123456", "Alphabet", "Numbers")
    user_profile_setemail(user_details["token"], "numbersalphabet@gmail.com")
    user_profile_setemail(user_details["token"], "imsuperfunny@gmail.com")
    user_profile_setemail(user_details["token"], "waitimmachangethisagain@gmail.com")
    user_profile_setemail(user_details["token"], "last1iswear@gmail.com")
    profile = user_profile(user_details["token"], user_details["u_id"])
    assert(profile["user"]["email"] == "last1iswear@gmail.com")
    clear()

def test_invalid_regex_email_1():
    clear()
    user_details = auth_register("example@gmail.com", "password", "First", "Last")
    with pytest.raises(InputError):
        user_profile_setemail(user_details["token"], "examplegmail.com")
    clear()

def test_invalid_regex_email_2():
    clear()
    user_details = auth_register("example@gmail.com", "password", "First", "Last")
    with pytest.raises(InputError):
        user_profile_setemail(user_details["token"], "e@gmail.community")
    clear()

def test_invalid_regex_email_3():
    clear()
    user_details = auth_register("example@gmail.com", "password", "First", "Last")
    with pytest.raises(InputError):
        user_profile_setemail(user_details["token"], "e@m@gmail.com")
    clear()

def test_no_email():
    clear()
    user_details = auth_register("example@gmail.com", "password", "First", "Last")
    with pytest.raises(InputError):
        user_profile_setemail(user_details["token"], "")
    clear()

def test_taken_email():
    clear()
    auth_register("kellyzhou@gmail.com", "password", "Kelly", "Zhou")
    user2 = auth_register("joshualee@gmail.com", "password", "Joshua", "Lee")
    with pytest.raises(InputError):
        user_profile_setemail(user2["token"], "kellyzhou@gmail.com")
    clear()

def test_invalid_token():
    clear()
    auth_register("kellyzhou@gmail.com", "cats<3", "Kelly", "Zhou")
    with pytest.raises(AccessError):
        user_profile_setemail('badtoken', "validemail@gmailcom")
    clear()

