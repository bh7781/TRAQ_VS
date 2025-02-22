from diagnostic_pandq.pandq_models.model_config import MODEL_CONFIGS
from common.config.logger_config import get_logger
from common.config.args_config import Config


class RegimeConfig:
    """
    Handles configuration settings for different regimes, including paths, metadata, and environment-specific settings.
    """

    def __init__(self, regime, env, use_case_name):
        """
        Initializes the configuration for the given regime.
        """
        self.use_case_name = use_case_name
        self.regime = regime
        self.env = env.lower()
        self.logger = get_logger(__name__, Config().env.lower(), Config().run_date, use_case_name=self.use_case_name)
        self.config = self._load_config()

    def _load_config(self):
        """
        Loads the regime-specific configurations.
        """
        # If your MODEL_CONFIGS is not keyed by environment, simply use:
        regime_config = MODEL_CONFIGS.get(self.regime)
        if not regime_config:
            raise ValueError(f"Configuration for regime {self.regime} not found.")
        return regime_config

    def get_path(self, env):
        """
        Returns the filesdqconfig path based on the environment.
        """
        if env.lower() == 'qa':
            return self.config['filesdqconfig_path_qa']
        elif env.lower() == 'prod':
            return self.config['filesdqconfig_path_prod']
        else:
            raise ValueError("Invalid environment specified. Use 'qa' or 'prod'.")

    def get_metadata(self):
        """
        Returns the metadata for the regime.
        """
        return {
            'model_version': self.config['model_version'],
            'model_id': self.config['model_id'],
            'model_name': self.config['model_name'],
        }

    def get_input_files(self):
        """
        Returns the input files for the regime.
        If the configuration has 'input_file_paths', returns that list;
        otherwise, returns the folder path from 'input_files_folder_path'.
        """
        if 'input_file_paths' in self.config:
            return self.config['input_file_paths']
        else:
            return self.config['input_files_folder_path']

    def get_output_path(self):
        """
        Returns the output path for the regime.
        """
        return self.config['output_path']
