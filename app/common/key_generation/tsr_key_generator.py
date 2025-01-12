"""
This module defines the base class for generating matching keys in TSR files.
Regime-specific classes can extend this base class to implement their own key generation logic.
"""

import pandas as pd
import numpy as np
import re

from common import constants
from common.config.logger_config import get_logger


class TSRKeyGenerator:
    def __init__(self, data, asset_class, environment, report_date, use_case):
        """
        Initialize the TSRKeyGenerator
        """
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be a pandas dataframe.")
        self.data = data
        self.asset_class = asset_class
        self.logger = get_logger(name=__name__, env=environment, date=report_date, use_case_name=use_case)

    def validate_columns(self):
        """
        Validate that the DataFrame contains all required columns.
        """
        raise NotImplementedError("This method should be implemented by the child class.")

    def clean_columns(self, required_columns):
        """
        Clean the values in the required columns by removing NaNs, stripping spaces,
        converting everything to uppercase, and replacing missing values with a placeholder
        that includes the column name and a random integer.
        """
        try:
            self.logger.debug('Cleaning required columns')
            for col in required_columns:
                # Clean the data by filling NaNs, stripping spaces, and converting to uppercase
                self.data[col] = self.data[col].fillna('').astype(str).str.strip().str.upper()

                # Replace blank or null values with a placeholder
                mask = self.data[col] == ''
                if mask.any():
                    placeholders = (
                        "missing_place_holder_" + col + "_" +
                        np.random.randint(0, len(self.data), size=mask.sum()).astype(str)
                    )
                    self.data.loc[mask, col] = placeholders

        except Exception as e:
            print(f"Error cleaning columns: {e}")
            raise

    def generate_keys(self):
        """
        Generate matching keys based on the specific columns defined by the child asset class.
        """
        raise NotImplementedError("This method should be implemented by the child class.")


class JFSATSRKeyGenerator(TSRKeyGenerator):
    def __init__(self, data, asset_class, environment, report_date, use_case):
        """
        Initialize the JFSA TSR KeyGenerator.
        """
        super().__init__(data, asset_class, environment, report_date, use_case)
        self.logger.debug('Started creating TSR keys')
        if self.asset_class in [constants.EQUITY_DERIVATIVES, constants.EQUITY_DERIVATIVES]:
            self.required_columns = ['Unique transaction identifier (UTI)']
        else:
            self.required_columns = ['Counterparty 1 (reporting counterparty)', 'Unique transaction identifier (UTI)']

    def validate_columns(self):
        """
        Validate that the DataFrame contains all required columns.
        """
        self.logger.debug('Validate that the DataFrame contains all required columns.')
        missing_columns = [col for col in self.required_columns if col not in self.data.columns]
        if missing_columns:
            raise KeyError(f"Missing required column(s): {', '.join(missing_columns)}")

    def generate_keys(self):
        """
        Generate matching keys based on LEI and various identifiers using str.cat,
        but store the results in a dictionary and concatenate at the end.
        """
        new_columns = {}
        try:
            pattern = re.compile(r'[^a-zA-Z0-9]')

            if self.asset_class in [constants.EQUITY_DERIVATIVES, constants.EQUITY_SWAPS]:
                self.logger.debug(f'Creating matching_key_uti for {self.asset_class}')
                new_columns['matching_key_uti'] = self.data['Unique transaction identifier (UTI)']
            else:
                self.logger.debug(f'Creating matching_key_uti for {self.asset_class}')
                uti = self.data['Counterparty 1 (reporting counterparty)'].str.cat(
                    self.data['Unique transaction identifier (UTI)'], na_rep=''
                )
                new_columns['matching_key_uti'] = uti

                if self.asset_class == constants.INTEREST_RATES:
                    self.logger.debug(f'Creating matching_key_straddle_uti for {self.asset_class}')
                    straddle_uti = self.data['Counterparty 1 (reporting counterparty)'].str.cat(
                        self.data['Unique transaction identifier (UTI)'].str[:-1], na_rep=''
                    )
                    new_columns['matching_key_straddle_uti'] = straddle_uti.apply(lambda x: pattern.sub('', x).upper())

            new_columns['matching_key_uti'] = new_columns['matching_key_uti'].apply(lambda x: pattern.sub('', x).upper())

            # Concatenate new columns to the DataFrame
            self.data = pd.concat([self.data, pd.DataFrame(new_columns)], axis=1)

        except Exception as e:
            print(f"Error generating keys: {e}")
            raise

        return self.data


