import pandas as pd
import os
from common.config.logger_config import get_logger
from common.config.args_config import Config
from column_datatype_identifier import detect_delimiter


class MetadataCSVGenerator:
    """
    Generates the required metadata CSV files:
      - filecolumns.csv: Column metadata.
      - filedqconfig.csv: Data quality configuration for files.
      - files.csv: Mapping of file names to IDs and descriptions.
      - models.csv: Model metadata.
    """
    def __init__(self, regime_config, column_types, use_case_name, logger=None):
        """
        Initializes the generator with the configuration and identified column types.
        """
        self.use_case_name = use_case_name
        self.regime_config = regime_config
        self.column_types = column_types  # Dictionary: file_path -> { column_name: data_type, ... }
        self.env = Config().env.lower()
        self.logger = logger if logger is not None else get_logger(__name__, Config().env, Config().run_date, use_case_name=use_case_name, log_to_file=False)

    def generate_file_columns(self):
        """
        Generates filecolumns.csv based on identified column types.
        """
        try:
            self.logger.info("Starting generation of filecolumns.csv")
            file_columns_data = []
            files = list(self.column_types.keys())
            file_id_mapping = {file: idx + 1 for idx, file in enumerate(files)}

            for file, columns in self.column_types.items():
                file_id = file_id_mapping[file]
                column_id = 1
                for col_name, data_type in columns.items():
                    file_columns_data.append({
                        "COLUMN_ID": column_id,
                        "SRC_FILE_ID": file_id,
                        "COLUMN_NAME": col_name,
                        "DESCRIPTION": '',
                        "DATA_TYPE": 'String',  # Fixed as 'String'
                        "LENGTH": 256,
                        "SCALE": 0,
                        "IS_NULL": 1,
                        "POSITION": column_id,
                        "DATE_FORMAT": '',
                        "IS_PRIMARY_KEY": 0,
                    })
                    column_id += 1

            df_file_columns = pd.DataFrame(file_columns_data)
            output_path = os.path.join(self.regime_config.get_output_path(), 'filecolumns.csv')
            self.logger.debug(f"Writing filecolumns.csv to {output_path}")
            df_file_columns.to_csv(output_path, index=False)
            self.logger.info("Successfully generated filecolumns.csv")
        except Exception as _:
            self.logger.error("Error generating filecolumns.csv", exc_info=True)
            raise

    def generate_filedqconfig(self):
        """
        Generates filedqconfig.csv with file paths and configuration details.
        The file paths are saved in UNIX format, the delimiter is detected from each file,
        and the frequency is set to 'NULL' for a single entry per environment.

        This implementation first lists all DEV file paths, then all PROD file paths.
        """
        try:
            self.logger.info("Starting generation of filedqconfig.csv")
            files = list(self.column_types.keys())
            # file_ids = list(range(1, len(files) + 1))
            dq_config_text = self.regime_config.config.get('filesdqconfig_text', '')

            def to_unix_path(path):
                unixpath = path.replace('\\', '/')
                if unixpath.startswith('//'):
                    unixpath = unixpath[1:]
                return unixpath

            # Generate DEV records first.
            dev_records = []
            for idx, file in enumerate(files):
                file_id = idx + 1
                delimiter = detect_delimiter(file)
                unix_path = to_unix_path(self.regime_config.get_path('QA'))
                dev_records.append({
                    "SRC_FILE_ID": file_id,
                    "FILE_PATH": unix_path,
                    "ENVIRONMENT": "DEV",
                    "FILE_TYPE": "csv",
                    "DELIMITER": delimiter,
                    "HAS_HEADER": "Y",
                    "HAS_TRAILER": "N",
                    "HEADER_FILE_NAME": "",
                    "HEADER_FILE_PATH": "",
                    "NUMBER_OF_COLUMNS": len(self.column_types[file]),
                    "FREQUENCY": "NULL",
                    "REGION": "ALL",
                    "TEXT": dq_config_text,
                    "SOURCE_CONTACT": "ttro_it_diagnostic"
                })

            # Generate PROD records next.
            prod_records = []
            for idx, file in enumerate(files):
                file_id = idx + 1
                delimiter = detect_delimiter(file)
                unix_path = to_unix_path(self.regime_config.get_path('PROD'))
                prod_records.append({
                    "SRC_FILE_ID": file_id,
                    "FILE_PATH": unix_path,
                    "ENVIRONMENT": "PROD",
                    "FILE_TYPE": "csv",
                    "DELIMITER": delimiter,
                    "HAS_HEADER": "Y",
                    "HAS_TRAILER": "N",
                    "HEADER_FILE_NAME": "",
                    "HEADER_FILE_PATH": "",
                    "NUMBER_OF_COLUMNS": len(self.column_types[file]),
                    "FREQUENCY": "NULL",
                    "REGION": "ALL",
                    "TEXT": dq_config_text,
                    "SOURCE_CONTACT": "ttro_it_diagnostic"
                })

            # Concatenate DEV records first, then PROD records.
            all_records = dev_records + prod_records
            df_filedqconfig = pd.DataFrame(all_records)
            output_path = os.path.join(self.regime_config.get_output_path(), 'filedqconfig.csv')
            self.logger.debug(f"Writing filedqconfig.csv to {output_path}")
            df_filedqconfig.to_csv(output_path, index=False)
            self.logger.info("Successfully generated filedqconfig.csv")
        except Exception:
            self.logger.error("Error generating filedqconfig.csv", exc_info=True)
            raise

    def generate_files(self):
        """
        Generates files.csv mapping file names to IDs and descriptions.
        File entity name is the uppercase of the filename (without extension),
        and description is the entity name appended with " data".
        """
        try:
            self.logger.info("Starting generation of files.csv")
            files = list(self.column_types.keys())
            file_names = [os.path.basename(f) for f in files]
            file_entities = [os.path.splitext(name)[0].upper() for name in file_names]
            descriptions = [entity + " data" for entity in file_entities]

            df_files = pd.DataFrame({
                "FILE_ID": range(1, len(file_names) + 1),
                "FILE_NAME": file_names,
                "FILE_ENTITY_NAME": file_entities,
                "DESCRIPTION": descriptions
            })
            output_path = os.path.join(self.regime_config.get_output_path(), 'files.csv')
            self.logger.debug(f"Writing files.csv to {output_path}")
            df_files.to_csv(output_path, index=False)
            self.logger.info("Successfully generated files.csv")
        except Exception as _:
            self.logger.error("Error generating files.csv", exc_info=True)
            raise

    def generate_models(self):
        """
        Generates models.csv with model metadata.
        """
        try:
            self.logger.info("Starting generation of models.csv")
            metadata = self.regime_config.get_metadata()
            model_data = {
                "Model ID": metadata['model_id'],
                "Model Name": metadata['model_name'],
                "Model Type": "FILE",
                "Model Version": metadata['model_version'],
            }
            df_models = pd.DataFrame([model_data])
            output_path = os.path.join(self.regime_config.get_output_path(), 'models.csv')
            self.logger.debug(f"Writing models.csv to {output_path}")
            df_models.to_csv(output_path, index=False)
            self.logger.info("Successfully generated models.csv")
        except Exception as _:
            self.logger.error("Error generating models.csv", exc_info=True)
            raise

    def generate_all(self):
        """
        Generates all required metadata CSV files.
        """
        self.logger.info("Starting complete metadata CSV generation process.")
        self.generate_file_columns()
        self.generate_filedqconfig()
        self.generate_files()
        self.generate_models()
        self.logger.info("Completed metadata CSV generation process successfully.")
