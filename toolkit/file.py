import os
from typing import List, Optional

import pandas as pd


def remove_duplicates(
        input_csv_path: Optional[str] = None,
        input_df: Optional[pd.DataFrame] = None,
        unique_columns: List[str] = None,
        columns_to_prioritize: Optional[List[str]] = None,
        rewrite: bool = False
) -> Optional[pd.DataFrame]:
    """
    Removes duplicates from the provided CSV or DataFrame, prioritizing rows with non-empty values
    in the specified columns. If columns_to_prioritize is not provided or is empty, keeps rows that
    have the most columns filled. Uses unique_columns to identify duplicates.

    :param input_csv_path: Path to the input CSV file. Used if input_df is not provided.
    :param input_df: A pandas DataFrame to process directly. Takes priority over input_csv_path.
    :param unique_columns: List of columns that should be treated as unique to identify duplicates.
    :param columns_to_prioritize: List of columns to prioritize when removing duplicates.
                                  Rows with non-empty values in these columns will be kept.
                                  If None or empty, prioritizes rows with the most filled columns.
    :param rewrite: If True, rewrites the original CSV file (if input_csv_path is provided) after
                    removing duplicates. If False, returns the cleaned DataFrame.
    :returns: Cleaned DataFrame with duplicates removed if rewrite is False, otherwise None.
    """
    # Ensure that either input_csv_path or input_df is provided
    if input_df is not None:
        df = input_df.copy()
    elif input_csv_path is not None:
        df = pd.read_csv(input_csv_path)
    else:
        raise ValueError("Either input_csv_path or input_df must be provided.")

    # Ensure unique_columns is provided
    if unique_columns is None or not unique_columns:
        raise ValueError("unique_columns must be provided to identify duplicates.")

    # If columns_to_prioritize is None or empty, prioritize rows with the most non-NA values
    if not columns_to_prioritize:
        # Sort by the number of non-NA values across all columns
        df['non_na_count'] = df.notna().sum(axis=1)
        df = df.sort_values(by='non_na_count', ascending=False)
        df = df.drop(columns=['non_na_count'])  # Drop helper column
    else:
        # Sort by the columns to prioritize, ensuring rows with values in those columns come first
        df = df.sort_values(by=columns_to_prioritize, ascending=False, na_position='last')

    # Drop duplicates, based on the unique columns
    df_cleaned = df.drop_duplicates(subset=unique_columns, keep='first')

    # Optionally rewrite the CSV if input_csv_path is provided and rewrite flag is True
    if rewrite and input_csv_path is not None:
        df_cleaned.to_csv(input_csv_path, index=False)
        return None

    return df_cleaned


def read_csvs_from_directory(directory_path) -> pd.DataFrame:
    """
    Reads all CSV files from the specified directory and combines them into a single Pandas DataFrame.

    :param directory_path: Path to the directory containing the CSV files.
    :returns: A single Pandas DataFrame containing the data from all CSVs.
    """
    all_dataframes = []

    # Loop through all files in the directory
    for filename in os.listdir(directory_path):
        # Check if the file is a CSV
        if filename.endswith(".csv"):
            file_path = os.path.join(directory_path, filename)
            # Read the CSV file into a DataFrame
            try:
                df = pd.read_csv(file_path)
                all_dataframes.append(df)
            except pd.errors.EmptyDataError:
                pass

    # Concatenate all DataFrames into one
    if all_dataframes:
        combined_df = pd.concat(all_dataframes, ignore_index=True)
    else:
        combined_df = pd.DataFrame()  # Return an empty DataFrame if no CSVs are found

    return combined_df


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
