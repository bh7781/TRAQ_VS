import pandas as pd
import re
import numpy as np
import logging
import os
import psutil
import gc
import sys
from common import constants
from datetime import datetime


def single_underscore(str_value):
    replaced_string = re.sub('[_]+', '_', str_value)
    return replaced_string


def basic_processing(input_df):
    input_df = input_df.replace(np.nan, '')
    # input_df = input_df.apply(lambda x: x.astype(str).str.lower())
    input_df = input_df.apply(lambda x: x.astype(str).str.replace('"', ''))
    input_df = input_df.apply(lambda x: x.astype(str).str.replace('?', ''))
    input_df = input_df.applymap(str)
    input_df.columns = map(str.lower, input_df.columns)
    input_df = input_df.apply(lambda x: x.astype(str).str.strip())
    input_df.columns = map(str.strip, input_df.columns)
    # input_df.columns = [replace_right(column_name, '.', '', 1) for column_name in list(input_df.columns)]
    input_df.columns = [col.strip().replace('-', ' ').replace(':', ' ')
                        .replace('(', ' ').replace(')', ' ')
                        .replace('/', ' ').replace(' ', '_')
                        for col in list(input_df.columns)]
    input_df.columns = [single_underscore(col) for col in list(input_df.columns)]
    return input_df


def create_combined_dataframe(all_files, use_cols=None):
    temp_list = []
    for filename in all_files:
        print('Filename: ', filename)
        df = pd.read_csv(filename, usecols=use_cols, skiprows=0, low_memory=False)
        print(df.shape)
        temp_list.append(df)

    print('Starting concat')
    frame2 = pd.concat(temp_list, axis=0, sort=False)
    print('Finished concat')
    frame2 = frame2.reset_index()
    frame2 = frame2.replace(np.nan, '')
    return frame2


def log_message_separator(pattern, length, log_message, double_separator):
    separator = pattern * length
    logging.info(separator)
    logging.info(log_message)
    if double_separator == 1:
        logging.info(separator)


def is_file_check(path):
    return os.path.isfile(path)


# def get_report_date(file_path, report_date_line=1):
#     """
#     Extracts the "Report Date" from a specified line in the CSV file.
#     """
#     # Adjust the line number for 0-based indexing
#     report_date_line_index = report_date_line - 1
#
#     # Extract the "Report Date" from the specified line
#     with open(file_path, 'r') as file:
#         for i, line in enumerate(file):
#             if i == report_date_line_index:
#                 print(line)
#                 report_date = line.strip().split('"Report Date" ')[1].split(' ')[0]
#                 return report_date
#
#     # If the function reaches here, it means the report date was not found on the specified line
#     raise ValueError(f"Report Date not found on line {report_date_line}")

def get_report_date(file_path, report_date_line=1):
    """
    Extracts the "Report Date" from a specified line in the CSV file.
    Handles various formatting variations.
    """
    # Adjust the line number for 0-based indexing
    report_date_line_index = report_date_line - 1

    # Extract the "Report Date" from the specified line
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            if i == report_date_line_index:
                # Look for 'Report Date' (case-insensitive) followed by a date
                # Regex pattern to find a date after 'Report Date', including multiple variations
                match = re.search(r'(?:"?[Rr]eport\s*[Dd]ate"?)\s*(\d{4}-\d{2}-\d{2})', line)

                if match:
                    return match.group(1)

    # If the function reaches here, it means the report date was not found
    raise ValueError(f"Report Date not found on line {report_date_line}")


def log_memory_usage_before_after_gc(logger):
    """
    Logs the memory usage before and after garbage collection.
    """
    process = psutil.Process()

    # Get memory usage before garbage collection
    mem_before = process.memory_info().rss / 1024 ** 2  # Convert to MB

    # Force garbage collection
    gc.collect()

    # Get memory usage after garbage collection
    mem_after = process.memory_info().rss / 1024 ** 2  # Convert to MB

    # Calculate the difference
    mem_cleared = mem_before - mem_after

    # Log the memory usage and the amount of memory cleared
    logger.info(f"Memory usage before GC: {mem_before:.2f} MB")
    logger.info(f"Memory usage after GC: {mem_after:.2f} MB")
    logger.info(f"Memory cleared by GC: {mem_cleared:.2f} MB")


