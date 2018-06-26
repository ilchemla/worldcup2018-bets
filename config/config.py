import os
import yaml

current_dir_path = os.path.dirname(os.path.realpath(__file__))
datasets_db_filepath = os.path.join(current_dir_path, 'config.yaml')
with open(datasets_db_filepath, 'r') as stream:
  cfg = yaml.load(stream)