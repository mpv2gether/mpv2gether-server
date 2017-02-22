def get_key(message, key):
    if key in message:
        return message[key]
    raise MissingKeyError(key)

class MissingKeyError(Exception):
    def __init__(self, key):
        self.key = key
        Exception.__init__(self, "Missing key: {}".format(key))