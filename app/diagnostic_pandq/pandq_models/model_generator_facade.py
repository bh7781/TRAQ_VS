import os
from common.config.args_config import Config
from regime_configuration import RegimeConfiguration
from metadata_csv_generator import MetadataCSVGenerator

class ModelGeneratorFacade:
    """
    Facade class that encapsulates the entire model metadata generation process,
    including configuration loading, (optional) column data type identification, and CSV generation.
    """
    def __init__(self, use_case_name, logger=None):
        """
        Initializes the facade with the given use case name and an optional logger.
        If no logger is passed, it will create one using the common logger configuration.
        """
        self.use_case_name = use_case_name
        self.regime = Config().regime.upper()
        self.env = Config().env.lower()
        # Use the provided logger or create one with the common logger.
        if logger is not None:
            self.logger = logger
        else:
            from common.config.logger_config import get_logger
            self.logger = get_logger(__name__, self.env, Config().run_date, use_case_name=self.use_case_name)

    def generate_model_files(self):
        """
        Executes the complete model metadata generation process.
        It loads the configuration, collects the input files, identifies column names,
        and generates the metadata CSV files.
        """
        try:
            # Load regime-specific configuration.
            regime_config = RegimeConfiguration(self.regime, self.env, use_case_name=self.use_case_name, logger=self.logger)

            # Get input files from configuration.
            input_files_info = regime_config.get_input_files()
            if isinstance(input_files_info, list):
                files = input_files_info
            else:
                files = [os.path.join(input_files_info, f) for f in os.listdir(input_files_info) if f.endswith('.csv')]
            
            self.logger.info(f"Processing files: {files}")

            # Option to use full column data type identification (which is slow)
            # versus a fast header-only extraction.
            USE_FULL_DATATYPE_IDENTIFICATION = False  # Set this to True to use full identification later.
            if USE_FULL_DATATYPE_IDENTIFICATION:
                # Uncomment the following lines if you want to use the full ColumnDataTypeIdentifier.
                # from column_datatype_identifier import ColumnDataTypeIdentifier
                # datatype_identifier = ColumnDataTypeIdentifier()
                # column_types = datatype_identifier.identify_column_types(files)
                pass  # Comment this line if USE_FULL_DATATYPE_IDENTIFICATION is set to True.
            else:
                # Use a fast method that reads only the CSV header to get column names.
                # We then create a dummy column_types dict where each column's data type is fixed as 'String'.
                from column_datatype_identifier import detect_delimiter
                import pandas as pd
                column_types = {}
                for file in files:
                    delim = detect_delimiter(file)
                    try:
                        # Read only the header row to get column names.
                        df = pd.read_csv(file, nrows=0, sep=delim)
                        # Build a dictionary mapping each column to 'String'.
                        column_types[file] = {col: 'String' for col in df.columns}
                        self.logger.debug(f"Header for file {file}: {list(df.columns)}")
                    except Exception as ex:
                        self.logger.error(f"Error reading header from file {file}", exc_info=True)
                        column_types[file] = {}

            # Generate the metadata CSV files using the (dummy) column_types.
            csv_generator = MetadataCSVGenerator(regime_config, column_types, self.use_case_name, logger=self.logger)
            csv_generator.generate_all()

        except Exception:
            self.logger.error("An error occurred in the model generation process.", exc_info=True)
            raise
