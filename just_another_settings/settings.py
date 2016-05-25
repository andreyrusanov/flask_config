import logging

from .fields import BaseField

class Setting(object):
    logger = logging.getLogger(__name__)

    def load(self):
        for variable, value in self.__dict__.items():
            if isinstance(value, BaseField):
                # load value
                value = self.__dict__[variable].value
                self.logger.info('Setting item {} loaded'.format(variable))
