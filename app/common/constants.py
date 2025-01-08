"""
When changing the values of the constants in this module, ensure to verify the
impacts on all scripts that import and use these 
"""

# Regulators / Regimes
CFTC = 'CFTC'                   # Commodity Futures Trading Commission
SEC = 'SEC'                     # Securities and Exchange Commission
HKMA = 'HKMA'                   # Hong Kong Monetary Authority
EMIR = 'EMIR'                   # European Market Infrastructure Regulation
EMIR_REFIT = 'EMIR_REFIT'       # European Market Infrastructure Regulation REgulatory FITness Program
SFTR = 'SFTR'                   # Securities Financing Transactions Regulation
MIFID = 'MIFID'                 # Markets in Financial Instruments Directive
ASIC = 'ASIC'                   # Australian Securities and Investments Commission
MAS = 'MAS'                     # Monetary Authority of Singapore
BOI = 'BOI'                     # Bank of Israel
JFSA = 'JFSA'                   # Japan Financial Services Agency
CROSS = 'CROSS'                 # All regimes

# Asset Classes
COMMODITY = 'CO'
CREDIT = 'CR'
EQUITY = 'EQ'
EQUITY_DERIVATIVES = 'EQD'
EQUITY_SWAPS = 'EQS'
FOREIGN_EXCHANGE = 'FX'
FOREIGN_EXCHANGE_CASH = 'FXC'
FOREIGN_EXCHANGE_OPTIONS = 'FXO'
INTEREST_RATES = 'IR'
EXCHANGE_TRADES_DERIVATIVES_ACTIVITY = 'ETDACTIVITY'
EXCHANGE_TRADES_DERIVATIVES_POSITION = 'ETDPOSITION'
COLLATERAL = 'COL'

# List of asset classes for each regulator
ASSET_CLASS_LIST = {
    SEC: [CREDIT, EQUITY_DERIVATIVES, EQUITY_SWAPS, INTEREST_RATES],

    CFTC: [COMMODITY, CREDIT, EQUITY_DERIVATIVES, EQUITY_SWAPS, FOREIGN_EXCHANGE, INTEREST_RATES],

    HKMA: [CREDIT, EQUITY_DERIVATIVES, EQUITY_SWAPS, FOREIGN_EXCHANGE, INTEREST_RATES],

    EMIR: [COMMODITY, CREDIT, EQUITY_DERIVATIVES, EQUITY_SWAPS, FOREIGN_EXCHANGE, INTEREST_RATES,
           EXCHANGE_TRADES_DERIVATIVES_POSITION, EXCHANGE_TRADES_DERIVATIVES_ACTIVITY],

    EMIR_REFIT: [COMMODITY, CREDIT, EQUITY_DERIVATIVES, EQUITY_SWAPS, FOREIGN_EXCHANGE, INTEREST_RATES,
                 EXCHANGE_TRADES_DERIVATIVES_POSITION, EXCHANGE_TRADES_DERIVATIVES_ACTIVITY],

    JFSA: [CREDIT, EQUITY_DERIVATIVES, EQUITY_SWAPS, FOREIGN_EXCHANGE, INTEREST_RATES],

    ASIC: [COMMODITY, CREDIT, EQUITY_DERIVATIVES, EQUITY_SWAPS, FOREIGN_EXCHANGE, INTEREST_RATES],

    MAS: [COMMODITY, CREDIT, EQUITY_DERIVATIVES, EQUITY_SWAPS, FOREIGN_EXCHANGE, INTEREST_RATES]
}

# Secondary Asset Classes for FOREIGN_EXCHANGE
FOREIGN_EXCHANGE_SECONDARY_ASSET_CLASS = [FOREIGN_EXCHANGE_CASH, FOREIGN_EXCHANGE_OPTIONS]

# Secondary Asset Classes for EQUITY
EQUITY_SECONDARY_ASSET_CLASS = [EQUITY_DERIVATIVES, EQUITY_SWAPS]

# Asset class MSA codes
ASSET_CLASS_MSA_TMS_CODES = {
    COLLATERAL: '0',
    COMMODITY: '2',
    CREDIT: '3',
    EQUITY: '4',
    FOREIGN_EXCHANGE: '5',
    INTEREST_RATES: '6',
    EXCHANGE_TRADES_DERIVATIVES_POSITION: '7',
    EXCHANGE_TRADES_DERIVATIVES_ACTIVITY: '7',
}

# Report Date line number inside TSR
REPORT_DATE_LINE = {
    JFSA: 1,
    ASIC: 1,
    MAS: 1,
    EMIR_REFIT: 2
}

# Number of lines to skip to get header row from Trade State Report (TSR)
TSR_SKIPROWS = {
    JFSA: 1,
    ASIC: 1,
    MAS: 1,
    EMIR_REFIT: 2
}

# Number of lines to remove from the end to remove '--End of Report--' line from Trade State Report (TSR)
TSR_SKIPFOOTERS = {
    JFSA: 0,
    ASIC: 0,
    MAS: 0,
    EMIR_REFIT: 0
}

# Number of lines to skip to get header row from Margin State Report (MSR)
MSR_SKIPROWS = {
    JFSA: 1,
    ASIC: 1,
    MAS: 1,
    EMIR_REFIT: 2
}

# Number of lines to remove from the end to remove '--End of Report--' line from Margin State Report (MSR)
MSR_SKIPFOOTERS = {
    JFSA: 0,
    ASIC: 0,
    MAS: 0,
    EMIR_REFIT: 0
}