def add_entity_names(input_df, gleif_dict, lei_columns):
    """
    Map LEI values to Entity Names and add corresponding columns to the dataframe.
    Handles multiple LEIs in a cell separated by ';' and removes spaces from LEI values.

    Parameters:
    input_df (pd.DataFrame): The dataframe containing LEI columns.
    gleif_dict (dict): A dictionary with LEI as keys and 'Entity Name' as values.
    lei_columns (list of str): List of column names in input_df that contain LEI values.

    Returns:
    pd.DataFrame: The updated dataframe with new columns containing Entity Names.
    """
    # Ensure the necessary mapping exists
    if not isinstance(gleif_dict, dict):
        raise ValueError("gleif_dict must be a dictionary with LEI as keys and Entity Names as values.")

    # For each LEI column in the dataframe
    for col in lei_columns:
        # Check if the column exists in the dataframe
        if col not in input_df.columns:
            raise ValueError(f"Column '{col}' does not exist in the dataframe.")

        # Remove all spaces from the LEI column values
        input_df[col] = input_df[col].fillna('').astype(str).str.replace(' ', '', regex=False)

        # Define the new column name by appending '_entity_name' suffix
        new_col_name = f"{col}_entity_name"

        # Split LEI values on ';' to handle multiple LEIs in a single cell
        lei_series = input_df[col].str.split(';')

        # Explode the lists into a flat Series, aligning with the original index
        lei_exploded = lei_series.explode()

        # Map LEI values to Entity Names using the gleif_dict dictionary
        entity_names = lei_exploded.map(gleif_dict)

        # Group the mapped Entity Names back to the original dataframe's index
        # Join multiple Entity Names with ';' to match the original format
        # Handle missing values by assigning NaN where necessary
        entity_names_grouped = entity_names.groupby(lei_exploded.index).apply(
            lambda x: ';'.join(x.dropna()) if not x.isnull().all() else pd.NA
        )

        # Assign the grouped Entity Names to the new column in the dataframe
        input_df[new_col_name] = entity_names_grouped

    # Return the updated dataframe with new Entity Name columns added
    return input_df


def adjust_path_for_os(path):
    """
    Adjusts the given path based on the operating system.
    Converts to Universal Naming Convention (UNC) paths on Windows if necessary.

    Parameters:
    path (str): The file path to adjust.

    Returns:
    str: The adjusted file path.
    """
    import platform
    if platform.system() == 'Windows':
        if path.startswith('/'):
            # Convert to UNC path
            path = '\\\\' + path.lstrip('/').replace('/', '\\')
        else:
            path = path.replace('/', '\\')
    else:
        path = path.replace('\\', '/')
    return path


def validate_file_existence(filepath, logger):
    """
    Generic function to validate file existence by first checking directory path validity
    and then verifying if the file exists at the specified location.
    Will terminate program execution if directory path is invalid or file is not found.
    """
    # First validation: Check if filepath input is empty or None
    if not filepath:
        error_msg = "Empty or None filepath provided"
        logger.error(error_msg)
        logger.error("Terminating program execution due to invalid filepath.")
        sys.exit(1)

    # Handle list of filepaths
    if isinstance(filepath, list):
        # Iterate through each filepath in the list
        for file in filepath:
            # Validate individual filepath in list is not empty
            if not file:
                error_msg = "Empty filepath found in the list"
                logger.error(error_msg)
                logger.error("Terminating program execution due to invalid filepath.")
                sys.exit(1)

            # Extract directory path from full filepath
            directory = os.path.dirname(file)

            # Handle case when file is in current directory
            # If directory path is empty, set it to current directory '.'
            if not directory:
                directory = '.'

            # Validate directory path exists
            # This check ensures the path to file is valid before checking file itself
            if not os.path.exists(directory):
                error_msg = f"Directory path does not exist: {directory}"
                logger.error(error_msg)
                logger.error("Terminating program execution due to invalid directory path.")
                sys.exit(1)

            # Finally check if file exists and is actually a file (not a directory)
            # os.path.isfile() ensures the path points to a file and not a directory
            if not os.path.isfile(file):
                error_msg = f"File not found at path: {file}"
                logger.error(error_msg)
                logger.error("Terminating program execution due to missing file.")
                sys.exit(1)

    # Handle single filepath
    else:
        # Extract directory path from full filepath
        directory = os.path.dirname(filepath)

        # Handle case when file is in current directory
        # If directory path is empty, set it to current directory '.'
        if not directory:
            directory = '.'

        # Validate directory path exists
        # This check ensures the path to file is valid before checking file itself
        if not os.path.exists(directory):
            error_msg = f"Directory path does not exist: {directory}"
            logger.error(error_msg)
            logger.error("Terminating program execution due to invalid directory path.")
            sys.exit(1)

        # Finally check if file exists and is actually a file (not a directory)
        # os.path.isfile() ensures the path points to a file and not a directory
        if not os.path.isfile(filepath):
            error_msg = f"File not found at path: {filepath}"
            logger.error(error_msg)
            logger.error("Terminating program execution due to missing file.")
            sys.exit(1)

    # Single file check:
    # validate_file_existence('/path/to/file.csv')

    # Multiple files check:
    # validate_file_existence(['/path1/file1.csv', '/path2/file2.csv'])


