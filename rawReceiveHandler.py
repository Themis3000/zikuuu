import json
from collections import namedtuple


def to_object(data):
    if data[:1] == '{':
        return json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    else:
        return False
