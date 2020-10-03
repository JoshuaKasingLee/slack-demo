import pytest
import database
import other
from channel_addowner import channel_addowner
from channel_removeowner import channel_removeowner
from channel_join import channel_join
import channels
import auth
from error import InputError
from error import AccessError

#need to test a few things: 
# valid channel (input error), u_id is not an owner (input error).
# access error if token is not global owner OR owner of channel
# regular testing: token is owner and u_id is owner

