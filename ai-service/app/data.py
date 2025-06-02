import json
def get_data_from_json():
    data = None
    with open("cl-data-3seasons.json") as f:
        data = json.load(f)
    return data