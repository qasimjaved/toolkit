import os

def write_list_to_text_file(file_path, data, mode="w"):
    """
    Write list to text file in splitting elements to new line

    :param mode:
    :param file_path:
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