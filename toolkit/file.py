import os

import pandas as pd


def write_list_to_text_file(file_path, data, mode="w"):
    """
    Write list to text file in splitting elements to new line

    :param mode: Write mode ('w' for write, 'a' for append)
    :param file_path: Path to the text file
    :param data:
    :return:
    """
    if mode == 'a' and os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        data.insert(0, "")

    with open(file_path, mode) as file:
        file.write("\n".join(data))


def read_list_from_text_file(file_path) -> list:
    """

    Check if file exists then read list from text file

    :param file_path:
    :return:
    """
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r") as file:
        data = file.readlines()
    return data


def read_from_csv(file_path: str): # -> Generator[Dict[str, str], None, None]:
    """
    Read CSV file and yield each row as a dictionary

    :param file_path: Path to the CSV file
    :return:
    """
    df = pd.read_csv(file_path)

    # Iterate over the DataFrame rows and yield each row as a dictionary
    for index, row in df.iterrows():
        yield row.to_dict()

def read_column_names_from_csv(file_path: str) -> list[str]:
    """
    Read CSV file and yield each row as a dictionary

    :param file_path: Path to the CSV file
    :return:
    """
    df = pd.read_csv(file_path)
    return df.columns.tolist()

def write_to_csv(file_path, input_dict, headers=None, mode='a'):
    """
    Write dictionary to CSV file

    :param file_path: Path to the CSV file
    :param input_dict: Dictionary to write to the CSV file
    :param headers: List of headers to include in the CSV file
    :param mode: Write mode ('w' for write, 'a' for append)
    :return:
    """
    if headers:
        input_dict = {key: input_dict.get(key, None) for key in headers}

    # Convert the input dictionary to a DataFrame
    df = pd.DataFrame([input_dict])

    # Write the DataFrame to the CSV file based on the mode provided (e.g., 'w' or 'a')
    df.to_csv(file_path, mode=mode, header=(mode == 'w'), index=False, columns=headers)
