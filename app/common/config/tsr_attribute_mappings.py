"""
This file contains tsr attributes and their mapping across regimes.
"""

from common import constants

# Used for Segregating EQ trades in EQS / EQD or FX trades in FXC / FXO
PRODUCT_TAXONOMY = {
    constants.ASIC: 'Unique product identifier',
    constants.JFSA: 'Contract type',
    constants.MAS: 'Unique Product Identifier',
}

# List of columns containing LEI values in Trade State Report (TSR)
TSR_COLUMNS_WITH_LEI = {
    constants.JFSA: ['Entity responsible for reporting', 'Counterparty 1 (reporting counterparty)', 'Counterparty 2',
                     'Submitter identifier', 'Other payment payer', 'Other payment receiver', 'Custom basket code LEI'],

    constants.ASIC: ['Report submitting entity', 'Reporting Entity', 'Counterparty 1', 'Counterparty 2', 'Broker',
                     'Other payment payer', 'Other payment receiver', 'Custom basket code LEI', 'Event identifier'],

    constants.MAS: ['Data submitter', 'Reporting specified person', 'Counterparty 1', 'Counterparty 2',
                    'Package Identifier', 'Central counterparty', 'Clearing member', 'Other payment payer',
                    'Other payment receiver'],

    constants.EMIR_REFIT: ['Report submitting entity ID', 'Entity responsible for reporting', 'Execution Agent ID',
                           'Counterparty 1 (Reporting counterparty)', 'Counterparty 2', 'Clearing member',
                           'Beneficiary ID', 'Central counterparty', 'PTRR service provider', 'Other payment payer',
                           'Other payment receiver', 'Reference entity']
}

# List of columns containing LEI values in Trade Activity Report (TAR)
TAR_COLUMNS_WITH_LEI = {
    constants.EMIR_REFIT: ['Report submitting entity ID', 'Entity responsible for reporting',
                           'Counterparty 1 (Reporting counterparty)', 'Counterparty 2', 'Broker ID', 'Clearing member',
                           'Central counterparty']
}

# List of columns containing LEI values in Margin State Report (MSR)
MSR_COLUMNS_WITH_LEI = {
    constants.JFSA: ['Entity responsible for reporting', 'Counterparty 1 (reporting counterparty)', 'Counterparty 2',
                     'Submitter identifier'],

    constants.ASIC: ['Reporting Entity', 'Counterparty 1', 'Counterparty 2', 'Report submitting entity'],

    constants.MAS: ['Reporting specified person', 'Counterparty 1', 'Counterparty 2', 'Data submitter'],

    constants.EMIR_REFIT: ['Report submitting entity ID', 'Entity responsible for reporting', 'Execution Agent ID',
                           'Counterparty 1 (Reporting counterparty)', 'Counterparty 2']
}
