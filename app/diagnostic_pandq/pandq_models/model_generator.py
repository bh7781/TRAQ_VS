import pandas as pd
import os
from common.config.logger_config import get_logger
from common.config.args_config import Config


class ModelGenerator:
    """
    Generates the required model files (filecolumns.csv, filedqconfig.csv, files.csv, models.csv).
    """

    def __init__(self, regime_config, column_types, use_case_name):
        """
        Initializes the CSV generator with the configuration and identified column types.
        """
        self.use_case_name = use_case_name
        self.regime_config = regime_config
        self.column_types = column_types
        self.env = Config().env.lower()
        self.logger = get_logger(__name__, self.env.lower(), Config().run_date, use_case_name=use_case_name)

    def generate_file_columns(self):
        """
        Generates filecolumns.csv based on identified column types.
        """
        file_columns_data = []

        # Get the list of files and assign FILE_IDs
        files = list(self.column_types.keys())
        file_id_mapping = {file: idx + 1 for idx, file in enumerate(files)}

        for file, columns in self.column_types.items():
            file_id = file_id_mapping[file]
            column_id = 1  # Start column count from 1 for each file

            for column, data_type in columns.items():
                file_columns_data.append({
                    "COLUMN_ID": column_id,  # Start from 1 for each file
                    "SRC_FILE_ID": file_id,  # Use the file ID from the mapping
                    "COLUMN_NAME": column,
                    "DESCRIPTION": '',
                    # "DATA_TYPE": data_type,
                    "DATA_TYPE": 'STRING',  # Keep DATA_TYPE fixed as 'STRING'
                    "LENGTH": 256,
                    "SCALE": 0,
                    "IS_NULL": 1,
                    "POSITION": column_id,  # POSITION should also start from 1 for each file
                    "DATE_FORMAT": '',  # Keep DATE_FORMAT empty if not needed
                    # "DATE_FORMAT": data_type if data_type in ['DATE', 'TIMESTAMP'] else None,
                    "IS_PRIMARY_KEY": 0,
                })

                column_id += 1  # Increment column ID for each column in the file

        # Convert to DataFrame and save as CSV
        df_file_columns = pd.DataFrame(file_columns_data)
        output_path = os.path.join(self.regime_config.get_output_path(), 'filecolumns.csv')
        df_file_columns.to_csv(output_path, index=False)

    def generate_filedqconfig(self):
        """
        Generates filedqconfig.csv with paths and configuration details for both QA and PROD environments.
        """
        files = [os.path.basename(f) for f in self.column_types.keys()]
        file_ids = list(range(1, len(files) + 1))

        # Generate file paths and other details for QA
        qa_file_paths = [self.regime_config.get_path('QA') for _ in files]
        qa_df_filedqconfig_daily = pd.DataFrame({
            "SRC_FILE_ID": file_ids,
            "FILE_PATH": qa_file_paths,
            "ENVIRONMENT": ['DEV'] * len(files),
            "FILE_TYPE": "csv",
            "DELIMITER": "|",
            "HAS_HEADER": "Y",
            "HAS_TRAILER": "N",
            "HEADER_FILE_NAME": "",
            "HEADER_FILE_PATH": "",
            "NUMBER_OF_COLUMNS": [len(self.column_types[file]) for file in self.column_types.keys()],
            "FREQUENCY": "Daily",
            "REGION": "ALL",
            "TEXT": self.regime_config.config.get('filesdqconfig_text', ''),
            "SOURCE_CONTACT": "ttro_it_diagnostic"
        })

        # Generate file paths and other details for QA Quarterly
        qa_df_filedqconfig_quarterly = pd.DataFrame({
            "SRC_FILE_ID": file_ids,
            "FILE_PATH": qa_file_paths,
            "ENVIRONMENT": ['DEV'] * len(files),
            "FILE_TYPE": "csv",
            "DELIMITER": "|",
            "HAS_HEADER": "Y",
            "HAS_TRAILER": "N",
            "HEADER_FILE_NAME": "",
            "HEADER_FILE_PATH": "",
            "NUMBER_OF_COLUMNS": [len(self.column_types[file]) for file in self.column_types.keys()],
            "FREQUENCY": "Daily",
            "REGION": "ALL",
            "TEXT": self.regime_config.config.get('filesdqconfig_text', ''),
            "SOURCE_CONTACT": "ttro_it_diagnostic"
        })

        # Generate file paths and other details for PROD
        prod_file_paths = [self.regime_config.get_path('PROD') for _ in files]
        prod_df_filedqconfig_daily = pd.DataFrame({
            "SRC_FILE_ID": file_ids,
            "FILE_PATH": prod_file_paths,
            "ENVIRONMENT": ['PROD'] * len(files),
            "FILE_TYPE": "csv",
            "DELIMITER": "|",
            "HAS_HEADER": "Y",
            "HAS_TRAILER": "N",
            "HEADER_FILE_NAME": "",
            "HEADER_FILE_PATH": "",
            "NUMBER_OF_COLUMNS": [len(self.column_types[file]) for file in self.column_types.keys()],
            "FREQUENCY": "Daily",
            "REGION": "ALL",
            "TEXT": self.regime_config.config.get('filesdqconfig_text', ''),
            "SOURCE_CONTACT": "ttro_it_diagnostic"
        })

        # Generate file paths and other details for PROD Quarterly
        prod_df_filedqconfig_quarterly = pd.DataFrame({
            "SRC_FILE_ID": file_ids,
            "FILE_PATH": prod_file_paths,
            "ENVIRONMENT": ['PROD'] * len(files),
            "FILE_TYPE": "csv",
            "DELIMITER": "|",
            "HAS_HEADER": "Y",
            "HAS_TRAILER": "N",
            "HEADER_FILE_NAME": "",
            "HEADER_FILE_PATH": "",
            "NUMBER_OF_COLUMNS": [len(self.column_types[file]) for file in self.column_types.keys()],
            "FREQUENCY": "Daily",
            "REGION": "ALL",
            "TEXT": self.regime_config.config.get('filesdqconfig_text', ''),
            "SOURCE_CONTACT": "ttro_it_diagnostic"
        })

        # Concatenate the QA and PROD DataFrames
        df_filedqconfig = pd.concat([qa_df_filedqconfig_daily, prod_df_filedqconfig_daily,
                                     qa_df_filedqconfig_quarterly, prod_df_filedqconfig_quarterly])

        # Save the combined DataFrame to the CSV file
        output_path = os.path.join(self.regime_config.get_output_path(), 'filedqconfig.csv')
        df_filedqconfig.to_csv(output_path, index=False)

    def generate_files(self):
        """
        Generates files.csv mapping file names to IDs and descriptions.
        """
        files = [os.path.basename(f) for f in self.column_types.keys()]

        df_files = pd.DataFrame({
            "FILE_ID": range(1, len(files) + 1),
            "FILE_NAME": files,
            "FILE_ENTITY_NAME": [f.replace('.csv', '') for f in files],
            "DESCRIPTION": "Combined TSR and DerivOne file."
        })

        output_path = os.path.join(self.regime_config.get_output_path(), 'files.csv')
        df_files.to_csv(output_path, index=False)

    def generate_models(self):
        """
        Generates models.csv with model metadata.
        """
        model_data = {
            "Model ID": self.regime_config.get_metadata()['model_id'],
            "Model Name": self.regime_config.get_metadata()['model_name'],
            "Model Type": "FILE",
            "Model Version": self.regime_config.get_metadata()['model_version'],
        }

        df_models = pd.DataFrame([model_data])

        output_path = os.path.join(self.regime_config.get_output_path(), 'models.csv')
        df_models.to_csv(output_path, index=False)

    def generate_all(self):
        """
        Generates all required CSV files.
        """
        self.logger.info('Generating filecolumns.csv')
        self.generate_file_columns()
        self.logger.info('Generating filedqconfig.csv')
        self.generate_filedqconfig()
        self.logger.info('Generating files.csv')
        self.generate_files()
        self.logger.info('Generating models.csv')
        self.generate_models()
        self.logger.info('Finished model config generation.')
