"""
This file contains file paths to all the reference data sources used in all TRAQ use-cases
"""
import os

from common.utility import adjust_path_for_os


def get_ref_data_location(env):
    # Define base paths for different environments
    base_path = f"/v/region/eu/appl/gtr/traq/data/{env.lower()}/input"

    base_path = adjust_path_for_os(base_path)

    # Construct output file paths for each regime and asset class
    ref_data = {
        'GLEIF': os.path.join(base_path, "gleif", 'gleif-goldencopy-lei2-golden-copy.csv'),
        # Add other reference data below...
    }

    return ref_data
