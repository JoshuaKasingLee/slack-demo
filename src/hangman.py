import random
import wikiquote

import database
from error import InputError


def hangman(channel_id):
    if database.hangman_active_check(channel_id):
        raise InputError('Hangman already active in this channel.')
    words = wikiquote.quotes('The Matrix (film)', max_quotes=1)[0].splitlines()[0]
    word = ''
    while len(word) < 4:
        word = random.choice(words.split())
    word = word.lower()
    database.start_hangman(channel_id, word)

def guess(channel_id, message):
    if not database.hangman_active_check(channel_id):
        raise InputError('Hangman not active in this channel.')
    char_guess = message.split(' ', 1)[1]
    if len(char_guess) != 1:
        raise InputError('Guess must be one character.')
    fails = database.hangman_guess(channel_id, char_guess)
    return fails

def print_hangman(channel_id, stage, message):
    if not database.hangman_active_check(channel_id):
        raise InputError('Hangman not active in this channel.')
    # the art looks better with characters of even width
    if stage == 0:
        picture = '\n   \n  O\n  T\n  ^\n'
    if stage == 1:
        picture = '\n   \n| O\n| T\n| ^\n'
    if stage == 2:
        picture = '\n___\n| O\n| T\n| ^\n'
    if stage == 3:
        picture = '\n___\n| x\n| T\n| ^\n'
    word = database.print_hangman_progress(channel_id)
    return message + picture + word

def check_game_end(channel_id, stage):
    word = database.fetch_hangman_word(channel_id)
    if database.check_hangman_victory(channel_id):
        database.end_hangman(channel_id)
        return f'HE LIVES\nGAME WORD : {word}'
    if stage == 3:
        database.end_hangman(channel_id)
        return f'HE IS DEAD BY YOUR HANDS\nGAME WORD : {word}'
    return ''