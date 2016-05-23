import json
import os


class BaseField(object):

    def __init__(self, not_none=True):
        self.not_none = not_none
        self.value = self._fetch_value()

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = value

    def _fetch_value(self):
        return self.validate(self.fetch_value())

    def validate(self, value):
        if value is None and self.not_none:
            raise ValueError('Wrong value')

    def fetch_value(self):
        raise NotImplementedError


class EnvField(BaseField):
    def __init__(self, variable, default=None, *args, **kwargs):
        self.variable = variable
        self.default = default
        super(EnvField, self).__init__(*args, **kwargs)

    def fetch_value(self):
        return os.getenv(self.variable, self.default)

    def __set__(self, instance, value):
        raise TypeError('Can not assign value to env field')


class BaseFileField(BaseField):
    def __init__(self, path):
        self.path = path
        super(BaseFileField, self).__init__()

    def open(self):
        with open(self.path) as f:
            return f.read()

    def parse_file(self, data):
        raise NotImplementedError

    def fetch_value(self):
        return self.parse_file(self.open())


class JSONFileField(BaseFileField):
    def open(self):
        return json.load(self.path)

    def parse_file(self, data):
        return data
