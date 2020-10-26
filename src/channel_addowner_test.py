import pytest
from other import clear
from channel import channel_addowner, channel_join, channel_details
import channels
import auth
from error import InputError
from error import AccessError

def test_valid_channel():
    clear()
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    u_id = user['u_id']
    token = user['token']
    channel_id = 999
    with pytest.raises(InputError):
        channel_addowner(token, channel_id, u_id)
    clear()
 
def test_already_channel_owner():
    clear()
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    u_id = user['u_id']
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)['channel_id']
    with pytest.raises(InputError):
        channel_addowner(token, channel_id, u_id)
    clear()
 
def test_not_global_or_local_owner():
    clear()
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    token = user['token']
    user_2 = auth.auth_register("email2@gmail.com", "password", "John", "Smith")
    u_id_2 = user_2['u_id']
    token_2 = user_2['token']  
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    with pytest.raises(AccessError):
        channel_addowner(token_2, channel_id, u_id_2)
    clear() 
 
def test_global_but_not_local_owner():
    clear()
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    u_id = user['u_id']
    token = user['token']
    user_2 = auth.auth_register("email2@gmail.com", "password", "John", "Smith")
    token_2 = user_2['token']    
    channel_id = channels.channels_create(token_2, "Channel1", True)["channel_id"]
    channel_addowner(token, channel_id, u_id)
    owner_members  = channel_details(token, channel_id)["owner_members"]
    is_in = 0
    for member in owner_members:
        if member['u_id'] == u_id:
            is_in = 1
    assert (is_in == 1)
    clear()   
 
def test_promote():
    clear()
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    token = user['token']
    user_2 = auth.auth_register("email2@gmail.com", "password", "John", "Smith")
    u_id_2 = user_2['u_id']
    token_2 = user_2['token']  
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    channel_join(token_2, channel_id)
    channel_addowner(token, channel_id, u_id_2)
    owner_members = channel_details(token, channel_id)["owner_members"]
    is_in = 0
    for member in owner_members:
        if member['u_id'] == u_id_2:
            is_in = 1
    assert (is_in == 1)
    clear()

