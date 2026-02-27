
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


if __name__ == "__main__":
    user_json = create_user("Ann", 20)
    print("Created:", user_json)

    parsed = parse_user(user_json)
    print("Parsed:", parsed)

    j1 = json.dumps({"a": 1, "b": 2})
    j2 = json.dumps({"b": None, "c": 3})
    print("Merged:", merge_json(j1, j2))
