from hashlib import sha256


def get_hash(message):
    return sha256(message.encode('utf-8')).hexdigest()