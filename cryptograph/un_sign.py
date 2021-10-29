from hashlib import blake2b


def sign(cookie):
    secret_key = b'pseudorandomly generated server secret key'
    auth_size = 16

    h = blake2b(digest_size=auth_size, key=secret_key)
    h.update(cookie)
    return h.hexdigest().encode('utf-8')


def unsign(sig):
    return sig.decode('utf-8')


cookie_alice = b'user-alice'
sig = sign(cookie_alice)
unsig = unsign(sig)
print("sign..: ", sig.decode('utf-8'))
print("unsign: ", unsig)
