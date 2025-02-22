"""
This script serves as an independent entry point for generating PANDQ model files.
It generates the following CSV files:
  - files.csv
  - filedqconfig.csv
  - filecolumns.csv
  - models.csv

Usage:
    python config_generator_main.py --env PROD --regime COMMON
"""

import argparse
from diagnostic_pandq.pandq_models.model_generator_api import PANDQModelsGenerator
from common.config.args_config import Config
from common import utility


def main():
    parser = argparse.ArgumentParser(description="Generate PANDQ model files based on a given regime.")
    parser.add_argument("--env", required=True, help="Environment name (e.g., PROD, QA, DEV, PPF)")
    parser.add_argument("--regime", required=True, help="Regime name (e.g., EMIR_REFIT, ASIC, MAS, JFSA)")
    args = parser.parse_args()

    use_case_name = 'pandq_metadata_generator'

    env = utility.sanitize_env(args.env)
    regulator = utility.sanitize_regime(args.regime)

    # Initialize global configuration object
    Config(env=env, regime=regulator, use_case_name=use_case_name)

    # Initialize the generator and create the model files.
    generator = PANDQModelsGenerator(use_case_name=use_case_name)
    generator.generate_model_files()


if __name__ == '__main__':
    main()
