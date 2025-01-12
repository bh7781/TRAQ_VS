"""
This module provides the FilePathConfig class, which constructs file paths for TSR and DerivOne files
based on the provided run date. It supports different regimes and asset classes and adjusts file paths
according to the operating system.
"""

import os
import glob
import sys
from datetime import datetime

from common import constants
from common.utility import adjust_path_for_os
from common.utility import get_business_day_offset


class FilePathConfig:
    """
    A class to configure and retrieve file paths for TSR and DerivOne files.
    """

    # Regimes and their respective configurations
    REGIMES_CONFIG = {
        constants.EMIR_REFIT: {
            'subfolders': ['ESMA', 'FCA'],
            'tsr_file_pattern': 'sFTP_{prefix}_EOD_Trade_State_Report_*_{report_date}.*_{msa_tms_code}*.csv',
            'tar_file_pattern': 'sFTP_{prefix}_EOD_Trade_Activity_Report_*_{report_date}.*_{msa_tms_code}*.csv',
            'collateral_file_pattern': 'sFTP_{prefix}_EOD_Margin_State_Report_*_{report_date}.*.csv',
            'prefixes': {
                'ESMA': 'EUEMIR',
                'FCA': 'UKEMIR',
            },
            'date_format': None,
        },

        constants.JFSA: {
            'subfolders': None,
            'tsr_file_pattern': 'sFTP_JFSA_EOD_Trade_State_Report_*-{report_date}.*_{msa_tms_code}*.csv',
            'collateral_file_pattern': 'sFTP_JFSA_EOD_Margin_State_Report_*-{report_date}.*.csv',
            'date_format': None,
        },

        constants.ASIC: {
            'subfolders': None,
            'tsr_file_pattern': 'sFTP_ASIC_EOD_Trade_State_Report_*-{report_date}.*_{msa_tms_code}*.csv',
            'collateral_file_pattern': 'sFTP_ASIC_EOD_Margin_State_Report_*-{report_date}.*.csv',
            'date_format': None,
        },

        constants.MAS: {
            'subfolders': None,
            'tsr_file_pattern': 'sFTP_MAS_EOD_Trade_State_Report_*-{report_date}.*_{msa_tms_code}*.csv',
            'collateral_file_pattern': 'sFTP_MAS_EOD_Margin_State_Report_*-{report_date}.*.csv',
            'date_format': None,
        },
    }

    def __init__(self, run_date, env, logger_obj=None):
        """
        Initializes the FilePathConfig with the provided run date.

        Parameters:
        run_date (str): The run date in 'YYYY-MM-DD' format.
        """
        self.run_date = run_date
        if logger_obj:
            self.logger = logger_obj
        self.env = env.lower()

        # Base directory where all regimes TSRs are located
        self.tsr_base_directory = f'/v/region/eu/appl/gtr/traq/data/{self.env}/input/tsr'
        self.tar_base_directory = f'/v/region/eu/appl/gtr/traq/data/{self.env}/input/tar'
        self.collateral_base_directory = f'/v/region/eu/appl/gtr/traq/data/{self.env}/input/collateral'

        # Adjusts path based on the operating system
        self.tsr_base_directory = adjust_path_for_os(self.tsr_base_directory)
        self.tar_base_directory = adjust_path_for_os(self.tar_base_directory)
        self.collateral_base_directory = adjust_path_for_os(self.collateral_base_directory)

    @staticmethod
    def report_date_to_filename(report_date, date_format):
        """
        Converts report date from 'YYYY-MM-DD' to the specified date format.

        Parameters:
        report_date (str): The report date in 'YYYY-MM-DD' format.
        date_format (str): The date format to convert to.

        Returns:
        str: The report date in the specified format.
        """
        if not date_format:
            return report_date
        dt = datetime.strptime(report_date, '%Y-%m-%d')
        return dt.strftime(date_format)

    def construct_file_pattern(self, template, report_date, date_format, asset_class, msa_tms_code, prefix=''):
        """
        Constructs the file pattern by formatting the template with the provided variables.

        Parameters:
        template (str): The file name template.
        report_date (str): The report date in 'YYYY-MM-DD' format.
        date_format (str): The date format to use in the filename.
        asset_class (str): The asset class code.
        msa_tms_code (str): The MSA code for the asset class.
        prefix (str): The prefix to use in the filename (if applicable).

        Returns:
        str: The constructed file pattern.
        """
        date_part = self.report_date_to_filename(report_date, date_format)
        file_pattern = template.format(
            prefix=prefix,
            report_date=report_date,
            msa_tms_code=msa_tms_code,
            asset_class=asset_class,
            asset_class_lower=asset_class.lower(),
            date_part=date_part
        )
        return file_pattern

    def get_tsr_files_for_regime(self, regime, asset_classes, report_date=None):
        """
        Finds TSR files for the specified regime and asset classes for the given report date.

        Parameters:
        regime (str): The regime to process (e.g., 'JFSA', 'EMIR_REFIT', etc.)
        asset_classes (str or list): Asset class or list of asset classes specific to the regime.
        report_date (str): The report date in 'YYYY-MM-DD' format. Defaults to self.run_date.

        Returns:
        dict: Dictionary mapping asset classes to lists of matching file paths.
        """
        if report_date is None:
            report_date = self.run_date

        # Convert asset_classes to a list if it's a string
        if isinstance(asset_classes, str):
            asset_classes = [asset_classes]

        # Keep track of which original asset classes map to 'EQ'
        eq_asset_classes = [ac for ac in asset_classes if ac in ['EQD', 'EQS']]

        # Create mapping for processing
        processing_asset_classes = ['EQ' if ac in ['EQD', 'EQS'] else ac for ac in asset_classes]
        # Remove duplicates while preserving order
        processing_asset_classes = list(dict.fromkeys(processing_asset_classes))

        # Get the regime configuration
        regime_info = self.REGIMES_CONFIG.get(regime)
        if not regime_info:
            self.logger.exception(f"Regime '{regime}' not recognized.")
            return {}

        files_found = {}

        try:
            # Process subfolders or top-level directory for asset classes
            if regime_info.get('subfolders'):
                self._process_subfolders(regime_info, regime, processing_asset_classes, report_date, files_found)
            else:
                self._process_asset_classes(regime_info, regime, processing_asset_classes, report_date, files_found)

            # Handle EQD and EQS separately
            if 'EQ' in files_found and eq_asset_classes:
                eq_files = files_found.pop('EQ')  # Remove 'EQ' entry
                # Create separate lists for each equity asset class
                for asset_class in eq_asset_classes:
                    files_found[asset_class] = list(eq_files)  # Create a new list for each asset class

        except Exception as e:
            self.logger.exception(f"Error occurred while processing TSR files for regime {regime}: {str(e)}")

        return files_found

    def _process_subfolders(self, regime_info, regime, asset_classes, report_date, files_found):
        """
        Process asset classes for regimes with subfolders.
        """
        subfolders = regime_info.get('subfolders')
        for subfolder in subfolders:
            prefix = regime_info.get('prefixes', {}).get(subfolder, '')

            # Adjust report date
            if regime == constants.EMIR_REFIT and subfolder == 'FCA':
                report_date_for_subfolder = get_business_day_offset(report_date, -1)  # Previous business day
            else:
                report_date_for_subfolder = report_date

            for asset_class in asset_classes:
                if asset_class.upper() == 'COL':
                    self._fetch_collateral_files(regime_info, regime, subfolder, asset_class, report_date_for_subfolder, files_found, prefix)
                else:
                    self._fetch_tsr_files(
                        regime_info, regime, subfolder, asset_class, report_date_for_subfolder, prefix, files_found)

    def _process_asset_classes(self, regime_info, regime, asset_classes, report_date, files_found):
        """
        Process asset classes for regimes without subfolders.
        """
        for asset_class in asset_classes:
            if asset_class.upper() == constants.COLLATERAL:
                self._fetch_collateral_files(regime_info, regime, None, asset_class, report_date, files_found)
            else:
                self._fetch_tsr_files(regime_info, regime, None, asset_class, report_date, '', files_found)

    def _fetch_tsr_files(self, regime_info, regime, subfolder, asset_class, report_date, prefix, files_found):
        """
        Fetch TSR or TAR files for a given asset class and subfolder.
        """
        msa_tms_code = None
        if asset_class not in [constants.COLLATERAL]:
            msa_tms_code = constants.ASSET_CLASS_MSA_TMS_CODES.get(asset_class)
            if msa_tms_code is None:
                error_msg = f"Asset class '{asset_class}' MSA code not found in configuration"
                self.logger.error(error_msg)
                self.logger.error("Terminating program execution.")
                sys.exit(1)

        # Determine if we should use TSR or TAR base directory and pattern
        if regime == constants.EMIR_REFIT and asset_class.upper() == 'ETDACTIVITY':
            base_directory = self.tar_base_directory
            pattern_template = regime_info.get('tar_file_pattern')
        else:
            base_directory = self.tsr_base_directory
            pattern_template = regime_info.get('tsr_file_pattern')

        # Construct the directory path
        dir_path = os.path.join(base_directory, regime, subfolder or '', 'ETD' if asset_class.upper() in ['ETDPOSITION', 'ETDACTIVITY'] else asset_class)
        dir_path = adjust_path_for_os(dir_path)

        # Check if the directory exists
        if not os.path.exists(dir_path):
            error_msg = f"TSR base directory path does not exist for asset class {asset_class}: {dir_path}"
            self.logger.error(error_msg)
            self.logger.error("Terminating program execution.")
            sys.exit(1)

        # Construct the file pattern
        file_pattern = self.construct_file_pattern(
            pattern_template,
            report_date,
            regime_info.get('date_format'),
            asset_class,
            msa_tms_code,
            prefix
        )

        # Construct the full glob pattern
        full_glob_pattern = os.path.join(dir_path, file_pattern)
        # self.logger.info(f"Searching for TSR files - Directory: {dir_path}, Pattern: {file_pattern}")

        # Find matching files
        matching_files = glob.glob(full_glob_pattern)
        if not matching_files:
            self.logger.error(f'No TSR files found for asset class {asset_class}')
            self.logger.error(f'Directory {dir_path}')
            self.logger.error(f'File Pattern {file_pattern}')
            self.logger.error(f'Full Path Pattern:  {full_glob_pattern}')

        # Save the matching files
        if asset_class not in files_found:
            files_found[asset_class] = []
        files_found[asset_class].extend(matching_files)

    def _fetch_collateral_files(self, regime_info, regime, subfolder, asset_class, report_date, files_found, prefix=''):
        """
        Fetch collateral files for a given regime.
        """
        dir_path = os.path.join(self.collateral_base_directory, regime, subfolder or '')
        dir_path = adjust_path_for_os(dir_path)

        # Check if the directory exists
        if not os.path.exists(dir_path):
            error_msg = f"Collateral base directory path does not exist for regime {regime}: {dir_path}"
            self.logger.error(error_msg)
            self.logger.error("Terminating program execution.")
            sys.exit(1)

        # Construct the file pattern for collateral files
        collateral_file_pattern = regime_info.get('collateral_file_pattern')
        if not collateral_file_pattern:
            error_msg = f"No collateral file pattern configured for regime '{regime}'"
            self.logger.error(error_msg)
            self.logger.error("Terminating program execution.")
            sys.exit(1)

        # Retrieve msa_tms_code for COLLATERAL as well, if needed by pattern
        msa_tms_code = None
        if asset_class not in [constants.COLLATERAL]:
            msa_tms_code = constants.ASSET_CLASS_MSA_TMS_CODES.get(asset_class)
            if msa_tms_code is None:
                error_msg = f"Asset class '{asset_class}' MSA code not found in configuration"
                self.logger.error(error_msg)
                self.logger.error("Terminating program execution.")
                sys.exit(1)
        else:
            # If collateral pattern requires msa_tms_code, provide a default or fetch as needed.
            # If a specific MSA code is not required for collateral, you can assign a default value like empty string.
            msa_tms_code = ''

        file_pattern = collateral_file_pattern.format(prefix=prefix, report_date=report_date, msa_tms_code=msa_tms_code)
        full_glob_pattern = os.path.join(dir_path, file_pattern)

        # Find matching files
        matching_files = glob.glob(full_glob_pattern)
        if not matching_files:
            self.logger.error(f'No Collateral files found for regime {regime}')
            self.logger.error(f'Directory {dir_path}')
            self.logger.error(f'File Pattern {file_pattern}')
            self.logger.error(f'Full Path Pattern:  {full_glob_pattern}')

        # Save the matching files
        if asset_class not in files_found:
            files_found[asset_class] = []
        files_found[asset_class].extend(matching_files)

    def get_derivone_filepaths(self, report_date):
        """
        Constructs file paths for DerivOne files based on the provided report date.

        Parameters:
        report_date (str): The report date in 'YYYY-MM-DD' format.

        Returns:
        dict: Dictionary mapping asset classes to lists of file paths.
        """
        report_date_yy_mm_dd = str(report_date)
        report_date_yymmdd = str(report_date).replace('-', '')

        try:
            # Define base directories for different components
            deriv1_base = adjust_path_for_os(f"/v/region/eu/appl/gtr/traq/data/{self.env}/input/Deriv1")
            ginger_base = adjust_path_for_os(f"/v/region/eu/appl/gtr/traq/data/{self.env}/input/GINGER")
            fred_base = adjust_path_for_os(f"/v/region/eu/appl/gtr/traq/data/{self.env}/input/FRED")

            # Validate base directories exist with specific messages for each
            base_dirs = {
                'DerivOne': deriv1_base,
                'GINGER': ginger_base,
                'FRED': fred_base
            }

            for source, base_dir in base_dirs.items():
                if not os.path.exists(base_dir):
                    error_msg = f"{source} base directory does not exist: {base_dir}"
                    self.logger.error(error_msg)
                    self.logger.error("Terminating program execution.")
                    sys.exit(1)

            derivone_filepaths = {
                constants.COMMODITY: [
                    adjust_path_for_os(f"{deriv1_base}/CO/imrecon_com_eod_prod_{report_date_yymmdd}.csv")],

                constants.CREDIT: [
                    adjust_path_for_os(f"{deriv1_base}/CR/imrecon_crd_ny_eod_CR_prod_{report_date_yymmdd}.csv"),
                    adjust_path_for_os(f"{deriv1_base}/CR/imrecon_crd_ln_eod_CR_prod_{report_date_yymmdd}.csv"),
                    adjust_path_for_os(f"{deriv1_base}/CR/imrecon_crd_ap_eod_CR_prod_{report_date_yymmdd}.csv")],

                constants.EQUITY_DERIVATIVES: [
                    adjust_path_for_os(f"{ginger_base}/EQD/dfa_eq_ds_prod_{report_date_yy_mm_dd}_*.csv"),
                    adjust_path_for_os(f"{ginger_base}/EQD/dfa_eq_ex_prod_{report_date_yy_mm_dd}_*.csv"),
                    adjust_path_for_os(f"{ginger_base}/EQD/dfa_eq_op_prod_{report_date_yy_mm_dd}_*.csv"),
                    adjust_path_for_os(f"{ginger_base}/EQD/dfa_eq_vs_prod_{report_date_yy_mm_dd}_*.csv")],

                constants.EQUITY_SWAPS: [
                    adjust_path_for_os(f"{fred_base}/EQS/dfa_eq_es_prod_{report_date_yy_mm_dd}_*_ny.csv"),
                    adjust_path_for_os(f"{fred_base}/EQS/dfa_eq_es_prod_{report_date_yy_mm_dd}_*_ln.csv"),
                    adjust_path_for_os(f"{fred_base}/EQS/dfa_eq_es_prod_{report_date_yy_mm_dd}_*_hk.csv")],

                constants.FOREIGN_EXCHANGE: [
                    adjust_path_for_os(f"{deriv1_base}/FX/imrecon_fx_eod_prod_{report_date_yymmdd}.csv")],

                constants.INTEREST_RATES: [
                    adjust_path_for_os(f"{deriv1_base}/IR/imrecon_ird_ny_eod_prod_{report_date_yymmdd}.csv"),
                    adjust_path_for_os(f"{deriv1_base}/IR/imrecon_ird_ln_eod_prod_{report_date_yymmdd}.csv"),
                    adjust_path_for_os(f"{deriv1_base}/IR/imrecon_ird_ap_eod_prod_{report_date_yymmdd}.csv")]
            }

            # Apply globbing for EQD and EQS file paths
            for key in [constants.EQUITY_DERIVATIVES, constants.EQUITY_SWAPS]:
                file_paths = []
                for path_pattern in derivone_filepaths[key]:
                    # self.logger.info(f"Searching for {key} files - Pattern: {path_pattern}")
                    matched_files = glob.glob(path_pattern)
                    if not matched_files:
                        self.logger.error(f'No DerivOne files found for {key}')
                        self.logger.error(f'Directory: {os.path.dirname(path_pattern)}')
                        self.logger.error(f'Pattern: {os.path.basename(path_pattern)}')
                    file_paths.extend(matched_files)
                derivone_filepaths[key] = file_paths

            # For non-glob paths, verify file existence
            for asset_class, paths in derivone_filepaths.items():
                if asset_class not in [constants.EQUITY_DERIVATIVES, constants.EQUITY_SWAPS]:
                    for path in paths:
                        if '*' not in path and not os.path.exists(path):
                            self.logger.error(f'DerivOne file not found for {asset_class}')
                            self.logger.error(f'Directory: {os.path.dirname(path)}')
                            self.logger.error(f'File: {os.path.basename(path)}')
                            self.logger.error(f'Full Path: {path}')

            return derivone_filepaths

        except Exception as e:
            error_msg = f"Error occurred while getting DerivOne file paths: {str(e)}"
            self.logger.error(error_msg)
            self.logger.error("Terminating program execution.")
            sys.exit(1)

    def get_preprocessed_derivone_filepaths(self, report_date):
        """
        Constructs file paths for Pre-processed DerivOne files based on the provided report date.
        Pre-processing includes:
        1. Deduplication based on deduplication key defined in common/scripts/derivone_deduplicator.py
        2. Matching key creation using common/key_generation/derivone_key_generator.py
        """
        report_date_yymmdd = str(report_date).replace('-', '')

        try:
            # Define base directories for different components
            # deriv1_base = adjust_path_for_os(f"/v/region/eu/appl/gtr/traq/data/{self.env}/input/Deriv1/pre_processed")
            # ginger_base = adjust_path_for_os(f"/v/region/eu/appl/gtr/traq/data/{self.env}/input/Deriv1/pre_processed")
            # fred_base = adjust_path_for_os(f"/v/region/eu/appl/gtr/traq/data/{self.env}/input/Deriv1/pre_processed")

            # Define base directories for different components
            deriv1_base = adjust_path_for_os(rf"C:\Users\{os.getlogin()}\Morgan Stanley\Tech & TRAQ Automation - Diagnostic Testing\input\Deriv1\pre_processed")
            ginger_base = adjust_path_for_os(rf"C:\Users\{os.getlogin()}\Morgan Stanley\Tech & TRAQ Automation - Diagnostic Testing\input\Deriv1\pre_processed")
            fred_base = adjust_path_for_os(rf"C:\Users\{os.getlogin()}\Morgan Stanley\Tech & TRAQ Automation - Diagnostic Testing\input\Deriv1\pre_processed")

            # Validate base directories exist with specific messages for each
            base_dirs = {
                'DerivOne': deriv1_base,
                'GINGER': ginger_base,
                'FRED': fred_base
            }

            for source, base_dir in base_dirs.items():
                if not os.path.exists(base_dir):
                    error_msg = f"{source} base directory does not exist: {base_dir}"
                    self.logger.error(error_msg)
                    self.logger.error("Terminating program execution.")
                    sys.exit(1)

            derivone_filepaths = {
                constants.COMMODITY: [adjust_path_for_os(f"{deriv1_base}/CO/derivone_CO_preprocessed_{report_date_yymmdd}.csv")],

                constants.CREDIT: [adjust_path_for_os(f"{deriv1_base}/CR/derivone_CR_preprocessed_{report_date_yymmdd}.csv")],

                constants.EQUITY_DERIVATIVES: [adjust_path_for_os(f"{ginger_base}/EQD/ginger_EQD_preprocessed_{report_date_yymmdd}.csv")],

                constants.EQUITY_SWAPS: [adjust_path_for_os(f"{fred_base}/EQS/fred_EQS_preprocessed_{report_date_yymmdd}.csv")],

                constants.FOREIGN_EXCHANGE: [adjust_path_for_os(f"{deriv1_base}/FX/derivone_FX_preprocessed_{report_date_yymmdd}.csv")],

                constants.INTEREST_RATES: [adjust_path_for_os(f"{deriv1_base}/IR/derivone_IR_preprocessed_{report_date_yymmdd}.csv")]
            }

            # For non-glob paths, verify file existence
            for asset_class, paths in derivone_filepaths.items():
                if asset_class not in [constants.EQUITY_DERIVATIVES, constants.EQUITY_SWAPS]:
                    for path in paths:
                        if '*' not in path and not os.path.exists(path):
                            self.logger.error(f'DerivOne file not found for {asset_class}')
                            self.logger.error(f'Directory: {os.path.dirname(path)}')
                            self.logger.error(f'File: {os.path.basename(path)}')
                            self.logger.error(f'Full Path: {path}')

            return derivone_filepaths

        except Exception as e:
            error_msg = f"Error occurred while getting DerivOne file paths: {str(e)}"
            self.logger.error(error_msg)
            self.logger.error("Terminating program execution.")
            sys.exit(1)
