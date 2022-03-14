import json
from hashlib import sha256


def get_hash(message):
    if type(message) == dict:
        message = json.dumps(message, sort_keys=True)
    return sha256(message.encode('utf-8')).hexdigest()