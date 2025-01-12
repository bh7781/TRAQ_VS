from common import constants

# Define matching keys for different regulators and optionally for specific asset classes
matching_keys = {
    constants.JFSA: {
        'default': [
            ('matching_key_uti', 'matching_key_huti'),
            ('matching_key_uti', 'matching_key_uti'),
            ('matching_key_uti', 'matching_key_usi'),
            ('matching_key_uti', 'matching_key_usi_value'),
            ('matching_key_uti', 'matching_key_uti_value'),
        ],

        constants.INTEREST_RATES: [
            ('matching_key_uti', 'matching_key_huti'),
            ('matching_key_uti', 'matching_key_uti'),
            ('matching_key_uti', 'matching_key_usi'),
            ('matching_key_uti', 'matching_key_usi_value'),
            ('matching_key_uti', 'matching_key_uti_value'),

            ('matching_key_straddle_uti', 'matching_key_huti'),
            ('matching_key_straddle_uti', 'matching_key_uti'),
            ('matching_key_straddle_uti', 'matching_key_usi'),
            ('matching_key_straddle_uti', 'matching_key_usi_value'),
            ('matching_key_straddle_uti', 'matching_key_uti_value'),
        ]
    },

    constants.ASIC: {
        'default': [
            ('matching_key_uti', 'matching_key_huti'),
            ('matching_key_uti', 'matching_key_uti'),
            ('matching_key_uti', 'matching_key_usi'),
        ],
    },

    constants.MAS: {
        'default': [
            ('matching_key_uti', 'matching_key_huti'),
            ('matching_key_uti', 'matching_key_uti'),
            ('matching_key_uti', 'matching_key_usi'),
        ],
    },

    constants.EMIR_REFIT: {
        'default': [
            ('matching_key_uti', 'matching_key_huti'),
            ('matching_key_uti', 'matching_key_uti'),
            ('matching_key_uti', 'matching_key_usi'),
        ],

        constants.INTEREST_RATES: [
            ('matching_key_uti', 'matching_key_huti'),
            ('matching_key_uti', 'matching_key_uti'),
            ('matching_key_uti', 'matching_key_usi'),

            ('matching_key_uti', 'matching_key_huti_dir'),
            ('matching_key_uti', 'matching_key_uti_dir'),
            ('matching_key_uti', 'matching_key_usi_dir'),
        ]
    }
}


def get_matching_keys_for_regulator(regulator, asset_class=None):
    """
    Get the matching keys for the specified regulator and asset class.
    """
    regulator_keys = matching_keys.get(regulator, {})

    if asset_class and asset_class in regulator_keys:
        return regulator_keys[asset_class]
    else:
        return regulator_keys.get('default', [])
