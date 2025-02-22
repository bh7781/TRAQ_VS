import pandas as pd
import warnings

# Suppress specific runtime warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in cast")

def detect_delimiter(file_path):
    """
    Detects the delimiter of a CSV file by reading its first line.
    Returns ',' if comma is more frequent than '|', otherwise returns '|'.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline()
        pipe_count = first_line.count('|')
        comma_count = first_line.count(',')
        return ',' if comma_count > pipe_count else '|'
    except Exception:
        # In case of error, default to pipe delimiter.
        return '|'

class ColumnDataTypeIdentifier:
    """
    Identifies data types of columns, focusing on DATE, TIMESTAMP, and STRING.
    """

    DATE_FORMATS = [
        '%Y', '%b %d, %Y', '%b %d, %Y', '%B %d, %Y', '%B %d %Y',
        "%H:%M:%S", '%m/%d/%Y', '%m/%d/%y', '%m-%d-%Y', '%m-%d-%y',
        '%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%d-%m-%y',
        '%Y/%m/%d', '%y/%m/%d', '%Y-%m-%d', '%y-%m-%d',
        '%b %Y', '%B%Y', '%b %d,%Y', '%Y-%m-%d %H:%M:%S',
        "%Y-%m-%d %H:%M:%S.%f", '%Y-%m-%d %H:%MZ', '%Y-%m-%dT%H:%M:%SZ',
        '%Y-%m-%dT%H:%M:%S.%fZ'
    ]

    def get_columns_dateformat(self, column_data: pd.Series):
        """
        Determines the date format for a given column of data.
        """
        date_format_counts = {}

        for fmt in self.DATE_FORMATS:
            try:
                parsed_dates = pd.to_datetime(column_data, format=fmt, errors='coerce')
                count = parsed_dates.notnull().sum()
                if count > 0:
                    date_format_counts[fmt] = count
            except (ValueError, TypeError):
                continue

        if date_format_counts:
            most_common_format = max(date_format_counts, key=date_format_counts.get)
            return "TIMESTAMP" if "H" in most_common_format else "DATE"
        else:
            return "STRING"

    def identify_column_types(self, files):
        """
        Identifies and returns data types for each column in each file.
        Returns a dictionary mapping each file path to a dictionary of column names and data types.
        """
        column_types = {}
        for file in files:
            delimiter = detect_delimiter(file)
            try:
                data = pd.read_csv(file, sep=delimiter, low_memory=False)
            except Exception as e:
                print(f"ERROR reading file {file}: {e}")
                continue

            file_column_types = {}
            for column in data.columns:
                file_column_types[column] = self.get_columns_dateformat(data[column])
            column_types[file] = file_column_types
        return column_types
