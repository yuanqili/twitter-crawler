import json


def print_json(json_file):
    print(json.dumps(json_file, sort_keys=True, indent=4, separators=(',', ':')))
