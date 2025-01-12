import os
from common import constants

from common.utility import adjust_path_for_os


def get_output_location(env):
    # Define base paths for different environments
    # base_path = f"/v/region/na/appl/gtr/ttro_it_diagnostic/data/{env}/pandq_daily"
    # For local testing
    base_path = rf"C:\Users\{os.getlogin()}\Morgan Stanley\Tech & TRAQ Automation - Diagnostic Testing\pandq_daily"

    base_path = adjust_path_for_os(base_path)

    # Construct output file paths for each regime and asset class
    output_location = {
        # 'log_files_location': adjust_path_for_os(rf"/v/region/eu/appl/gtr/traq/data/{env}/logs/diagnostic"),
        'log_files_location': rf'C:\Users\{os.getlogin()}\Morgan Stanley\Tech & TRAQ Automation - Diagnostic Testing\python_testing\logs',

        constants.JFSA: {
            constants.CREDIT: os.path.join(base_path, "jfsa2", 'JFSA_CR.csv'),
            constants.EQUITY_DERIVATIVES: os.path.join(base_path, "jfsa2", 'JFSA_EQD.csv'),
            constants.EQUITY_SWAPS: os.path.join(base_path, "jfsa2", 'JFSA_EQS.csv'),
            constants.FOREIGN_EXCHANGE: os.path.join(base_path, "jfsa2", 'JFSA_FX.csv'),
            constants.INTEREST_RATES: os.path.join(base_path, "jfsa2", 'JFSA_IR.csv'),
            constants.COLLATERAL: os.path.join(base_path, "jfsa2", 'JFSA_COL.csv'),
        },

        constants.ASIC: {
            constants.COMMODITY: os.path.join(base_path, 'asic2', 'ASIC_CO.csv'),
            constants.CREDIT: os.path.join(base_path, 'asic2', 'ASIC_CR.csv'),
            constants.EQUITY_DERIVATIVES: os.path.join(base_path, 'asic2', 'ASIC_EQD.csv'),
            constants.EQUITY_SWAPS: os.path.join(base_path, 'asic2', 'ASIC_EQS.csv'),
            constants.FOREIGN_EXCHANGE: os.path.join(base_path, 'asic2', 'ASIC_FX.csv'),
            constants.INTEREST_RATES: os.path.join(base_path, 'asic2', 'ASIC_IR.csv'),
            constants.COLLATERAL: os.path.join(base_path, 'asic2', 'ASIC_COL.csv'),
        },

        constants.MAS: {
            constants.COMMODITY: os.path.join(base_path, 'mas2', 'MAS_CO.csv'),
            constants.CREDIT: os.path.join(base_path, 'mas2', 'MAS_CR.csv'),
            constants.EQUITY_DERIVATIVES: os.path.join(base_path, 'mas2', 'MAS_EQD.csv'),
            constants.EQUITY_SWAPS: os.path.join(base_path, 'mas2', 'MAS_EQS.csv'),
            constants.FOREIGN_EXCHANGE: os.path.join(base_path, 'mas2', 'MAS_FX.csv'),
            constants.INTEREST_RATES: os.path.join(base_path, 'mas2', 'MAS_IR.csv'),
            constants.COLLATERAL: os.path.join(base_path, 'mas2', 'MAS_COL.csv'),
        },

        constants.EMIR_REFIT: {
            constants.COMMODITY: os.path.join(base_path, 'emir_refit', 'EMIR_REFIT_CO.csv'),
            constants.CREDIT: os.path.join(base_path, 'emir_refit', 'EMIR_REFIT_CR.csv'),
            constants.EQUITY_DERIVATIVES: os.path.join(base_path, 'emir_refit', 'EMIR_REFIT_EQD.csv'),
            constants.EQUITY_SWAPS: os.path.join(base_path, 'emir_refit', 'EMIR_REFIT_EQS.csv'),
            constants.FOREIGN_EXCHANGE: os.path.join(base_path, 'emir_refit', 'EMIR_REFIT_FX.csv'),
            constants.INTEREST_RATES: os.path.join(base_path, 'emir_refit', 'EMIR_REFIT_IR.csv'),
            constants.COLLATERAL: os.path.join(base_path, 'emir_refit', 'EMIR_REFIT_COL.csv'),
            constants.EXCHANGE_TRADES_DERIVATIVES_ACTIVITY: os.path.join(base_path, 'emir_refit', 'EMIR_REFIT_ETDACTIVITY.csv'),
            constants.EXCHANGE_TRADES_DERIVATIVES_POSITION: os.path.join(base_path, 'emir_refit', 'EMIR_REFIT_ETDPOSITION.csv'),
        },
        # Add output file paths for other regimes below...
    }

    return output_location


