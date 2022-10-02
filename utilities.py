import string

ALPHABET = string.digits + string.ascii_letters
base = len(ALPHABET)

def base62encode(num: int):
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



