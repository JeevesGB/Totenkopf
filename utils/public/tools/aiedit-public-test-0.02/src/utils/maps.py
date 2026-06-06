import os
import sys
sys.dont_write_bytecode = True
import json


def load_maps_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            return [str(m) for m in data]
    except Exception:
        pass
    return []


def find_maps_json():
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    candidates = [
        os.path.join(script_dir, 'maplist.json'),
        os.path.join(script_dir, 'utils', 'maplist.json'),
        os.path.join(os.getcwd(), 'maplist.json'),
        os.path.join(os.getcwd(), 'utils', 'maplist.json'),
    ]
    for candidate in candidates:
        if os.path.isfile(candidate):
            return candidate
    return None