import os
from common import constants
from common.utility import adjust_path_for_os

MODEL_CONFIGS = {
    constants.JFSA: {
        'filesdqconfig_path_qa': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_daily/jfsa2'),
        'filesdqconfig_path_prod': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/prod/pandq_daily/jfsa2'),
        'output_path': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_config/jfsa2/metadata'),
        'model_version': '14.10.2024',
        'model_id': 'Q1234',
        'model_name': 'JFSA',
        'input_files_folder_path': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_daily/jfsa2'),
        'column_mapping': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_config/jfsa2/column_mapping/jfsa_diagnostic_field_name_mapping.json'),
    },

    constants.ASIC: {
        'filesdqconfig_path_qa': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_daily/asic2'),
        'filesdqconfig_path_prod': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/prod/pandq_daily/asic2'),
        'output_path': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_config/asic2/metadata'),
        'model_version': '14.10.2024',
        'model_id': 'Q1234',
        'model_name': 'ASIC',
        'input_files_folder_path': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_daily/asic2'),
        'column_mapping': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_config/asic2/column_mapping/asic_diagnostic_field_name_mapping.json'),
    },

    constants.MAS: {
        'filesdqconfig_path_qa': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_daily/mas2'),
        'filesdqconfig_path_prod': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/prod/pandq_daily/mas2'),
        'output_path': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_config/mas2/metadata'),
        'model_version': '14.10.2024',
        'model_id': 'Q1234',
        'model_name': 'MAS',
        'input_files_folder_path': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_daily/mas2'),
        'column_mapping': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_config/mas2/column_mapping/mas_diagnostic_field_name_mapping.json'),
    },

    constants.EMIR_REFIT: {
        'filesdqconfig_path_qa': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_daily/emir_refit'),
        'filesdqconfig_path_prod': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/prod/pandq_daily/emir_refit'),
        'output_path': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_config/emir_refit/metadata'),
        'model_version': '14.10.2024',
        'model_id': 'Q1234',
        'model_name': 'EMIR_REFIT',
        'input_files_folder_path': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_daily/emir_refit'),
        'column_mapping': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_config/emir_refit/column_mapping/emir_refit_diagnostic_field_name_mapping.json'),
    },

    constants.COMMON: {
        # Specify a list of full file paths.
        'input_file_paths': [
            adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/prod/pandq_daily/common_data/anna_dsb.csv'),
            adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/prod/pandq_daily/common_data/ISO_MIC.csv'),
            adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/prod/pandq_daily/common_data/fx_rates.csv'),
        ],
        'filesdqconfig_path_qa': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/common'),
        'filesdqconfig_path_prod': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/prod/common'),
        # 'output_path': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_config/common/metadata'),
        'output_path': rf'C:\Users\{os.getlogin()}\Morgan Stanley\Tech & TRAQ Automation - Diagnostic Testing\pandq_config\common\metadata',
        'model_version': '22.02.2025',
        'model_id': 'Q1234',
        'model_name': 'COMMON',
        # Column mapping can be set to None or defined as needed.
        'column_mapping': None,
    },
}
