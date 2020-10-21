import pytest
from auth import auth_register
from user import user_profile, user_profile_setname
from other import clear
from error import InputError, AccessError

# assume that u_id has already been checked in user_profile

def test_change_first_name():
    clear()
    user_details = auth_register("frankiefort@gmail.com", "falala", "Frankie", "Fort")
    user_profile_setname(user_details["token"], "Frankenstein", "Fort")
    profile = user_profile(user_details["token"], user_details["u_id"])
    assert(profile["user"]["name_first"] == "Frankenstein")
    assert(profile["user"]["name_last"] == "Fort")
    assert(profile["user"]["handle_str"] == "frankiefort")
    clear()

def test_change_last_name():
    clear()
    user_details = auth_register("frankiefort@gmail.com", "falala", "Frankie", "Fort")
    user_profile_setname(user_details["token"], "Frankie", "Fantastic")
    profile = user_profile(user_details["token"], user_details["u_id"])
    assert(profile["user"]["name_first"] == "Frankie")
    assert(profile["user"]["name_last"] == "Fantastic")
    assert(profile["user"]["handle_str"] == "frankiefort")
    clear()

def test_change_name():
    clear()
    user_details = auth_register("moanadisney@gmail.com", "bluesea", "Moana", "Disney")
    user_profile_setname(user_details["token"], "Cinderella", "Princess")
    profile = user_profile(user_details["token"], user_details["u_id"])
    assert(profile["user"]["name_first"] == "Cinderella")
    assert(profile["user"]["name_last"] == "Princess")
    assert(profile["user"]["handle_str"] == "moanadisney")
    clear()

def test_change_many_names():
    clear()
    user1 = auth_register("cyruschow@gmail.com", "ilikecookies", "Cyrus", "Chow")
    user2 = auth_register("kellyzhou@gmail.com", "pink=bestcolour", "Kelly", "Zhou")
    user3 = auth_register("andreeavissarion@hotmail.com", "coolestshoes!!", "Andreea", "Vissarion")
    user_profile_setname(user1["token"], "Cyrus Yu Seng", "Chow")
    user_profile_setname(user2["token"], "Kel", "Zhou")
    user_profile_setname(user3["token"], "Andreea", "Viss")
    profile1 = user_profile(user1["token"], user1["u_id"])
    profile2 = user_profile(user2["token"], user2["u_id"])
    profile3 = user_profile(user3["token"], user3["u_id"])
    correct_profile1 = {"user": {"u_id" : user1['u_id'], "email" : "cyruschow@gmail.com", \
        "name_first": "Cyrus Yu Seng", "name_last": "Chow", "handle_str": "cyruschow"}}
    correct_profile2 = {"user": {"u_id" : user2['u_id'], "email" : "kellyzhou@gmail.com", \
        "name_first": "Kel", "name_last": "Zhou", "handle_str": "kellyzhou"}}
    correct_profile3 = {"user": {"u_id" : user3['u_id'], "email" : "andreeavissarion@hotmail.com", \
        "name_first": "Andreea", "name_last": "Viss", "handle_str": "andreeavissarion"}}
    assert(profile1 == correct_profile1)
    assert(profile2 == correct_profile2)
    assert(profile3 == correct_profile3)
    clear()

def test_change_short_name_1():
    clear()
    user_details = auth_register("cyruschow@gmail.com", "ilikecookies", "Cyrus", "Chow")
    with pytest.raises(InputError):
        user_profile_setname(user_details["token"], "", "Chow")
    clear()

def test_change_short_name_2():
    clear()
    user_details = auth_register("andreeavissarion@hotmail.com", "coolestshoes!!", "Andreea", "Vissarion")
    with pytest.raises(InputError):
        user_profile_setname(user_details["token"], "Andreea", "")
    clear()   

def test_change_long_name_1():
    clear()
    user_details = auth_register("joshualee@icloud.org", "randypopping", "Josh", "Lee")
    with pytest.raises(InputError):
        user_profile_setname(user_details["token"], "JoshuaJoshuaJoshuaJoshuaJoshuaJoshuaJoshuaJoshuaJoshua", "Lee")
    clear()

def test_change_long_name_2():
    clear()
    user_details = auth_register("nickdodd@gmail.com", "doddthegod", "Nick", "Dodd")
    with pytest.raises(InputError):
        user_profile_setname(user_details["token"], "NicholasIsTheGreatestNicholasIsTheGreatestNicholasIsTheGreatest", "Dodd")
    clear()

def test_change_no_name():
    clear()
    user_details = auth_register("kellyzhou@gmail.com", "pink=bestcolour", "Kelly", "Zhou")
    with pytest.raises(InputError):
        user_profile_setname(user_details["token"], "", "")
    clear()

def test_invalid_token():
    clear()
    auth_register("kellyczhou@gmail.com", "cats<3", "Kelly", "Zhou")
    with pytest.raises(AccessError):
        user_profile_setname('badtoken', "Valid", "Name")
    clear()