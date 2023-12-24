import os

def write_list_to_text_file(file_path, data):
    """
    Write list to text file

    :param file_path:
    :param data:
    :return:
    """
    with open(file_path, "w") as file:
        file.writelines(data)

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