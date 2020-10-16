import pytest
from other import clear
from channel import channel_addowner, channel_removeowner, channel_details, channel_join
import channels
import auth
from error import InputError, AccessError



def test_valid_channel() :
    clear()
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    u_id = user['u_id']
    token = user['token']
    channel_id = 999
    with pytest.raises(InputError) as e:
        channel_removeowner(token, channel_id, u_id)
    clear()
 
def test_uid_not_channel_owner() :
    clear()
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    u_id = user['u_id']
    token = user['token']
    user_2 = auth.auth_register("email2@gmail.com", "passwords", "Johns", "Smiths")
    u_id_2 = user_2['u_id']
    token_2 = user_2['token'] 
    channel_id = channels.channels_create(token, "Channel1", True)['channel_id']
    with pytest.raises(InputError) as e:
        channel_removeowner(token, channel_id, u_id_2)
    clear()
 
def test_not_global_or_local_owner() :
    clear()
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    u_id = user['u_id']
    token = user['token']
    user_2 = auth.auth_register("email2@gmail.com", "passwords", "Johns", "Smiths")
    u_id_2 = user_2['u_id']
    token_2 = user_2['token']   
    channel_id = channels.channels_create(token, "Channel1", True)['channel_id']
    with pytest.raises(AccessError) as e:
        channel_removeowner(token_2, channel_id, u_id)
    clear()   
