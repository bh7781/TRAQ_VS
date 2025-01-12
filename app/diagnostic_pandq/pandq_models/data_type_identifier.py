import pandas as pd
import warnings

# Suppress specific runtime warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in cast")


class DataTypeIdentifier:
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
        Determines the format of date/timestamp columns.
        """
        date_format_counts = {}

        for fmt in self.DATE_FORMATS:
            try:
                # Attempt to parse the column data with the given format
                parsed_dates = pd.to_datetime(column_data, format=fmt, errors='coerce')
                count = parsed_dates.notnull().sum()

                if count > 0:
                    date_format_counts[fmt] = count
            except (ValueError, TypeError):
                continue

        if date_format_counts:
            most_common_format = max(date_format_counts, key=date_format_counts.get)

            if "H" in most_common_format:
                return "TIMESTAMP"
            else:
                return "DATE"
        else:
            return "STRING"

    def identify_column_types(self, files):
        """
        Identifies and returns data types for each column in each file.
        """
        column_types = {}

        for file in files:
            data = pd.read_csv(file, sep='|', low_memory=False)
            file_column_types = {}

            for column in data.columns:
                file_column_types[column] = self.get_columns_dateformat(data[column])

            column_types[file] = file_column_types

        return column_types
