# model_config.py
import os
from common.utility import adjust_path_for_os

# A simplified configuration dictionary for each regime.
# (You can update the paths as needed.)
MODEL_CONFIGS = {
    'JFSA': {
        'filesdqconfig_path_qa': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_daily/jfsa2'),
        'filesdqconfig_path_prod': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/prod/pandq_daily/jfsa2'),
        'output_path': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_config/jfsa2/metadata'),
        'model_version': '14.10.2024',
        'model_id': 'TBD',
        'model_name': 'TBD_JFSA',
        'input_files_folder_path': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_daily/jfsa2'),
        'column_mapping': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_config/jfsa2/column_mapping/jfsa_diagnostic_field_name_mapping.json'),
    },
    'ASIC': {
        'filesdqconfig_path_qa': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_daily/asic2'),
        'filesdqconfig_path_prod': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/prod/pandq_daily/asic2'),
        'output_path': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_config/asic2/metadata'),
        'model_version': '14.10.2024',
        'model_id': 'TBD',
        'model_name': 'TBD_ASIC',
        'input_files_folder_path': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_daily/asic2'),
        'column_mapping': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_config/asic2/column_mapping/asic_diagnostic_field_name_mapping.json'),
    },
    'MAS': {
        'filesdqconfig_path_qa': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_daily/mas2'),
        'filesdqconfig_path_prod': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/prod/pandq_daily/mas2'),
        'output_path': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_config/mas2/metadata'),
        'model_version': '14.10.2024',
        'model_id': 'TBD',
        'model_name': 'TBD_MAS',
        'input_files_folder_path': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_daily/mas2'),
        'column_mapping': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_config/mas2/column_mapping/mas_diagnostic_field_name_mapping.json'),
    },
    'EMIR_REFIT': {
        'filesdqconfig_path_qa': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_daily/emir_refit'),
        'filesdqconfig_path_prod': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/prod/pandq_daily/emir_refit'),
        'output_path': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_config/emir_refit/metadata'),
        'model_version': '14.10.2024',
        'model_id': 'TBD',
        'model_name': 'TBD_EMIR_REFIT',
        'input_files_folder_path': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_daily/emir_refit'),
        'column_mapping': adjust_path_for_os('/v/region/na/appl/gtr/ttro_it_diagnostic/data/qa/pandq_config/emir_refit/column_mapping/emir_refit_diagnostic_field_name_mapping.json'),
    }
}
