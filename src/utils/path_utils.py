import os

data_dir_path = os.path.join(os.path.dirname(__file__), "..", "..", "data")

events_files = sorted(os.listdir(data_dir_path))
