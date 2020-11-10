import pytest
from message import message_sendlater
import auth
import channel
import channels
import time
import database
from error import AccessError
from error import InputError
from other import clear

# Test to make sure that message is sent with the time delay
def test_message_delay():
    clear()
    ## Insert Code
    user = auth.auth_register("user@gmail.com", "password", "John", "Smith")
    user_token = user['token']
    channel_id = channels.channels_create(user_token, "Test Channel", True)['channel_id']
    message_to_send = 'Hi!'
    curr_time = time.time()
    time_sent = curr_time + 5
    message_sendlater(user_token, channel_id, message_to_send, time_sent)
    assert(len(channel.channel_messages(user_token, channel_id, 0)['messages']) == 0)
    time.sleep(6)
    assert(len(channel.channel_messages(user_token, channel_id, 0)['messages']) == 1)
    clear()

# Test to make sure test cannot be sent into the past ~ Raise input error
def test_message_to_past():
    clear()
    ## Insert Code
    user = auth.auth_register("user@gmail.com", "password", "John", "Smith")
    user_token = user['token']
    channel_id = channels.channels_create(user_token, "Test Channel", True)['channel_id']
    message_to_send = 'Hi!'
    curr_time = time.time()
    time_sent = curr_time - 5
    with pytest.raises(InputError):
        message_sendlater(user_token, channel_id, message_to_send, time_sent)
    clear()

# Check to make sure message length is > than 1000
def test_message_length():
    clear()
    user_token = auth.auth_register("user@gmail.com", "password", "John", "Smith")['token']
    channel_id = channels.channels_create(user_token, "Test Channel", True)['channel_id']
    channel.channel_join(user_token, channel_id)
    curr_time = time.time()
    time_sent = curr_time + 5
    message_to_send = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Na'
    with pytest.raises(InputError):
        message_sendlater(user_token, channel_id, message_to_send, time_sent)
    clear()

# Make sure user cannot send if they haven't joined the channel they want to join
def test_user_in_channel():
    clear()
    ## Insert Code
    user_1 = auth.auth_register("user@gmail.com", "password", "John", "Smith")
    user_token_1 = user_1['token']
    channel_id_1 = channels.channels_create(user_token_1, "Test Channel", True)['channel_id']
    user_2 = auth.auth_register("user1@gmail.com", "password", "John", "Smith")
    user_token_2 = user_2['token']
    channels.channels_create(user_token_2, "Test2 Channel", True)['channel_id']
    message_to_send = 'Hi!'
    curr_time = time.time()
    time_sent = curr_time + 5
    with pytest.raises(AccessError):
        message_sendlater(user_token_2, channel_id_1, message_to_send, time_sent)
    clear()

# Make sure message is correct (payload is correct)
def test_message_success():
    clear()
    ## Insert Code
    user = auth.auth_register("user@gmail.com", "password", "John", "Smith")
    user_token = user['token']
    channel_id = channels.channels_create(user_token, "Test Channel", True)['channel_id']
    message_to_send = 'Hi!'
    curr_time = time.time()
    time_sent = curr_time + 5
    message_sendlater(user_token, channel_id, message_to_send, time_sent)
    assert(len(database.messages) == 0)
    time.sleep(6)
    assert(channel.channel_messages(user_token, channel_id, 0)['messages'][0]['message'] == message_to_send)
    clear()
