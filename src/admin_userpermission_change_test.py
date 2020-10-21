import pytest
from other import admin_userpermission_change, clear
import channel
import channels
import auth
from error import InputError, AccessError

def test_not_admin() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    user_2 = auth.auth_register("sallychampion@gmail.com", "password", "Sally", "Champion")
    token_2 = user_2['token']
    channel_id = channels.channels_create(token, "Channel1", False)["channel_id"]
    with pytest.raises(AccessError):
        channel.channel_join(token_2, channel_id)
    clear()

def test_make_admin() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    user_2 = auth.auth_register("sallychampion@gmail.com", "password", "Sally", "Champion")
    u_id_2 = user_2['u_id']
    token_2 = user_2['token']
    admin_userpermission_change(token, u_id_2, 1)
    channel_id = channels.channels_create(token, "Channel1", False)["channel_id"]
    assert(channel.channel_join(token_2, channel_id))
    clear()

def test_remove_admin() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    user_2 = auth.auth_register("sallychampion@gmail.com", "password", "Sally", "Champion")
    u_id_2 = user_2['u_id']
    token_2 = user_2['token']
    admin_userpermission_change(token, u_id_2, 1)
    admin_userpermission_change(token, u_id_2, 2)
    channel_id = channels.channels_create(token, "Channel1", False)["channel_id"]
    with pytest.raises(AccessError):
        channel.channel_join(token_2, channel_id)
    clear()

def test_invalid_permission_id() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    user_2 = auth.auth_register("sallychampion@gmail.com", "password", "Sally", "Champion")
    u_id_2 = user_2['u_id']
    with pytest.raises(InputError):
        admin_userpermission_change(token, u_id_2, 4)
    clear()
    
def test_invalid_u_id() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    auth.auth_register("sallychampion@gmail.com", "password", "Sally", "Champion")
    with pytest.raises(InputError):
        admin_userpermission_change(token, 100, 1)
    clear()

def test_not_admin_not_owner() :
    clear()
    auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    user_2 = auth.auth_register("sallychampion@gmail.com", "password", "Sally", "Champion")
    token_2 = user_2['token']
    user_3 = auth.auth_register("jane@gmail.com", "password", "Jane", "Doe")
    u_id_3 = user_3['u_id']
    with pytest.raises(AccessError):
        admin_userpermission_change(token_2, u_id_3, 1)
    clear()

def test_admin_but_not_owner() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    user_2 = auth.auth_register("sallychampion@gmail.com", "password", "Sally", "Champion")
    u_id_2 = user_2['u_id']
    token_2 = user_2['token']
    admin_userpermission_change(token, u_id_2, 1)
    user_3 = auth.auth_register("jane@gmail.com", "password", "Jane", "Doe")
    u_id_3 = user_3['u_id']
    with pytest.raises(AccessError):
        admin_userpermission_change(token_2, u_id_3, 1)
    clear()
