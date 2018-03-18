import json


def load_config(filepath):
    with open(filepath) as jf:
        return json.load(jf)