import database
from error import InputError
from error import AccessError
import threading
import time


def standup_start(token, channel_id, length):

    u_id = database.token_check(token)
    database.channels_user_log_check(u_id)

    database.channel_valid_channel(channel_id)

    end_time = time.time() + length
    database.add_standup(channel_id, end_time, u_id)
    t = threading.Timer(length, lambda: database.standup_removal(channel_id))
    t.start()
    # database.standup_removal(channel_id)
    return {'time_finish': end_time}


def standup_active(token, channel_id):

    u_id = database.token_check(token)
    database.channels_user_log_check(u_id)

    database.channel_valid_channel(channel_id)
    active_status = database.active_check(channel_id)
    return active_status

#millisecond error and also continual time checker to remove active standups?

def standup_send(token, channel_id, message):

    u_id = database.token_check(token)
    database.channels_user_log_check(u_id)

    database.channel_valid_channel(channel_id)
    database.channel_member_permissions(channel_id, u_id)

    if len(message) > 1000:
        raise InputError

    if standup_active(token, channel_id) == False:
        raise InputError

    name = database.fetch_first_name(u_id)

    if len(database.standup_fetch_message(channel_id)) != 0:
        standup_message = f"\n{name}: {message}"
    else:
        standup_message = f"{name}: {message}"

    database.standup_message_add(channel_id, standup_message)

    return {}