"""
This module provides classes and methods for filtering and segregating trades within Trade State Reports (TSR).
The primary focus is on segregating Alleges (if applicable), EQ trades into EQS and EQD,
and FX trades into FXC and FXO based on predefined rules and regime-specific requirements.
"""

import re
import pandas as pd
import warnings

from common import constants

warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)


eqs_products = ['Equity:Swap:PriceReturnBasicPerformance:SingleName',
                'Equity:Swap:PriceReturnBasicPerformance:SingleIndex',
                'Equity:Swap:PriceReturnBasicPerformance:Basket',
                'Equity:PortfolioSwap:PriceReturnBasicPerformance:SingleName',
                'Equity:PortfolioSwap:PriceReturnBasicPerformance:SingleIndex',
                'Equity:PortfolioSwap:PriceReturnBasicPerformance:Basket',
                'Equity:ContractForDifference:PriceReturnBasicPerformance:SingleName',
                'Equity:ContractForDifference:PriceReturnBasicPerformance:SingleIndex',
                'Equity:ContractForDifference:PriceReturnBasicPerformance:Basket',
                'Equity:Forward:PriceReturnBasicPerformance:SingleName',
                'Equity:Forward:PriceReturnBasicPerformance:SingleIndex',
                'Equity:Forward:PriceReturnBasicPerformance:Basket']

eqd_products = ['Equity:Swap:ParameterReturnDividend:SingleName',
                'Equity:Swap:ParameterReturnDividend:SingleIndex',
                'Equity:Swap:ParameterReturnDividend:Basket',
                'Equity:Swap:ParameterReturnVariance:SingleName',
                'Equity:Swap:ParameterReturnVariance:SingleIndex',
                'Equity:Swap:ParameterReturnVariance:Basket',
                'Equity:Swap:ParameterReturnVolatility:SingleName',
                'Equity:Swap:ParameterReturnVolatility:SingleIndex',
                'Equity:Swap:ParameterReturnVolatility:Basket',
                'Equity:Option:PriceReturnBasicPerformance:SingleName',
                'Equity:Option:PriceReturnBasicPerformance:SingleIndex',
                'Equity:Option:PriceReturnBasicPerformance:Basket',
                'Equity:Option:ParameterReturnDividend:SingleName',
                'Equity:Option:ParameterReturnDividend:SingleIndex',
                'Equity:Option:ParameterReturnDividend:Basket',
                'Equity:Option:ParameterReturnVariance:SingleName',
                'Equity:Option:ParameterReturnVariance:SingleIndex',
                'Equity:Option:ParameterReturnVariance:Basket',
                'Equity:Option:ParameterReturnVolatility:SingleName',
                'Equity:Option:ParameterReturnVolatility:SingleIndex',
                'Equity:Option:ParameterReturnVolatility:Basket',
                'Equity:Other:PriceReturnBasicPerformance:SingleName',
                'Equity:Other:PriceReturnBasicPerformance:SingleIndex',
                'Equity:Other:PriceReturnBasicPerformance:Basket',
                'Equity:Other:ParameterReturnDividend:SingleName',
                'Equity:Other:ParameterReturnDividend:SingleIndex',
                'Equity:Other:ParameterReturnDividend:Basket',
                'Equity:Other:ParameterReturnVariance:SingleName',
                'Equity:Other:ParameterReturnVariance:SingleIndex',
                'Equity:Other:ParameterReturnVariance:Basket',
                'Equity:Other:ParameterReturnVolatility:SingleName',
                'Equity:Other:ParameterReturnVolatility:SingleIndex',
                'Equity:Other:ParameterReturnVolatility:Basket',
                'Equity:Other']

fxc_products = ['ForeignExchange:Forward',
                'ForeignExchange:NDF',
                'ForeignExchange:Spot']

fxo_products = ['ForeignExchange:VanillaOption',
                'ForeignExchange:ComplexExotic',
                'ForeignExchange:SimpleExotic:Barrier',
                'ForeignExchange:NDO',
                'ForeignExchange:SimpleExotic:Digital']


