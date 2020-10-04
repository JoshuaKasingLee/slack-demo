import pytest
from other import clear
from channel_addowner import channel_addowner
from channel_removeowner import channel_removeowner
from channel_details import channel_details
from channel_join import channel_join
import channels
import auth
from error import InputError, AccessError

#need to test a few things: 
# valid channel (input error), u_id is not an owner (input error).
# access error if token is not global owner OR owner of channel
# regular testing: token is owner and u_id is owner

def test_valid_channel() :
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    u_id = user['u_id']
    token = user['token']
    channel_id = 999
    with pytest.raises(InputError) as e:
        channel_removeowner(token, channel_id, u_id)
    clear()
 
def test_uid_not_channel_owner() :
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    u_id = user['u_id']
    token = user['token']
    user_2 = auth.auth_register("email2@gmail.com", "password", "John", "Smith")
    u_id_2 = user_2['u_id']
    token_2 = user_2['token'] 
    channel_id = channels.channels_create(token, "Channel1", True)
    with pytest.raises(InputError) as e:
        channel_removeowner(token, channel_id, u_id_2)
    clear()
 
def test_not_global_or_local_owner() :
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    u_id = user['u_id']
    token = user['token']
    user_2 = auth.auth_register("email2@gmail.com", "password", "John", "Smith")
    u_id_2 = user_2['u_id']
    token_2 = user_2['token']   
    channel_id = channels.channels_create(token, "Channel1", True)
    with pytest.raises(AccessError) as e:
        channel_removeowner(token_2, channel_id, u_id)
    clear()   
 
def test_global_but_not_local_owner() :
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    u_id = user['u_id']
    token = user['token']
    user_2 = auth.auth_register("email2@gmail.com", "password", "John", "Smith")
    u_id_2 = user_2['u_id']
    token_2 = user_2['token']   
    channel_id = channels.channels_create(token_2, "Channel1", True)
    channel_removeowner(token, channel_id, u_id_2)
    (name, owner_members, all_members)  = channel_details(token, channel_id)
    is_in_owner = 0
    for member in owner_members:
        if member['u_id'] == u_id_2:
            is_in_owner = 1
    assert (is_in_owner == 0)
 
    is_in_all = 0
    for member in all_members:
        if member['u_id'] == u_id_2:
            is_in_all = 1
    assert (is_in_all == 1)
    clear() 