"""
This script serves as an independent entry point for generating PANDQ model metadata CSV files.
It generates the following configurations:
  - files.csv
  - filedqconfig.csv
  - filecolumns.csv
  - models.csv

Usage:
    python metadata_config_generator.py --env PROD --regime EMIR_REFIT
"""

import argparse
import sys
import logging
from model_generator_facade import ModelGeneratorFacade
from common.config.args_config import Config
from common import utility

def main():
    parser = argparse.ArgumentParser(description="Generate model metadata CSV files based on a given regime.")
    parser.add_argument("--env", required=True, help="Environment name (e.g., PROD, QA, DEV)")
    parser.add_argument("--regime", required=True, help="Regime name (e.g., EMIR_REFIT, ASIC, MAS, JFSA, COMMON)")
    args = parser.parse_args()

    try:
        use_case_name = 'model_metadata_generator'
        env = utility.sanitize_env(args.env)
        regime = utility.sanitize_regime(args.regime)

        # Initialize global configuration object.
        Config(env=env, regime=regime, use_case_name=use_case_name)
        logging.info(f"Starting model metadata generation for regime: {regime}, environment: {env}")

        # Initialize the generation facade and generate the model files.
        generator = ModelGeneratorFacade(use_case_name=use_case_name)
        generator.generate_model_files()

        logging.info("Model metadata generation completed successfully.")
    except Exception as e:
        logging.error("An error occurred during model metadata generation.", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
