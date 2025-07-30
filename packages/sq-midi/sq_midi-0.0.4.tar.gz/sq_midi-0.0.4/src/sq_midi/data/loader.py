import json
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def decode(data):
    if isinstance(data, dict):
        return {key: decode(val) for key, val in data.items()}
    elif isinstance(data, list):
        return [decode(val) for val in data]
    elif isinstance(data, str):
        try:
            return int(data, 16)
        except ValueError:
            return data
    else:
        return data

def load_data(file_name: str):
    with open(os.path.join(__location__, file_name + ".json")) as data:
        return decode(json.load(data))

if __name__ == '__main__':
    test = load_data("inputs")
    print(test[0])