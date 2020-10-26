import pytest
from auth import auth_register
from user import user_profile, user_profile_sethandle
from other import clear
from error import InputError, AccessError

def test_change_valid_handles():
    clear()
    user_details = auth_register("alphabetnumbers@gmail.com", "123456", "Alphabet", "Numbers")
    user_profile_sethandle(user_details["token"], "numbersalphabet")
    profile = user_profile(user_details["token"], user_details["u_id"])
    assert(profile["user"]["handle_str"] == "numbersalphabet")
    user_profile_sethandle(user_details["token"], "NuMBersAlPhAbeT")
    profile = user_profile(user_details["token"], user_details["u_id"])
    assert(profile["user"]["handle_str"] == "NuMBersAlPhAbeT")
    user_profile_sethandle(user_details["token"], "123456asdfghjkl")
    profile = user_profile(user_details["token"], user_details["u_id"])
    assert(profile["user"]["handle_str"] == "123456asdfghjkl")
    user_profile_sethandle(user_details["token"], "!!  &d# Cn!")
    profile = user_profile(user_details["token"], user_details["u_id"])
    assert(profile["user"]["handle_str"] == "!!  &d# Cn!")
    clear()

def test_change_short_handle():
    clear()
    user_details = auth_register("email@gmail.com", "password", "Jane", "Doe")
    with pytest.raises(InputError):
        user_profile_sethandle(user_details["token"], "ab")
    clear()

def test_change_long_handle():
    clear()
    user_details = auth_register("email@gmail.com", "password", "Jane", "Doe")
    with pytest.raises(InputError):
        user_profile_sethandle(user_details["token"], "janedoeisthebestpersonintheuniverse")
    clear()

def test_change_no_handle():
    clear()
    user_details = auth_register("email@gmail.com", "password", "Jane", "Doe")
    with pytest.raises(InputError):
        user_profile_sethandle(user_details["token"], "")
    clear()

def test_change_handle_taken():
    clear()
    auth_register("kellyzhou@gmail.com", "password", "Kelly", "Zhou")
    user2 = auth_register("joshualee@gmail.com", "password", "Joshua", "Lee")
    with pytest.raises(InputError):
        user_profile_sethandle(user2["token"], "kellyzhou")
    clear()

def test_invalid_token():
    clear()
    auth_register("kellyzhou@gmail.com", "cats<3", "Kelly", "Zhou")
    with pytest.raises(AccessError):
        user_profile_sethandle('badtoken', "validhandle")
    clear()
