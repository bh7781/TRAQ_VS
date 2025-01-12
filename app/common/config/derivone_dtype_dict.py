from common import constants

derivone_dtype = {
    constants.COMMODITY: {
        'USI Prefix': 'string',
        'USI Value': 'string',
        'UTI Prefix': 'string',
        'Harmonized UTI Prefix': 'string',
        'Harmonized UTI Value': 'string',
        'MS Legal Entity LEI': 'string',
        'Party 2 LEI': 'string',
        'Identifier of Counterparty 1': 'string',
        'Trade Party 1 Account': 'string',
        'Trade Party 2 Account': 'string',
        'Trade Ref': 'string',
        'Prior HUTI Prefix': 'string',
        'Prior HUTI Value': 'string',
        'Book Value': 'string',
        'Trader Id': 'string',
        'Book Location': 'string'
    },

    constants.CREDIT: {
        'USI Prefix': 'string',
        'USI Value': 'string',
        'UTI Prefix': 'string',
        'Harmonized UTI Prefix': 'string',
        'Harmonized UTI Value': 'string',
        'MS Legal Entity LEI': 'string',
        'Party 2 LEI': 'string',
        'Trade Party 1 Value': 'string',
        'Trade Party 2 Value': 'string',
        'MS Internal Trade Name': 'string',
        'Prior HUTI Prefix': 'string',
        'Prior HUTI Value': 'string',
        'Book': 'string',
        'Trader ID': 'string',
        'Book Live Location': 'string'
    },

    constants.EQUITY_DERIVATIVES: {
        'USI Prefix': 'string',
        'USI Value': 'string',
        'UTI Prefix': 'string',
        'HUTI LEI': 'string',
        'HUTI suffix': 'string',
        'MS Legal Entity LEI': 'string',
        'Party 2 LEI': 'string',
        'Party 1': 'string',
        'Party 2': 'string',
        'Trade Ref': 'string',
        'Prior HUTI LEI': 'string',
        'Prior HUTI suffix': 'string',
        'Trader Id': 'string'
    },

    constants.EQUITY_SWAPS: {
        'USI Prefix': 'string',
        'USI Value': 'string',
        'UTI Prefix': 'string',
        'HUTI Prefix': 'string',
        'HUTI Value': 'string',
        'MS Legal Entity LEI': 'string',
        'Party 2 LEI': 'string',
        'Party 1': 'string',
        'Party 2': 'string',
        'Source System Id': 'string',
        'Prior HUTI Prefix': 'string',
        'Prior HUTI Value': 'string',
        'Trader Id': 'string'
    },

    constants.FOREIGN_EXCHANGE: {
        'USI Prefix': 'string',
        'USI Value': 'string',
        'UTI Prefix': 'string',
        'Harmonized UTI Prefix': 'string',
        'Harmonized UTI Value': 'string',
        'MS Legal Entity LEI': 'string',
        'Party 2 LEI': 'string',
        'Trade Party 1 Value': 'string',
        'Trade Party 2 Value': 'string',
        'Order Number': 'string',
        'Prior HUTI Prefix': 'string',
        'Prior HUTI Value': 'string',
        'Book': 'string',
        'Trader ID': 'string',
        'Book Location': 'string'
    },

    constants.INTEREST_RATES: {
        'USI Prefix': 'string',
        'USI Value': 'string',
        'UTI Prefix': 'string',
        'Harmonized UTI Prefix': 'string',
        'Harmonized UTI Value': 'string',
        'MS Legal Entity LEI': 'string',
        'Party 2 LEI': 'string',
        'Data Submitter UCI': 'string',
        'Counterparty UCI': 'string',
        'MS Trade Name': 'string',
        'Prior HUTI Prefix': 'string',
        'Prior HUTI Value': 'string',
        'Trading Book': 'string',
        'Trader ID': 'string',
        'Book Location': 'string'
    }
}
