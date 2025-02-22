import os
from common.config.args_config import Config
from regime_configuration import RegimeConfiguration
from column_datatype_identifier import ColumnDataTypeIdentifier
from metadata_csv_generator import MetadataCSVGenerator

class ModelGeneratorFacade:
    """
    Facade class that encapsulates the entire model metadata generation process,
    including configuration loading, column data type identification, and CSV generation.
    """
    def __init__(self, use_case_name):
        """
        Initializes the facade with the given use case name.
        """
        self.use_case_name = use_case_name
        self.regime = Config().regime.upper()
        self.env = Config().env.lower()

    def generate_model_files(self):
        """
        Executes the complete model metadata generation process.
        """
        try:
            # Load regime-specific configuration.
            regime_config = RegimeConfiguration(self.regime, self.env, use_case_name=self.use_case_name)

            # Get input files from configuration.
            input_files_info = regime_config.get_input_files()
            if isinstance(input_files_info, list):
                files = input_files_info
            else:
                files = [os.path.join(input_files_info, f) for f in os.listdir(input_files_info) if f.endswith('.csv')]

            print(f"INFO: Processing files: {files}")

            # Identify column data types in the input files.
            datatype_identifier = ColumnDataTypeIdentifier()
            column_types = datatype_identifier.identify_column_types(files)

            # Generate CSV metadata files.
            csv_generator = MetadataCSVGenerator(regime_config, column_types, self.use_case_name)
            csv_generator.generate_all()
        except Exception as e:
            print("ERROR: An error occurred in the model generation process.", e)
            raise
