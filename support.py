from random import choice


def gen_key():
    """Generates a random 48 character key"""
    result = ''
    char = '1234567890!@#$%^&*~`abcdefghijklmnopqustuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    while len(result) < 48:
        result += choice(char)
    return result
