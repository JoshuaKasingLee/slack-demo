from database import master_users, user, users, message, messages, channel, channels, member, members

# add functions below if needed
def clear():
    global master_users
    master_users.clear()
    global user
    user.clear()
    global users
    users.clear()
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