def get_business_day_offset(base_date, offset):
    """
    Calculates a business day relative to the given base date.

    Parameters:
    base_date (str): The base date in 'YYYY-MM-DD' format.
    offset (int): The number of business days to offset.
                  Positive for future dates, negative for past dates.

    Returns:
    str: The calculated business day in 'YYYY-MM-DD' format.
    """
    from datetime import datetime
    from dateutil.relativedelta import relativedelta

    base_date_dt = datetime.strptime(base_date, '%Y-%m-%d')
    delta = 0  # Initialize a counter for the offset adjustment
    step = 1 if offset > 0 else -1  # Step forward or backward depending on offset sign

    while delta != abs(offset):
        base_date_dt += relativedelta(days=step)
        # Skip weekends
        if base_date_dt.weekday() not in [5, 6]:  # Monday-Friday only
            delta += 1

    return base_date_dt.strftime('%Y-%m-%d')


def sanitize_env(environment):
    allowed_envs = ['qa', 'prod']
    if environment.lower() not in allowed_envs:
        raise ValueError(f"Invalid env: {environment}. Allowed: {allowed_envs}")
    return environment.lower()


def sanitize_regime(regime):
    allowed_regimes = [constants.JFSA, constants.ASIC, constants.MAS, constants.EMIR_REFIT]
    if regime.upper() not in allowed_regimes:
        raise ValueError(f"Invalid regime: {regime}. Allowed: {allowed_regimes}")
    return regime.upper()


def sanitize_asset_class(assetclass):
    allowed_asset_classes = [
        constants.COLLATERAL,
        constants.CREDIT,
        constants.COMMODITY,
        constants.EQUITY_SWAPS,
        constants.EQUITY_DERIVATIVES,
        constants.INTEREST_RATES,
        constants.FOREIGN_EXCHANGE,
        constants.EXCHANGE_TRADES_DERIVATIVES_ACTIVITY,
        constants.EXCHANGE_TRADES_DERIVATIVES_POSITION
    ]
    if assetclass not in allowed_asset_classes:
        raise ValueError(f"Invalid or unsafe asset class: {assetclass}")
    return assetclass


def sanitize_run_date(date_str):
    """
    Validate the run_date argument to ensure it is in YYYY-MM-DD format.
    Raises ValueError if the format is invalid.
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid run_date: {date_str}. Must be YYYY-MM-DD format.")
    return date_str


def sanitize_filename(filename):
    """
    Sanitize the filename to prevent path traversal attacks.
    """
    return os.path.basename(filename)


def sanitize_string(input_str: str) -> str:
    """
    Replace all non-alphanumeric/underscore characters with underscores,
    and convert to lowercase.
    """
    return re.sub(r'[^0-9a-zA-Z_]', '_', input_str.strip()).lower()


def get_safe_filepath(base_dir, user_input_path):
    """
    Safely join a base directory with a user-provided path to prevent path traversal.
    Raises ValueError if the resolved path is outside the base directory.
    """
    # Normalize the user input path to remove any '../' or './' sequences
    normalized_user_input = os.path.normpath(user_input_path)

    # Construct the full path
    full_path = os.path.join(base_dir, normalized_user_input)

    # Convert both to absolute paths and check if the full_path is within base_dir
    if not os.path.abspath(full_path).startswith(os.path.abspath(base_dir)):
        raise ValueError(f"Unsafe file path detected: {full_path}")

    return full_path
