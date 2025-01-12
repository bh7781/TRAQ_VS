class Config:
    """
    A Singleton configuration class for setting and accessing global configuration parameters.
    This class allows the setting and accessing of configuration parameters such as date, environment, regime,
    and use_case_name.
    The configuration parameters are set when the class is first instantiated and can be accessed
    from anywhere within the program.
    """

    instance = None

    class __Config:
        """
        Class for configuration parameters.
        This class holds the actual configuration parameters, preventing direct access to them.
        """
        def __init__(self, env, regime, run_date, use_case_name=None):
            self.env = env
            self.regime = regime
            self.run_date = run_date
            self.use_case_name = use_case_name

    def __init__(self, env=None, regime=None, run_date=None, use_case_name=None):
        """
        Initializes an instance of Config, or sets parameters on the existing instance.
        If an instance of Config doesn't exist, this initializes it with the given parameters.
        If an instance already exists, this sets the given parameters on it.
        """
        if not Config.instance:
            Config.instance = Config.__Config(env, regime, run_date, use_case_name)
        else:
            if env:
                Config.instance.env = env
            if regime:
                Config.instance.regime = regime
            if regime:
                Config.instance.run_date = run_date
            if use_case_name:
                Config.instance.use_case_name = use_case_name

    def __getattr__(self, name):
        """
        Allows access to the configuration parameters on the inner Config instance.
        This method is called when an attribute lookup has not found the attribute in the usual places.
        """
        return getattr(self.instance, name)