class ASICTSRKeyGenerator(TSRKeyGenerator):
    def __init__(self, data, asset_class, environment, report_date, use_case):
        """
        Initialize the ASIC TSR KeyGenerator.
        """
        super().__init__(data, asset_class, environment, report_date, use_case)
        if self.asset_class in [constants.EQUITY_DERIVATIVES, constants.EQUITY_DERIVATIVES]:
            self.required_columns = ['Unique transaction identifier']
        else:
            self.required_columns = ['Counterparty 1', 'Unique transaction identifier']

    def validate_columns(self):
        """
        Validate that the DataFrame contains all required columns.
        """
        missing_columns = [col for col in self.required_columns if col not in self.data.columns]
        if missing_columns:
            raise KeyError(f"Missing required column(s): {', '.join(missing_columns)}")

    def generate_keys(self):
        """
        Generate matching keys using str.cat, store in dictionary, and then concatenate.
        """
        new_columns = {}
        try:
            pattern = re.compile(r'[^a-zA-Z0-9]')

            if self.asset_class in [constants.EQUITY_DERIVATIVES, constants.EQUITY_SWAPS]:
                new_columns['matching_key_uti'] = self.data['Unique transaction identifier']
            else:
                uti = self.data['Counterparty 1'].str.cat(
                    self.data['Unique transaction identifier'], na_rep=''
                )
                new_columns['matching_key_uti'] = uti

                if self.asset_class == constants.INTEREST_RATES:
                    straddle_uti = self.data['Counterparty 1'].str.cat(
                        self.data['Unique transaction identifier'].str[:-1], na_rep=''
                    )
                    new_columns['matching_key_straddle_uti'] = straddle_uti.apply(lambda x: pattern.sub('', x).upper())

            new_columns['matching_key_uti'] = new_columns['matching_key_uti'].apply(lambda x: pattern.sub('', x).upper())

            self.data = pd.concat([self.data, pd.DataFrame(new_columns)], axis=1)

        except Exception as e:
            print(f"Error generating keys: {e}")
            raise

        return self.data


class MASTSRKeyGenerator(TSRKeyGenerator):
    def __init__(self, data, asset_class, environment, report_date, use_case):
        """
        Initialize the MAS TSR KeyGenerator.
        """
        super().__init__(data, asset_class, environment, report_date, use_case)
        if self.asset_class in [constants.EQUITY_DERIVATIVES, constants.EQUITY_DERIVATIVES]:
            self.required_columns = ['Unique transaction identifier (UTI)']
        else:
            self.required_columns = ['Counterparty 1', 'Unique transaction identifier (UTI)']

    def validate_columns(self):
        """
        Validate that the DataFrame contains all required columns.
        """
        missing_columns = [col for col in self.required_columns if col not in self.data.columns]
        if missing_columns:
            raise KeyError(f"Missing required column(s): {', '.join(missing_columns)}")

    def generate_keys(self):
        """
        Generate matching keys using str.cat, store in dictionary, and then concatenate.
        """
        new_columns = {}
        try:
            pattern = re.compile(r'[^a-zA-Z0-9]')

            if self.asset_class in [constants.EQUITY_DERIVATIVES, constants.EQUITY_SWAPS]:
                new_columns['matching_key_uti'] = self.data['Unique transaction identifier (UTI)']
            else:
                uti = self.data['Counterparty 1'].str.cat(
                    self.data['Unique transaction identifier (UTI)'], na_rep=''
                )
                new_columns['matching_key_uti'] = uti

                if self.asset_class == constants.INTEREST_RATES:
                    straddle_uti = self.data['Counterparty 1'].str.cat(
                        self.data['Unique transaction identifier (UTI)'].str[:-1], na_rep=''
                    )
                    new_columns['matching_key_straddle_uti'] = straddle_uti.apply(lambda x: pattern.sub('', x).upper())

            new_columns['matching_key_uti'] = new_columns['matching_key_uti'].apply(lambda x: pattern.sub('', x).upper())

            self.data = pd.concat([self.data, pd.DataFrame(new_columns)], axis=1)

        except Exception as e:
            print(f"Error generating keys: {e}")
            raise

        return self.data


class EMIR_REFITTSRKeyGenerator(TSRKeyGenerator):
    def __init__(self, data, asset_class, environment, report_date, use_case):
        """
        Initialize the EMIR Refit TSR KeyGenerator.
        """
        super().__init__(data, asset_class, environment, report_date, use_case)
        self.logger.debug('Started creating TSR keys')
        if self.asset_class in [constants.EQUITY_DERIVATIVES, constants.EQUITY_DERIVATIVES]:
            self.required_columns = ['UTI']
        else:
            self.required_columns = ['Counterparty 1 (Reporting counterparty)', 'UTI']

    def validate_columns(self):
        """
        Validate that the DataFrame contains all required columns.
        """
        self.logger.debug('Validate that the DataFrame contains all required columns.')
        missing_columns = [col for col in self.required_columns if col not in self.data.columns]
        if missing_columns:
            raise KeyError(f"Missing required column(s): {', '.join(missing_columns)}")

    def generate_keys(self):
        """
        Generate matching keys using str.cat, store in dictionary, and then concatenate.
        """
        new_columns = {}
        try:
            if self.asset_class in [constants.EQUITY_DERIVATIVES, constants.EQUITY_SWAPS]:
                self.logger.debug(f'Creating matching_key_uti for {self.asset_class}')
                new_columns['matching_key_uti'] = self.data['UTI']
            else:
                self.logger.debug(f'Creating matching_key_uti for {self.asset_class}')
                uti = self.data['Counterparty 1 (Reporting counterparty)'].str.cat(
                    self.data['UTI'], na_rep=''
                )
                new_columns['matching_key_uti'] = uti

            # Keep only alphanumeric values in matching key and convert to uppercase
            self.logger.debug('Keeping only alphanumeric values in matching key and converting to uppercase')
            new_columns['matching_key_uti'] = (new_columns['matching_key_uti']
                                               .str.replace(r'[^a-zA-Z0-9]', '', regex=True)
                                               .str.upper())

            self.data = pd.concat([self.data, pd.DataFrame(new_columns)], axis=1)

        except Exception as e:
            print(f"Error generating keys: {e}")
            raise

        return self.data