def get_column_json_location(env):
    # Define base paths for different environments
    # base_path = f'/v/region/na/appl/gtr/ttro_it_diagnostic/data/{env}/pandq_config'
    # For local testing
    base_path = rf'C:\Users\{os.getlogin()}\Morgan Stanley\Tech & TRAQ Automation - Diagnostic Testing\pandq_config'

    # Adjust the path for Windows or Linux
    base_path = adjust_path_for_os(base_path)

    # Construct output file paths for each regime and asset class JSON columns
    column_json_location = {
        constants.JFSA: {
            constants.CREDIT: os.path.join(base_path, 'jfsa2', 'columns'),
            constants.EQUITY_DERIVATIVES: os.path.join(base_path, 'jfsa2', 'columns'),
            constants.EQUITY_SWAPS: os.path.join(base_path, 'jfsa2', 'columns'),
            constants.FOREIGN_EXCHANGE: os.path.join(base_path, 'jfsa2', 'columns'),
            constants.INTEREST_RATES: os.path.join(base_path, 'jfsa2', 'columns'),
            constants.COLLATERAL: os.path.join(base_path, 'jfsa2', 'columns'),
        },

        constants.ASIC: {
            constants.COMMODITY: os.path.join(base_path, 'asic2', 'columns'),
            constants.CREDIT: os.path.join(base_path, 'asic2', 'columns'),
            constants.EQUITY_DERIVATIVES: os.path.join(base_path, 'asic2', 'columns'),
            constants.EQUITY_SWAPS: os.path.join(base_path, 'asic2', 'columns'),
            constants.FOREIGN_EXCHANGE: os.path.join(base_path, 'asic2', 'columns'),
            constants.INTEREST_RATES: os.path.join(base_path, 'asic2', 'columns'),
            constants.COLLATERAL: os.path.join(base_path, 'asic2', 'columns'),
        },

        constants.MAS: {
            constants.COMMODITY: os.path.join(base_path, 'mas2', 'columns'),
            constants.CREDIT: os.path.join(base_path, 'mas2', 'columns'),
            constants.EQUITY_DERIVATIVES: os.path.join(base_path, 'mas2', 'columns'),
            constants.EQUITY_SWAPS: os.path.join(base_path, 'mas2', 'columns'),
            constants.FOREIGN_EXCHANGE: os.path.join(base_path, 'mas2', 'columns'),
            constants.INTEREST_RATES: os.path.join(base_path, 'mas2', 'columns'),
            constants.COLLATERAL: os.path.join(base_path, 'mas2', 'columns'),
        },

        constants.EMIR_REFIT: {
            constants.COMMODITY: os.path.join(base_path, 'emir_refit', 'columns'),
            constants.CREDIT: os.path.join(base_path, 'emir_refit', 'columns'),
            constants.EQUITY_DERIVATIVES: os.path.join(base_path, 'emir_refit', 'columns'),
            constants.EQUITY_SWAPS: os.path.join(base_path, 'emir_refit', 'columns'),
            constants.FOREIGN_EXCHANGE: os.path.join(base_path, 'emir_refit', 'columns'),
            constants.INTEREST_RATES: os.path.join(base_path, 'emir_refit', 'columns'),
            constants.COLLATERAL: os.path.join(base_path, 'emir_refit', 'columns'),
            constants.EXCHANGE_TRADES_DERIVATIVES_ACTIVITY: os.path.join(base_path, 'emir_refit', 'columns'),
            constants.EXCHANGE_TRADES_DERIVATIVES_POSITION: os.path.join(base_path, 'emir_refit', 'columns'),
        },
        # Add output paths for other regimes below...
    }

    return column_json_location
