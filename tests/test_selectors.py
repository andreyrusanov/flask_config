import os
from unittest import TestCase

from mock import Mock

from just_another_settings.selectors import EnvSelector, ValueSelector, NoSuchSettings


class TestEnvSelector(TestCase):
    def setUp(self):
        self.var = 'environ-test-var'
        self.addCleanup(self.cleanup_env, self.var)

    @staticmethod
    def cleanup_env(var):
        if var in os.environ:
            del os.environ[var]

    def test_choose(self):
        os.environ[self.var] = 'mode2'
        mode1 = Mock()
        mode2 = Mock()
        selector = EnvSelector(self.var, None, mode1=mode1, mode2=mode2)
        choice = selector.choose()
        self.assertIsNot(choice, mode1)
        self.assertIs(choice, mode2)

    def test_choose_default(self):
        self.assertNotIn(self.var, os.environ)
        mode1 = Mock()
        mode2 = Mock()
        selector = EnvSelector(self.var, 'mode1', mode1=mode1, mode2=mode2)
        choice = selector.choose()
        self.assertIs(choice, mode1)
        self.assertIsNot(choice, mode2)

    def test_missing(self):
        with self.assertRaises(NoSuchSettings):
            selector = EnvSelector(self.var)
            selector.choose()


class TestValueSelector(TestCase):
    def test_choose(self):
        mode1 = Mock()
        mode2 = Mock()
        selector = ValueSelector(mode1=mode1, mode2=mode2)
        choice = selector.choose('mode2')
        self.assertIsNot(choice, mode1)
        self.assertIs(choice, mode2)

    def test_choose_default(self):
        mode1 = Mock()
        mode2 = Mock()
        selector = ValueSelector('mode2', mode1=mode1, mode2=mode2)
        choice = selector.choose()
        self.assertIsNot(choice, mode1)
        self.assertIs(choice, mode2)

    def test_missing(self):
        with self.assertRaises(NoSuchSettings):
            selector = ValueSelector()
            selector.choose('missing_mode')