class TSRFilters:
    """
    Base class for filtering and segregating trades in TSR data.
    Common logic for EQ and FX segregation is implemented here.
    """

    def __init__(self, data, regime, asset_class, product_id_col, logger):
        """
        Initialize the TSRFilters class with data, regime, asset class, and other parameters.
        """
        self.data = data
        self.regime = regime.upper()
        self.asset_class = asset_class.upper()
        self.product_id_col = product_id_col
        self.logger = logger

        # Automatically call the appropriate segregation method based on the asset class
        if self.asset_class in [constants.EQUITY_DERIVATIVES, constants.EQUITY_SWAPS]:
            self.data = self.segregate_eq_trades()
        elif self.asset_class in [constants.FOREIGN_EXCHANGE, constants.FOREIGN_EXCHANGE_OPTIONS, constants.FOREIGN_EXCHANGE_CASH]:
            self.data = self.segregate_fx_trades()

    @staticmethod
    def clean_product_id(product_id):
        """
        Cleans the 'Unique Product Identifier' by removing symbols, spaces, etc., and converts to lowercase.
        """
        return re.sub(r'\W+', '', product_id.lower())

    def segregate_eq_trades(self):
        """
        Segregates equity trades into EQS, EQD, and marks unclassified trades as TBD.
        Automatically returns the filtered DataFrame based on the asset class.
        """

        if self.regime.upper() == constants.JFSA:
            eqd_condition = (self.data['Asset Class'] == 'EQUI') & (self.data['Contract type'].isin(['OPTN', 'OTHR']))
            eqs_condition = (self.data['Asset Class'] == 'EQUI') & (self.data['Contract type'].isin(['SWAP', 'FORW']))
        elif self.regime.upper() == constants.ASIC:
            # Define EQD condition for ASIC regime
            eqd_condition = ((self.data['Contract Type'].isin(['OTHR', 'OPTN'])) |
                             ((self.data['Contract Type'] == 'SWAP')
                              & (self.data['Direction 1'].notna())
                              & (self.data['Direction 1'].str.strip() != '')))
            # Remaining trades that do not meet EQD condition are EQS
            eqs_condition = ~eqd_condition
        elif self.regime.upper() == constants.MAS:
            # Define EQD condition for ASIC regime
            eqd_condition = ((self.data['Contract Type'].isin(['OTHR', 'OPTN'])) |
                             ((self.data['Contract Type'] == 'SWAP')
                              & (self.data['Direction'].notna())
                              & (self.data['Direction'].str.strip() != '')))
            # Remaining trades that do not meet EQD condition are EQS
            eqs_condition = ~eqd_condition
        elif self.regime.upper() == constants.EMIR_REFIT:
            # Define EQS/EQD segregation logic for EMIR_REFIT
            eqd_condition = (
                    (self.data['Contract type'].isin(['OPTN', 'OTHR'])) |
                    (self.data['Product classification'].isin(['SEMVXC', 'SESLXC', 'SEILXC', 'SESVXC', 'SEMLXC',
                                                               'SEMDXC', 'SESDXC', 'SEBVXC', 'SEIDXC', 'SEBLXC',
                                                               'SEIVXC']))
            )
            # Remaining trades that do not meet EQD condition are EQS
            eqs_condition = ~eqd_condition
        else:
            raise ValueError(f"Segregation logic not defined for regime: {self.regime}")

        self.data.loc[:, 'EQ_Secondary_Asset_Class'] = 'TBD'
        self.data.loc[eqs_condition, 'EQ_Secondary_Asset_Class'] = 'EQS'
        self.data.loc[eqd_condition, 'EQ_Secondary_Asset_Class'] = 'EQD'

        tbd = self.data[self.data['EQ_Secondary_Asset_Class'] == 'TBD']
        if not tbd.empty:
            self.logger.warning(f"{len(tbd)} rows were not segregated into EQS or EQD.")

        if self.asset_class == constants.EQUITY_SWAPS:
            return self.data[self.data['EQ_Secondary_Asset_Class'] != 'EQD']
        else:
            return self.data[self.data['EQ_Secondary_Asset_Class'] != 'EQS']

    def segregate_fx_trades(self):
        """
        Segregates FX trades into FXC and FXO, and marks unclassified trades as TBD.
        Automatically returns the filtered DataFrame based on the asset class.
        """

        # This is common logic used by many regulators to segregate EQ TSR trades into EQS and EQD
        # If any regulator has different logic then add the same in this function

        if self.regime == constants.JFSA:
            fxc_condition = (self.data['Asset Class'] == 'CURR') & (self.data['Contract type'].isin(['FORW']))
            fxo_condition = (self.data['Asset Class'] == 'CURR') & (self.data['Contract type'].isin(['OPTN', 'OTHR']))
        elif self.regime == constants.ASIC:
            fxc_condition = (self.data['Asset Class'] == 'CURR') & (self.data['Contract Type'].isin(['FORW', 'SWAP']))
            fxo_condition = (self.data['Asset Class'] == 'CURR') & (self.data['Contract Type'].isin(['OPTN', 'OTHR']))
        elif self.regime == constants.MAS:
            fxc_condition = (self.data['Asset Class'] == 'CURR') & (self.data['Contract Type'].isin(['FORW', 'SWAP']))
            fxo_condition = (self.data['Asset Class'] == 'CURR') & (self.data['Contract Type'].isin(['OPTN', 'OTHR']))
        elif self.regime == constants.EMIR_REFIT:
            fxo_condition = (pd.notna(self.data['Product Classification']) & (self.data['Contract Type'].isin(['OPTN', 'OTHR'])))
            fxc_condition = (pd.notna(self.data['Product Classification']) & (self.data['Contract Type'] == 'FORW'))
        else:
            raise ValueError(f"Segregation logic not defined for regime: {self.regime}")

        self.data.loc['FX_Secondary_Asset_Class'] = 'TBD'
        self.data[fxc_condition, 'FX_Secondary_Asset_Class'] = 'FXC'
        self.data[fxo_condition, 'FX_Secondary_Asset_Class'] = 'FXO'

        tbd = self.data[self.data['FX_Secondary_Asset_Class'] == 'TBD']
        if not tbd.empty:
            self.logger.warning(f"{len(tbd)} rows were not segregated into FXC or FXO.")

        if self.asset_class == constants.FOREIGN_EXCHANGE_CASH:
            return self.data[self.data['FX_Secondary_Asset_Class'] != 'FXO']
        elif self.asset_class == constants.FOREIGN_EXCHANGE_OPTIONS:
            return self.data[self.data['FX_Secondary_Asset_Class'] != 'FXC']
        else:
            return self.data
