import os
from common import constants

from common.utility import adjust_path_for_os


def get_model_configs(env):
    # Define base paths for different environments
    # pandq_output_base_path = f'/v/region/na/appl/gtr/ttro_it_diagnostic/data/{env}/pandq_daily'
    # For local testing
    pandq_output_base_path = rf'C:\Users\{os.getlogin()}\Morgan Stanley\Tech & TRAQ Automation - Diagnostic Testing\pandq_daily'
    pandq_output_base_path = adjust_path_for_os(pandq_output_base_path)

    # Define base paths for different environments
    # pandq_config_base_path = f'/v/region/na/appl/gtr/ttro_it_diagnostic/data/{env}/pandq_config'
    # For local testing
    pandq_config_base_path = rf'C:\Users\{os.getlogin()}\Morgan Stanley\Tech & TRAQ Automation - Diagnostic Testing\pandq_config'
    pandq_config_base_path = adjust_path_for_os(pandq_config_base_path)

    # Construct output file paths for each regime and asset class
    configs = {
        constants.JFSA: {
            'filesdqconfig_path_qa': os.path.join(pandq_output_base_path, 'jfsa2'),
            'filesdqconfig_path_prod': os.path.join(pandq_output_base_path, 'jfsa2'),
            'output_path': os.path.join(pandq_config_base_path, 'jfsa2', 'metadata'),
            'model_version': '14.10.2024',
            'model_id': 'TBD',
            'model_name': 'TBD_JFSA',
            'input_files_folder_path': os.path.join(pandq_output_base_path, 'jfsa2'),
            'column_mapping': os.path.join(pandq_config_base_path, 'jfsa2', 'column_mapping', 'jfsa_diagnostic_field_name_mapping.json'),
        },

        constants.ASIC: {
            'filesdqconfig_path_qa': os.path.join(pandq_output_base_path, 'asic2'),
            'filesdqconfig_path_prod': os.path.join(pandq_output_base_path, 'asic2'),
            'output_path': os.path.join(pandq_config_base_path, 'asic2', 'metadata'),
            'model_version': '14.10.2024',
            'model_id': 'TBD',
            'model_name': 'TBD_ASIC',
            'input_files_folder_path': os.path.join(pandq_output_base_path, 'asic2'),
            'column_mapping': os.path.join(pandq_config_base_path, 'asic2', 'column_mapping', 'asic_diagnostic_field_name_mapping.json'),
        },

        constants.MAS: {
            'filesdqconfig_path_qa': os.path.join(pandq_output_base_path, 'mas2'),
            'filesdqconfig_path_prod': os.path.join(pandq_output_base_path, 'mas2'),
            'output_path': os.path.join(pandq_config_base_path, 'mas2', 'metadata'),
            'model_version': '14.10.2024',
            'model_id': 'TBD',
            'model_name': 'TBD_MAS',
            'input_files_folder_path': os.path.join(pandq_output_base_path, 'mas2'),
            'column_mapping': os.path.join(pandq_config_base_path, 'mas2', 'column_mapping', 'mas_diagnostic_field_name_mapping.json'),
        },

        constants.EMIR_REFIT: {
            'filesdqconfig_path_qa': os.path.join(pandq_output_base_path, 'emir_refit'),
            'filesdqconfig_path_prod': os.path.join(pandq_output_base_path, 'emir_refit'),
            'output_path': os.path.join(pandq_config_base_path, 'emir_refit', 'metadata'),
            'model_version': '14.10.2024',
            'model_id': 'TBD',
            'model_name': 'TBD_MAS',
            'input_files_folder_path': os.path.join(pandq_output_base_path, 'emir_refit'),
            'column_mapping': os.path.join(pandq_config_base_path, 'emir_refit', 'column_mapping', 'emir_refit_diagnostic_field_name_mapping.json'),
        }
    }

    return configs
