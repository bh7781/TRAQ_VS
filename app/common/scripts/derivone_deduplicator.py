import pandas as pd
from common import constants
from common.config.upstream_attribute_mappings import HARMONIZED_UTI_PREFIX
from common.config.upstream_attribute_mappings import HARMONIZED_UTI_VALUE
from common.config.upstream_attribute_mappings import PARTY1_LEI
from common.config.logger_config import get_logger


class DerivOneDeduplicator:
    """
    Class to remove duplicate trades from DerivOne data based on a deduplication key.
    """

    def __init__(self, data, asset_class, environment, report_date, use_case, log_to_file=True):
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be a pandas DataFrame.")

        self.data = data
        self.asset_class = asset_class
        self.logger = get_logger(name=__name__, env=environment, date=report_date, use_case_name=use_case,
                                 log_to_file=log_to_file)
        self.huti_prefix = HARMONIZED_UTI_PREFIX.get(self.asset_class)
        self.huti_value = HARMONIZED_UTI_VALUE.get(self.asset_class)

    def create_deduplication_key(self):
        """
        Creates the 'deduplication_key' column.
        Works with string operations first, then converts to categorical at the end.
        """
        # Pre-allocate a Series for deduplication keys with the same index as the data
        dedup_keys = pd.Series(index=self.data.index, dtype='object')

        # Process columns in chunks to reduce peak memory usage
        chunk_size = 100000
        total_rows = len(self.data)

        for start_idx in range(0, total_rows, chunk_size):
            end_idx = min(start_idx + chunk_size, total_rows)
            chunk = self.data.iloc[start_idx:end_idx]
            chunk_idx = chunk.index

            huti_prefixes = chunk[self.huti_prefix].astype('string').fillna('').str.strip()
            uti_prefixes = chunk['UTI Prefix'].astype('string').fillna('').str.strip()
            usi_prefixes = chunk['USI Prefix'].astype('string').fillna('').str.strip()

            # Convert to strings and handle nulls
            huti_values = chunk[self.huti_value].astype('string').fillna('').str.strip()
            uti_values = chunk['UTI Value'].astype('string').fillna('').str.strip()
            usi_values = chunk['USI Value'].astype('string').fillna('').str.strip()

            if self.asset_class == constants.EQUITY_DERIVATIVES:
                # Create the combined key
                combined_key = (
                        huti_prefixes +
                        huti_values +
                        uti_prefixes +
                        uti_values +
                        usi_prefixes +
                        usi_values
                )

                # If everything ends up empty, assign a placeholder
                mask_empty = combined_key == ''
                if mask_empty.any():
                    missing_indices = mask_empty[mask_empty].index
                    placeholders = [f'missing_placeholder{i}' for i in range(start_idx + 1, start_idx + len(missing_indices) + 1)]
                    combined_key[missing_indices] = placeholders

                dedup_keys[chunk_idx] = combined_key
                del combined_key, huti_prefixes, uti_prefixes, usi_prefixes

            else:
                # Get LEI based on asset class
                if self.asset_class == constants.EQUITY_SWAPS:
                    lei = chunk['party1_lei_derived'].astype('string').fillna('').str.strip()
                else:
                    lei = chunk[PARTY1_LEI.get(self.asset_class)].astype('string').fillna('').str.strip()

                # Initialize chunk_key as empty Series
                chunk_key = pd.Series('', index=chunk.index)

                # Apply the prioritization logic
                # 1. If HUTI value is populated - Treat '' or 'NOHUTIPROVIDED' (case-insensitive) as empty HUTI
                # huti_is_empty = ((huti_values == '') |
                #                  (huti_values.str.contains('NOHUTIPROVIDED', case=False, na=False)) |
                #                  (huti_prefixes.str.contains('NOHUTIPROVIDED', case=False, na=False)))
                huti_is_empty = (huti_values == '') | (huti_values.str.upper() == 'NOHUTIPROVIDED') | (huti_prefixes.str.upper() == 'NOHUTIPROVIDED')
                huti_mask = ~huti_is_empty
                chunk_key[huti_mask] = lei[huti_mask] + huti_prefixes[huti_mask] + huti_values[huti_mask]

                # 2. If HUTI is blank but USI is populated
                usi_mask = huti_is_empty & (usi_values != '')
                chunk_key[usi_mask] = lei[usi_mask] + usi_prefixes[usi_mask] + usi_values[usi_mask]

                # 3. If both HUTI and USI are blank, use UTI
                uti_mask = huti_is_empty & (usi_values == '')
                chunk_key[uti_mask] = lei[uti_mask] + uti_prefixes[uti_mask] + uti_values[uti_mask]

                # Handle completely empty cases
                mask_empty = chunk_key == ''
                if mask_empty.any():
                    missing_indices = mask_empty[mask_empty].index
                    placeholders = [f'missing_placeholder{i}' for i in
                                    range(start_idx + 1, start_idx + len(missing_indices) + 1)]
                    chunk_key[missing_indices] = placeholders

                dedup_keys[chunk_idx] = chunk_key
                del chunk_key, lei

            # Clean up temporary variables
            del chunk

        # Create new column all at once and convert to categorical
        # Using a temporary DataFrame to avoid fragmentation
        temp_df = pd.DataFrame({'deduplication_key': dedup_keys}, index=self.data.index)
        self.data = pd.concat([self.data, temp_df], axis=1)

        # Clean up
        del dedup_keys, temp_df

        # Convert to categorical
        self.data['deduplication_key'] = self.data['deduplication_key'].astype('category')

    def remove_duplicates(self):
        """
        Removes duplicate trades with minimal memory overhead.
        """
        if 'deduplication_key' not in self.data.columns:
            self.create_deduplication_key()

        self.logger.debug('Removing duplicates...')

        # Get unique indices efficiently
        unique_indices = (
            self.data.reset_index()
            .groupby('deduplication_key', observed=True)['index']
            .first()
            .values
        )

        # Use boolean indexing instead of drop_duplicates
        self.data = self.data.iloc[unique_indices]
        self.data.reset_index(drop=True, inplace=True)

        # Clean up
        # self.data.drop(columns=['deduplication_key'], inplace=True)

        self.data['deduplication_key'] = self.data['deduplication_key'].astype(str)

        return self.data

    def run(self):
        """
        Executes the deduplication process and returns the deduplicated data.
        """
        return self.remove_duplicates()
