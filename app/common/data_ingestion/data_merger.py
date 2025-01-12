import pandas as pd
from common.config.logger_config import get_logger
from common.config.matching_keys_config import get_matching_keys_for_regulator
from common.config.args_config import Config


class DataMerger:
    def __init__(self, df_left, df_right, regulator, asset_class=None, left_prefix='', right_prefix='',
                 use_case_name='default'):
        """
        Initialize DataMerger instance with two dataframes, regulator, and optional asset class.
        Matching keys will be dynamically loaded based on the regulator and asset class.
        """
        self.use_case_name = use_case_name
        self.logger = get_logger(__name__, Config().env.lower(), Config().run_date.lower(),
                                 use_case_name=self.use_case_name)

        self.logger.info(
            f"Initializing DataMerger for {regulator} - {asset_class if asset_class else 'all asset classes'}")
        self.logger.info(f"Input shapes - Left DataFrame: {df_left.shape}, Right DataFrame: {df_right.shape}")

        # Instead of copying entire dataframes, we'll only add prefixes to column names
        self.df_left = df_left.copy()  # Create copy to avoid modifying original
        self.df_right = df_right.copy()  # Create copy to avoid modifying original
        self.left_prefix = left_prefix
        self.right_prefix = right_prefix

        # Store original column names and dtypes
        self.left_columns = df_left.columns
        self.right_columns = df_right.columns

        # Add prefixes to column names without copying data
        self.logger.info(f"Adding column prefixes - Left: '{left_prefix}', Right: '{right_prefix}'")
        self.df_left.columns = [f"{left_prefix}{col}" for col in df_left.columns]
        self.df_right.columns = [f"{right_prefix}{col}" for col in df_right.columns]

        # Get matching keys with prefixes
        self.on_keys_list = [
            (f"{left_prefix}{key[0]}", f"{right_prefix}{key[1]}")
            for key in get_matching_keys_for_regulator(regulator, asset_class)
        ]
        self.logger.info(f"Found {len(self.on_keys_list)} matching key pairs for merging")
        for left_key, right_key in self.on_keys_list:
            self.logger.info(f"Matching key pair: {left_key} <--> {right_key}")

    def _process_matches(self, df_left, df_right, keys):
        """
        Process a single pair of matching keys.
        Returns indices of matched records and the matched data.
        """
        # Perform merge on specific columns only
        left_key, right_key = keys
        merge_result = pd.merge(
            df_left[[left_key]].reset_index(),
            df_right[[right_key]].reset_index(),
            left_on=left_key,
            right_on=right_key,
            how='inner'
        )

        self.logger.info(f"Processing match for keys: {left_key} <--> {right_key}")
        self.logger.info(f"Left records: {len(df_left)}, Right records: {len(df_right)}")

        if not merge_result.empty:
            # Check for duplicates in the merge result
            if merge_result['index_x'].duplicated().any() or merge_result['index_y'].duplicated().any():
                self.logger.warning(f"Found duplicate matches for {left_key} <--> {right_key}")
                self.logger.warning(f"Left duplicates: {merge_result['index_x'].duplicated().sum()}")
                self.logger.warning(f"Right duplicates: {merge_result['index_y'].duplicated().sum()}")
                # Keep first occurrence of duplicates
                merge_result = merge_result.drop_duplicates(subset=['index_x', 'index_y'], keep='first')

            # Get matched records using loc with integer indexing
            matched_left = df_left.iloc[merge_result['index_x']].copy()
            matched_right = df_right.iloc[merge_result['index_y']].copy()

            # Reset indices to ensure they match
            matched_left.reset_index(drop=True, inplace=True)
            matched_right.reset_index(drop=True, inplace=True)

            # Create matched DataFrame efficiently
            matched_data = pd.concat([matched_left, matched_right], axis=1)
            matched_data.insert(len(matched_data.columns), 'matching_flag', ['matched'] * len(matched_data))

            self.logger.info(f'SUCCESS: {left_key} <--> {right_key} || {len(merge_result)} records were matched')
            return merge_result['index_x'].unique(), merge_result['index_y'].unique(), matched_data

        self.logger.info(f'NO MATCHES: {left_key} <--> {right_key} || 0 records were matched')
        return pd.Index([]), pd.Index([]), pd.DataFrame()

    def merge_data(self, return_type='full'):
        """
        Memory-efficient implementation of the merge operation.
        """
        self.logger.info(f"Starting merge operation with return_type='{return_type}'")

        if return_type not in {'left', 'right', 'inner', 'full'}:
            raise ValueError(
                f"Invalid return_type '{return_type}'. Must be one of 'left', 'right', 'inner', or 'full'.")

        # Initialize indices for tracking matched records
        left_matched_indices = pd.Index([])
        right_matched_indices = pd.Index([])
        matched_dfs = []

        # Process each pair of keys
        self.logger.info(f"Starting iterative matching process with {len(self.on_keys_list)} key pairs")
        for iteration, keys in enumerate(self.on_keys_list, 1):
            self.logger.info(f"Processing key pair {iteration}/{len(self.on_keys_list)}")

            # Get unmatched records indices
            left_unmatched_mask = ~self.df_left.index.isin(left_matched_indices)
            right_unmatched_mask = ~self.df_right.index.isin(right_matched_indices)

            unmatched_left_count = left_unmatched_mask.sum()
            unmatched_right_count = right_unmatched_mask.sum()
            self.logger.info(
                f"Remaining unmatched records - Left: {unmatched_left_count}, Right: {unmatched_right_count}")

            if not left_unmatched_mask.any() or not right_unmatched_mask.any():
                self.logger.info("No more unmatched records to process, breaking iteration")
                break

            # Process only unmatched records
            temp_left = self.df_left[left_unmatched_mask].copy()
            temp_right = self.df_right[right_unmatched_mask].copy()

            # Reset indices for temporary dataframes
            temp_left.reset_index(drop=True, inplace=True)
            temp_right.reset_index(drop=True, inplace=True)

            # Process matches for current key pair
            new_left_indices, new_right_indices, matched_df = self._process_matches(temp_left, temp_right, keys)

            if not matched_df.empty:
                matched_dfs.append(matched_df)
                # Update matched indices using the original indices
                left_matched_indices = left_matched_indices.union(
                    self.df_left[left_unmatched_mask].index[new_left_indices])
                right_matched_indices = right_matched_indices.union(
                    self.df_right[right_unmatched_mask].index[new_right_indices])

        # Process unmatched records based on return_type
        self.logger.info("Processing unmatched records")
        result_dfs = []

        if matched_dfs:
            result_dfs.extend(matched_dfs)
            self.logger.info(f"Total matched records: {sum(len(df) for df in matched_dfs)}")

        if return_type in {'left', 'full'}:
            left_unmatched = self.df_left[~self.df_left.index.isin(left_matched_indices)]
            if not left_unmatched.empty:
                self.logger.info(f"Processing {len(left_unmatched)} unmatched left records")
                # Create empty DataFrame with NaN/None values for right columns
                right_empty_data = {
                    f"{self.right_prefix}{col}": pd.Series([None] * len(left_unmatched))
                    for col in self.right_columns
                }
                # Create unmatched DataFrame with empty right columns
                df_unmatched = pd.concat([left_unmatched.reset_index(drop=True),
                                          pd.DataFrame(right_empty_data)], axis=1)
                df_unmatched.insert(len(df_unmatched.columns), 'matching_flag', ['left_only'] * len(df_unmatched))
                result_dfs.append(df_unmatched)
            elif not result_dfs:  # No matches and return_type is 'left'
                self.logger.info(
                    "No matches found and return_type is 'left', returning empty DataFrame with correct columns")
                # Return empty DataFrame with all columns
                return pd.DataFrame(columns=[
                    *[f"{self.left_prefix}{col}" for col in self.left_columns],
                    *[f"{self.right_prefix}{col}" for col in self.right_columns],
                    'matching_flag'
                ])

        if return_type in {'right', 'full'}:
            right_unmatched = self.df_right[~self.df_right.index.isin(right_matched_indices)]
            if not right_unmatched.empty:
                self.logger.info(f"Processing {len(right_unmatched)} unmatched right records")
                right_unmatched = right_unmatched.reset_index(drop=True)
                right_unmatched.insert(len(right_unmatched.columns), 'matching_flag',
                                       ['right_only'] * len(right_unmatched))
                result_dfs.append(right_unmatched)

        # Restore original column names
        self.logger.info("Restoring original column names")
        self.df_left.columns = self.left_columns
        self.df_right.columns = self.right_columns

        # Concatenate results only once at the end
        if not result_dfs:
            self.logger.info("No results to concatenate, returning empty DataFrame")
            return pd.DataFrame(columns=[*self.left_columns, *self.right_columns, 'matching_flag'])

        # result = pd.concat(result_dfs, ignore_index=True)

        if not result_dfs:
            # Create an empty DataFrame with all expected columns
            all_columns = [*self.df_left.columns, *self.df_right.columns, 'matching_flag']
            result = pd.DataFrame(columns=all_columns)
        else:
            result = pd.concat(result_dfs, ignore_index=True)

        self.logger.info(f"Final merged DataFrame shape: {result.shape}")

        total_matched = len(result[result['matching_flag'] == 'matched'])
        total_left_only = len(result[result['matching_flag'] == 'left_only'])
        total_right_only = len(result[result['matching_flag'] == 'right_only'])

        self.logger.info("Matching Summary:")
        self.logger.info(f"Total Records: {len(result)}")
        self.logger.info(f"Matched Records: {total_matched}")
        self.logger.info(f"Unmatched Left Records: {total_left_only}")
        self.logger.info(f"Unmatched Right Records: {total_right_only}")
        self.logger.info(f"Match Rate: {(total_matched / len(result) * 100):.2f}%")

        self.logger.info('Matching logic implementation complete.')
        return result
