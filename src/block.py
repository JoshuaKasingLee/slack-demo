import database
from error import InputError

def process_block(message, u_id):
    block_handle = message.split(' ', 1)[1]
    u_block = database.fetch_u_id_from_handle(block_handle)
    if u_block == -1:
        raise InputError(f'Handle {block_handle} does not correspond with an existing user.')
    database.block_user(u_id, u_block)

def process_unblock(message, u_id):
    unblock_handle = message.split(' ', 1)[1]
    u_unblock = database.fetch_u_id_from_handle(unblock_handle)
    if u_unblock == -1:
        raise InputError(f'Handle {unblock_handle} does not correspond with an existing user.')
    database.unblock_user(u_id, u_unblock)
