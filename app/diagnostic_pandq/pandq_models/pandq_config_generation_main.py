"""
This script serves as an independent entry point for generating PANDQ model metadata CSV files.
It generates the following configuration CSV files:
  - files.csv
  - filedqconfig.csv
  - filecolumns.csv
  - models.csv

Usage:
    python pandq_config_generation_main.py --env PROD --regime EMIR_REFIT
"""

import time
import argparse
import sys
from common.config.logger_config import get_logger
from model_generator_facade import ModelGeneratorFacade
from common.config.args_config import Config
from common import utility
from model_configurations import MODEL_CONFIGURATIONS  # Imported for consistency

def main():
    """
    Main function to parse command-line arguments, initialize global configuration,
    and trigger model metadata CSV generation.
    Exceptions are caught and logged to ensure the process exits gracefully with status code 1.
    """
    # Parse command-line arguments
    try:
        parser = argparse.ArgumentParser(
            description="Generate model metadata CSV files based on a given regime."
        )
        parser.add_argument("--env", required=True, help="Environment name (e.g., PROD, QA, DEV)")
        parser.add_argument("--regime", required=True, help="Regime name (e.g., EMIR_REFIT, ASIC, MAS, JFSA, COMMON)")
        args = parser.parse_args()
    except Exception as _:
        logger.error("Error parsing command-line arguments.", exc_info=True)
        sys.exit(1)

    # Sanitize the command-line arguments using utility functions.
    try:
        env = utility.sanitize_env(args.env)
        regime = utility.sanitize_regime(args.regime)
    except Exception as _:
        logger.error("Error sanitizing command-line arguments.", exc_info=True)
        sys.exit(1)

    # Initialize the global configuration object.
    try:
        # Note: run_date can be set to None if not used; it should be set appropriately if needed.
        Config(env=env, regime=regime, run_date=None, use_case_name=use_case_name)
        logger.info(f'ENVIRONMENT = {env.upper()}')
        logger.info(f'REGIME = {regime.upper()}')
    except Exception as _:
        logger.error("Error initializing global configuration.", exc_info=True)
        sys.exit(1)

    # Instantiate the model generator facade and generate the metadata CSV files.
    try:
        generator = ModelGeneratorFacade(use_case_name=use_case_name, logger=logger)
        generator.generate_model_files()
    except Exception as _:
        logger.error("Error during model metadata CSV generation.", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    # Define the use case name for logging and configuration.
    use_case_name = 'model_metadata_generator'
    
    # Initialize the common logger instance.
    # Here, file logging is disabled (log_to_file=False) but you can enable it by providing a valid log_directory.
    logger = get_logger(__name__, use_case_name=use_case_name, log_to_file=False)
    logger.info('*********************Execution Started*********************')
    
    start_time = time.time()
    try:
        main()
    except Exception as _:
        logger.error("Unhandled exception in main execution.", exc_info=True)
        sys.exit(1)
    logger.info('*********************Execution Finished*********************')
    logger.info(f'Total time required = {round((time.time() - start_time) / 60, 2)} minutes')
