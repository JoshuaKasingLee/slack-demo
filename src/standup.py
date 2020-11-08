import database
from error import InputError
from error import AccessError
from datetime import datetime
from datetime import timedelta
import threading
import time


def standup_start(token, channel_id, length):

    u_id = database.token_check(token)
    database.channels_user_log_check(u_id)

    database.channel_valid_channel(channel_id)

    end_time = datetime.now() + timedelta(seconds=length)
    database.add_standup(channel_id, end_time)
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
