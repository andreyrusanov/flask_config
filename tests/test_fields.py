import os
from unittest import TestCase

from just_another_settings import EnvField


class TestEnvField(TestCase):
    def setUp(self):
        self.var = 'TEST_ENV_VAR'
        self.value = 'env_var_value'
        os.environ[self.var] = self.value
        self.addCleanup(self.cleanup_env, self.var)

    @staticmethod
    def cleanup_env(var):
        if var in os.environ:
            del os.environ[var]

    def test__set__(self):
        class Settings(object):
            field = EnvField(self.var)
        settings = Settings()

        with self.assertRaises(TypeError):
            settings.field = 1

    def test__get__(self):
        class Settings(object):
            field = EnvField(self.var)
        settings = Settings()
        self.assertEqual(settings.field, self.value)

    def test__get__default(self):
        default = 'default_value'

        class Settings(object):
            field = EnvField('just-another-var', default)

        settings = Settings()
        self.assertEqual(settings.field, default)

    def test__not_none_false(self):

        class Settings(object):
            field = EnvField('just-another-var', not_none=False)

        settings = Settings()
        self.assertIsNone(settings.field)

    def test__not_none_true(self):

        class Settings(object):
            field = EnvField('just-another-var', not_none=True)

        settings = Settings()
        with self.assertRaises(ValueError):
            settings.field
