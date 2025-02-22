#!/usr/bin/env python3
"""
config_generator_main.py

This script serves as an independent entry point for generating PANDQ model files.
It generates the following CSV files:
  - files.csv
  - filedqconfig.csv
  - filecolumns.csv
  - models.csv

Usage:
    python config_generator_main.py --regime COMMON --env qa --use_case_name my_use_case
"""

import argparse
from diagnostic_pandq.pandq_models.model_generator_api import PANDQModelsGenerator
from common.config.args_config import Config

def main():
    parser = argparse.ArgumentParser(description="Generate PANDQ model files based on a given regime or common data.")
    parser.add_argument("--regime", required=True, help="Regime name (e.g., EMIR_REFIT, ASIC, MAS, JFSA, COMMON)")
    parser.add_argument("--env", default="qa", help="Environment to use (qa or prod)")
    parser.add_argument("--use_case_name", default="default_use_case", help="Use case name for logging and tracking")
    args = parser.parse_args()

    # Update the global configuration with command-line parameters.
    config = Config()
    config.regime = args.regime
    config.env = args.env

    # Initialize the generator and generate the model files.
    generator = PANDQModelsGenerator(use_case_name=args.use_case_name)
    generator.generate_model_files()

if __name__ == '__main__':
    main()
