import string
import uuid


ALPHABET = string.digits + string.ascii_letters
base = len(ALPHABET)


def base62encode(num: int) -> str:
    """ Base 62 Encode a number."""
    if num == 0:
        return ALPHABET[0]
    else:
        res = list()
        while num:
            num, remainder = divmod(num, base)
            res.append(ALPHABET[remainder])
        res.reverse()
        return ''.join(res)


def generate_mapkey() -> str:
    """ Generate a unique shortened mapkey for creating the shortened URL."""
    uid = uuid.uuid4().int
    shortened_uid = int(str(uid)[:8])
    return base62encode(shortened_uid)
    
