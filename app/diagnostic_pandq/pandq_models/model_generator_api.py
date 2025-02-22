# model_generator_api.py
import os
from common.config.args_config import Config
from diagnostic_pandq.pandq_models.regime_config import RegimeConfig
from diagnostic_pandq.pandq_models.data_type_identifier import DataTypeIdentifier
from diagnostic_pandq.pandq_models.model_generator import ModelGenerator

class PANDQModelsGenerator:
    """
    Facade class that encapsulates the entire PANDQ models generation process,
    including configuration loading, data type identification, and CSV generation.
    """

    def __init__(self, use_case_name):
        """
        Initializes the generator with the given regime and environment.
        """
        self.use_case_name = use_case_name
        self.regime = Config().regime.upper()
        self.env = Config().env.lower()

    def generate_model_files(self):
        """
        Executes the entire PANDQ models generation process, including data type identification
        and CSV file generation.
        """
        # Load regime-specific configuration
        regime_config = RegimeConfig(self.regime, self.env, use_case_name=self.use_case_name)

        # Get input files from the configuration.
        input_files_info = regime_config.get_input_files()
        if isinstance(input_files_info, list):
            # For common data, input_files_info is already a list of full file paths.
            files = input_files_info
        else:
            # For regime-specific data, treat input_files_info as a folder path.
            files = [os.path.join(input_files_info, f) for f in os.listdir(input_files_info) if f.endswith('.csv')]

        # Identify data types in the input files
        data_identifier = DataTypeIdentifier()
        column_types = data_identifier.identify_column_types(files)

        # Generate necessary CSV files
        csv_gen = ModelGenerator(regime_config, column_types, self.use_case_name)
        csv_gen.generate_all()
