import hashlib

def get_gravatar_hash(email):
    """Creates a Gravatar hash

    http://en.gravatar.com/site/implement/hash/
    """
    gravatar_hash = hashlib.md5(email.strip().lower()).hexdigest()
    return gravatar_hash
