import numpy as np
import pandas as pd
import json
import os
import yaml
from typing import Union


def combine_json_files(input_path: str):
    combined_dict = {}
    file_list = os.listdir(input_path)
    for filename in file_list:
        filepath = os.path.join(input_path, filename)
        raw_data = read_file(filepath)
        raw_data_dict = json.loads(raw_data)
        combined_dict.update(raw_data_dict)
    return combined_dict


def create_dir(filepath: str, discard_last: bool = False):
    sep_char = os.path.join(' ', ' ').strip()
    filepath_split = filepath.split(sep_char)[:-1] if discard_last else filepath.split(sep_char)
    full_filepath = ''
    for directory in filepath_split:
        full_filepath = os.path.join(full_filepath, directory)
        if not os.path.exists(full_filepath):
            os.mkdir(full_filepath)


def read_file(filepath: str):
    if '.yml' in filepath or '.yaml' in filepath:
        with open(filepath, 'r') as file_reader:
            to_return = yaml.safe_load(file_reader)
    elif '.csv' in filepath:
        to_return = pd.read_csv(filepath)
    else:
        with open(filepath, 'r') as file_reader:
            to_return = file_reader.read()
    return to_return


def write_to_file(
        to_write: Union[dict, str, pd.DataFrame],
        filepath: str,
        overwrite: bool = False
) -> bool:
    file_exists = os.path.exists(filepath)
    if file_exists and not overwrite:
        return False
    else:
        create_dir(filepath, discard_last=True)

    if '.yml' in filepath or '.yaml' in filepath:
        with open(filepath, 'w') as file_writer:
            yaml.safe_dump(to_write, filepath)
        return True
    elif '.csv' in filepath:
        to_write.to_csv(filepath, header=True, index=False)
        return True
    elif isinstance(to_write, dict):
        with open(filepath, 'w') as file_writer:
            file_writer.write(json.dumps(to_write))
        return True
    else:
        with open(filepath, 'w') as file_writer:
            file_writer.write(to_write)