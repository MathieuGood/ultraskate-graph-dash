import os
import json
from utils.path_utils import data_dir_path

def get_event_data_from_json(json_filename: str) -> dict:
    json_file_path = os.path.join(data_dir_path, json_filename)
    with open(json_file_path) as json_file:
        return json.load(json_file)