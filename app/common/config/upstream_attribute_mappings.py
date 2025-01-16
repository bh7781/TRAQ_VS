"""
This file contains upstream attributes and their mapping across asset classes.
"""

COMPANY_CODE = {
    'CO': 'Identifier of Counterparty 1',
    'CR': 'Trade Party 1 Value',
    'EQD': 'Order Filler',
    'EQS': '',
    'FXC': 'Company Code',
    'FXO': 'Company Code',
    'IR': 'Data Submitter UCI'
}

PARTY_1_ACCOUNT_NUMBER = {
    'CO': 'Trade Party 1 Account',
    'CR': '',
    'EQD': 'Party 1',
    'EQS': 'Party 1',
    'FXC': 'Trade Party 1 Value',
    'FXO': 'Trade Party 1 Value',
    'IR': ''
}

PARTY_2_ACCOUNT_NUMBER = {
    'CO': 'Trade Party 2 Account',
    'CR': 'Trade Party 2 Value',
    'EQD': 'Party 2',
    'EQS': 'Party 2',
    'FXC': 'Trade Party 2 Value',
    'FXO': 'Trade Party 2 Value',
    'IR': 'Counterparty UCI',
}

TRADE_REF = {
    'CO': 'Trade Ref',
    'CR': 'MS Internal Trade Name',
    'EQD': 'Trade Ref',
    'EQS': 'Source System Id',
    'FXC': 'Order Number',
    'FXO': 'Trade ID',
    'IR': 'MS Trade Name',
}

HARMONIZED_UTI_PREFIX = {
    'CO': 'Harmonized UTI Prefix',
    'CR': 'Harmonized UTI Prefix',
    'EQD': 'HUTI LEI',
    'EQS': 'HUTI Prefix',
    'FXC': 'Harmonized UTI Prefix',
    'FXO': 'Harmonized UTI Prefix',
    'IR': 'Harmonized UTI Prefix',
    'FX': 'Harmonized UTI Prefix'
}

HARMONIZED_UTI_VALUE = {
    'CO': 'Harmonized UTI Value',
    'CR': 'Harmonized UTI Value',
    'EQD': 'HUTI suffix',
    'EQS': 'HUTI Value',
    'FXC': 'Harmonized UTI Value',
    'FXO': 'Harmonized UTI Value',
    'IR': 'Harmonized UTI Value',
    'FX': 'Harmonized UTI Value',
}

PRIOR_HARMONIZED_UTI_PREFIX = {
    'CO': 'Harmonized Prior UTI Prefix',
    'CR': 'Harmonized Prior UTI Prefix',
    'EQD': 'Prior HUTI LEI',
    'EQS': 'Prior HUTI Prefix',
    'FXC': 'Harmonized Prior UTI Prefix',
    'FXO': 'Harmonized Prior UTI Prefix',
    'IR': 'Harmonized Prior UTI Prefix'
}

PRIOR_HARMONIZED_UTI_VALUE = {
    'CO': 'Harmonized Prior UTI Value',
    'CR': 'Harmonized Prior UTI Value',
    'EQD': 'Prior HUTI suffix',
    'EQS': 'Prior HUTI Value',
    'FXC': 'Harmonized Prior UTI Value',
    'FXO': 'Harmonized Prior UTI Value',
    'IR': 'Harmonized Prior UTI Value'
}

BOOK = {
    'CO': 'Book Value',
    'CR': 'Book',
    'EQD': '',
    'EQS': '',
    'FXC': 'Book',
    'FXO': 'Book',
    'IR': 'Trading Book',
}

TRADER_ID = {
    'CO': 'Trader Id',
    'CR': 'Trader ID',
    'EQD': 'Trader Id',
    'EQS': 'Trader Id',
    'FXC': 'Trader ID',
    'FXO': 'Trader ID',
    'IR': 'Trader ID',
}

BOOK_LOCATION = {
    'CO': 'Book Location',
    'CR': 'Book Live Location',
    'EQD': '',
    'EQS': '',
    'FXC': 'Book Location',
    'FXO': 'Book Location',
    'IR': 'Book Location'
}

PARTY1_LEI = {
    'CO': 'MS Legal Entity LEI',
    'CR': 'MS Legal Entity LEI',
    'EQD': '',
    'EQS': '',
    'FXC': 'MS Legal Entity LEI',
    'FXO': 'MS Legal Entity LEI',
    'IR': 'MS Legal Entity LEI',
    'FX': 'MS Legal Entity LEI'
}

PARTY2_LEI = {
    'CO': '',
    'CR': 'Party 2 LEI',
    'EQD': '',
    'EQS': '',
    'FXC': '',
    'FXO': '',
    'IR': ''
}
