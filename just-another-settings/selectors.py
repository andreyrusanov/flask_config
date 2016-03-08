import os


class NoSuchSettings(Exception):
    pass


class BaseSelector(object):
    __settings = dict()

    def __init__(self, default=None, **settings):
        """
        :param str or None default: default value if variable not set
        :param settings: dict of variable_value=settings_class pairs
        :return:
        """
        self.default = default
        self.register(**settings)

    def choose(self, *args, **kwargs):
        raise NotImplementedError

    def register(self, **settings):
        self.__settings.update(settings)

    def __call__(self, *args, **kwargs):
        return self.choose(*args, **kwargs)

    def __getitem__(self, item):
        return self.__settings[item]

    def get(self, item, default=None):
        return self.__settings.get(item, default)

    def __contains__(self, item):
        return item in self.__settings


class EnvSelector(BaseSelector):

    def __init__(self, variable, default=None, **settings):
        """

        :param str variable: name of env variable
        :param str or None default: default value if variable not set
        :param settings: dict of variable_value=settings_class pairs
        :return:
        """
        self.variable = variable
        super(EnvSelector, self).__init__(default, **settings)

    def choose(self):
        mode = os.getenv(self.variable, self.default)
        if not mode or mode not in self.__settings:
            raise NoSuchSettings
        return self.__settings.get(mode)


class ValueSelector(BaseSelector):
    def choose(self, mode):
        if mode not in self.__settings:
            raise NoSuchSettings
        return self.__settings.get(mode)
