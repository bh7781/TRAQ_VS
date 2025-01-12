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

        # Identify data types in the regime's input files
        data_identifier = DataTypeIdentifier()
        input_files_path = regime_config.get_input_files_path()
        files = [os.path.join(input_files_path, f) for f in os.listdir(input_files_path) if f.endswith('.csv')]
        column_types = data_identifier.identify_column_types(files)

        # Generate necessary CSV files
        csv_gen = ModelGenerator(regime_config, column_types, self.use_case_name)
        csv_gen.generate_all()
