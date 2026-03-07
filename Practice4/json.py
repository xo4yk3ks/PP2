
"""JSON parsing and creation"""

import json


def create_user(name, age):
    data = {"name": name, "age": age}
    return json.dumps(data)


def parse_user(json_string):
    return json.loads(json_string)


def merge_json(a, b):
    """Merge two JSON objects (b overrides a)"""
    obj_a = json.loads(a)
    obj_b = json.loads(b)
    merged = {**obj_a, **obj_b}
    return json.dumps(merged)


