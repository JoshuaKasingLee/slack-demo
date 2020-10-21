import pytest
from message import message_send
import auth
import channel
import channels
from error import AccessError
from error import InputError
from other import clear

'''
# Check to see if a message works
# To clarify with team - how to see a message
def test_message_sends():
    user_token = auth.auth_register("user@gmail.com", "password", "John", "Smith")['token']
    channel_id = channels.channels_create(user_token)['channel_id']
    message_to_send = 'Hi!'
    message_id = message_send(user_token, channel_id, message_to_send)['message_id']
    # channel_messages(user_token, channel_id, ) <- originally was going to search through this but not effective
    # as messages is a list of dictionaries -> can't look up the messages in O(1) time
    # I then thought about looking into database, but are we making functions in the database?
    # assert()
    clear()
'''

# Ensure the user is a member of the channel beforehand
''' Pseudo-code
Create a user - input: {email, password, name_first, name_last}     output: {token}
Send Message - input: {token, channel_id, message}                  output: {AccessError}
'''
def test_user_in_channel():
    user_token = auth.auth_register("user@gmail.com", "password", "John", "Smith")['token']
    channel_id = channels.channels_create(user_token, "Test Channel", True)['channel_id']
    message_to_send = 'Hi!'
    user_token = auth.auth_register("user2@gmail.com", "password", "Sam", "Smith")['token']
    with pytest.raises(AccessError):
        message_send(user_token, channel_id, message_to_send)
    clear()


# Ensure the message is less than 1000 characters
''' Pseudo-code
Create a user - input: {email, password, name_first, name_last}     output: {token}
Create a channel - input: {token, name, is_public}                  output: {channel_id}
Send Message - input: {token, channel_id, message}                  output: {InputError}
'''
def test_message_length():
    clear()
    user_token = auth.auth_register("user@gmail.com", "password", "John", "Smith")['token']
    channel_id = channels.channels_create(user_token, "Test Channel", True)['channel_id']
    channel.channel_join(user_token, channel_id)
    message_to_send = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Na'
    with pytest.raises(InputError):
        message_send(user_token, channel_id, message_to_send)
    clear()
