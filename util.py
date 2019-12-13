
import string, random, hashlib

def gen_token(length, chars=string.ascii_letters, taken=set(), tries = 4):
    for i in range(tries):
        token = ''.join(random.choice(chars) for x in range(length))
        if not token in taken:
            return token
    raise Exception("Could not find available token")
