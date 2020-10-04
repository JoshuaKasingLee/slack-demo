from database import master_users, message, messages, channel, channels, member, members, channels_and_members, channels_and_messages

# add functions below if needed
def clear():
    global master_users
    master_users.clear()
    #global user
    #user.clear()
    #global users
    #users.clear()
    global message
    message.clear()
    global messages
    messages.clear()
    global channel
    channel.clear()
    global channels
    channels.clear()
    global member
    member.clear()
    global members
    members.clear()
    global channels_and_members
    channels_and_members.clear()
    global channels_and_messages
    channels_and_messages.clear()

# channel with members
# channels_and_members = { channel_id: [owner_members, all_members], channel2: [owner_members2, all_members2], ...}
# channels_and_members = {}

# messages in channels
#channels_and_messages = { channel_id: messages, channel_id2: messages2, ... }
#channels_and_messages = { 1: [ { 'message_id': 1, 'u_id': 1, 'message' = 'whtever the fuck', 'time_created' = 1111111111 }, { 'message_id': 2, ... } ... ], 2: ... }
# channels_and_messages = {}

def users_all(token):
    return {
        'users': [
            {
                'u_id': 1,
                'email': 'cs1531@cse.unsw.edu.au',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'hjacobs',
            },
        ],
    }

def search(token, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }