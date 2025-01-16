"""
This module generates matching keys in DerivOne files based on specified business logic.

The matching keys are generated using combinations of various identifiers such as USI, UTI,
and Harmonized UTI, along with their prefixes and Party1 LEI where applicable.

The code is optimized for performance and memory efficiency on large datasets.
"""

import pandas as pd
import numpy as np
from common.config import upstream_attribute_mappings
from common.config.ms_entity_mappings import company_code_lei_mapping
from common import constants
from common.config.logger_config import get_logger


class DerivOneKeyGenerator:
   """
   A class to generate matching keys in DerivOne data based on business logic.
   """

   def __init__(self, data, asset_class, environment, report_date, use_case, log_to_file=True):
       """
       Initialize the DerivOneKeyGenerator with a DataFrame.

       Args:
           data (pd.DataFrame): Input DataFrame containing DerivOne data
           asset_class (str): Asset class of the data
           environment (str): Environment name for logging
           report_date (str): Report date for logging
           use_case (str): Use case name for logging
           log_to_file (bool, optional): Whether to log to file. Defaults to True.
       """
       self.logger = get_logger(name=__name__, env=environment, date=report_date, use_case_name=use_case, log_to_file=log_to_file)
       if not isinstance(data, pd.DataFrame):
           raise ValueError("Input data must be a pandas DataFrame.")

       self.asset_class = asset_class

       # Get the column names for HUTI prefix and value based on asset class
       self.huti_prefix_col = upstream_attribute_mappings.HARMONIZED_UTI_PREFIX.get(self.asset_class)
       self.huti_value_col = upstream_attribute_mappings.HARMONIZED_UTI_VALUE.get(self.asset_class)

       # Define required columns
       self.required_columns = ['USI Prefix', 'USI Value', 'UTI Prefix', 'UTI Value',
                              self.huti_prefix_col, self.huti_value_col]

       # For EQS, we need BookingEntity column
       if self.asset_class == constants.EQUITY_SWAPS:
           self.required_columns.append('BookingEntity')
           self.party1_lei_col = None
       elif self.asset_class != constants.EQUITY_DERIVATIVES:
           # For other asset classes (except EQD), 'Party1 LEI' is required
           self.party1_lei_col = upstream_attribute_mappings.PARTY1_LEI.get(self.asset_class)
           self.required_columns.append(self.party1_lei_col)
       else:
           self.party1_lei_col = None

       # Keep full data for final output, but ensure required columns exist
       self.data = data
       self.validate_columns()
       self.clean_columns()

   def validate_columns(self):
       """
       Validate that the DataFrame contains all required columns.
       Raises KeyError if any required column is missing.
       """
       self.logger.debug('Checking if required columns are present in DerivOne report')
       missing_columns = [col for col in self.required_columns if col not in self.data.columns]
       if missing_columns:
           raise KeyError(f"Missing required column(s): {', '.join(missing_columns)}")

   def clean_columns(self):
       """
       Clean the values in the required columns by removing NaNs, stripping spaces,
       and converting everything to uppercase.
       """
       try:
           # Cleaning columns
           self.logger.debug('Cleaning the values in the required columns.')
           for col in self.required_columns:
               self.data[col] = self.data[col].fillna('').astype(str).str.strip().str.upper()
       except Exception as e:
           self.logger.error(f"Error cleaning columns: {e}")
           raise

   def generate_keys(self):
       """
       Generate matching keys based on business logic.
       Returns:
           pd.DataFrame: DataFrame with additional matching key columns
       """
       try:
           # Define the regex pattern to remove non-alphanumeric characters
           pattern = r'[^A-Z0-9]'

           # Dictionary to store new columns
           new_columns = {}

           if self.asset_class == constants.EQUITY_SWAPS:
               # For Equity Swaps
               self.logger.debug('Creating matching keys for Equity Swaps')
               
               # Create ms_entity_lei column using the mapping
               ms_entity_lei = self.data['BookingEntity'].map(company_code_lei_mapping)
               
               # Find and log any new company codes not in the mapping
               new_company_codes = set(self.data[self.data['BookingEntity'].map(company_code_lei_mapping).isna()]['BookingEntity'].unique())
               if new_company_codes:
                   self.logger.warning(f"Found {len(new_company_codes)} new company codes not present in mapping: {sorted(new_company_codes)}")
                   print(f"WARNING: Found new company codes not present in mapping: {sorted(new_company_codes)}")
               
               # Fill NaN values with empty string for missing mappings
               ms_entity_lei = ms_entity_lei.fillna('')
               
               # Generate keys with ms_entity_lei
               new_columns['ms_entity_lei'] = ms_entity_lei
               new_columns['matching_key_usi'] = ms_entity_lei.str.cat(self.data['USI Prefix'], na_rep='').str.cat(self.data['USI Value'], na_rep='')
               new_columns['matching_key_uti'] = ms_entity_lei.str.cat(self.data['UTI Prefix'], na_rep='').str.cat(self.data['UTI Value'], na_rep='')
               new_columns['matching_key_huti'] = ms_entity_lei.str.cat(self.data[self.huti_prefix_col], na_rep='').str.cat(self.data[self.huti_value_col], na_rep='')

               new_columns['matching_key_usi_value'] = ms_entity_lei.str.cat(self.data['USI Value'], na_rep='')
               new_columns['matching_key_uti_value'] = ms_entity_lei.str.cat(self.data['UTI Value'], na_rep='')

           elif self.asset_class == constants.EQUITY_DERIVATIVES:
               # For Equity Derivatives
               self.logger.debug('Creating matching keys for Equity Derivatives')
               
               new_columns['matching_key_usi'] = self.data['USI Prefix'].str.cat(self.data['USI Value'], na_rep='')
               new_columns['matching_key_uti'] = self.data['UTI Prefix'].str.cat(self.data['UTI Value'], na_rep='')
               new_columns['matching_key_huti'] = self.data[self.huti_prefix_col].str.cat(self.data[self.huti_value_col], na_rep='')

               new_columns['matching_key_usi_value'] = self.data['USI Value']
               new_columns['matching_key_uti_value'] = self.data['UTI Value']

           else:
               # For other asset classes, include Party1 LEI in the keys
               self.logger.debug(f'Creating matching keys for {self.asset_class}')
               party1_lei = self.data[self.party1_lei_col]

               new_columns['matching_key_usi'] = party1_lei.str.cat(self.data['USI Prefix'], na_rep='').str.cat(self.data['USI Value'], na_rep='')
               new_columns['matching_key_uti'] = party1_lei.str.cat(self.data['UTI Prefix'], na_rep='').str.cat(self.data['UTI Value'], na_rep='')
               new_columns['matching_key_huti'] = party1_lei.str.cat(self.data[self.huti_prefix_col], na_rep='').str.cat(self.data[self.huti_value_col], na_rep='')

               new_columns['matching_key_usi_value'] = party1_lei.str.cat(self.data['USI Value'], na_rep='')
               new_columns['matching_key_uti_value'] = party1_lei.str.cat(self.data['UTI Value'], na_rep='')

               # Additional logic for INTEREST_RATES
               if self.asset_class == constants.INTEREST_RATES:
                   # Determine direction suffix ("P" or "R")
                   direction_suffix = np.where(
                       self.data['Direction'].str.contains('PAY', case=False, na=False), 'P',
                       np.where(self.data['Direction'].str.contains('REC', case=False, na=False), 'R', '')
                   )

                   # Create the three new keys with direction
                   new_columns['matching_key_huti_dir'] = party1_lei.str.cat(self.data[self.huti_prefix_col], na_rep='').str.cat(self.data[self.huti_value_col], na_rep='') + direction_suffix
                   new_columns['matching_key_uti_dir'] = party1_lei.str.cat(self.data['UTI Prefix'], na_rep='').str.cat(self.data['UTI Value'], na_rep='') + direction_suffix
                   new_columns['matching_key_usi_dir'] = party1_lei.str.cat(self.data['USI Prefix'], na_rep='').str.cat(self.data['USI Value'], na_rep='') + direction_suffix

           # Remove non-alphanumeric characters and convert to uppercase for all new columns
           self.logger.debug('Removing non-alphanumeric characters and converting to uppercase from keys')
           for key in new_columns:
               new_columns[key] = new_columns[key].str.replace(pattern, '', regex=True).str.upper()

           # Concatenate all new columns to the DataFrame at once
           self.data = pd.concat([self.data, pd.DataFrame(new_columns)], axis=1)
           del new_columns

       except Exception as e:
           self.logger.error(f"Error generating keys: {e}")
           raise

       self.logger.debug('Key creation is complete.')
       return self.data
    