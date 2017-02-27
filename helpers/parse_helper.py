def get_key(message, key):
    if "message" in message and key in message["message"]:
        return message["message"][key]
    raise MissingKeyError(key)

class MissingKeyError(Exception):
    def __init__(self, key):
        self.key = key
        Exception.__init__(self, "Missing key: {}".format(key))