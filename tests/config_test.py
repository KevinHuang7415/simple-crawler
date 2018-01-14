'''
Unit tests for config module.
'''
from configparser import NoSectionError, NoOptionError
import logging
import os
import unittest
import config

logging.disable(logging.CRITICAL)


class ConfigTestCase(unittest.TestCase):
    '''Test cases for config.'''

    @classmethod
    def setUpClass(cls):
        '''The class level setup.'''
        cls.config = config.Config()
        cls.config_name = r'tests\test.conf'
        cls.config.load(os.path.abspath(cls.config_name))

    def test_load_default(self):
        '''Unit test for config.load_default.'''
        self.config.load_default()
        self.assertTrue(self.config.config.has_option('Crawler', 'board'))

    def test_load(self):
        '''Unit test for config.load.'''
        path = self.config.path
        with self.assertRaises(ValueError):
            self.config.load('no_this_config')
            self.assertEqual(self.config.path, path)

        path = os.path.abspath(config.DEFAULT_FILE)
        self.config.load()
        self.assertEqual(self.config.path, path)
        self.assertTrue(self.config.config.has_option('Crawler', 'board'))

        path = os.path.abspath(self.config_name)
        self.config.load(path)
        self.assertEqual(self.config.path, path)
        self.assertTrue(self.config.config.has_section('Test'))

    def test_get(self):
        '''Unit test for config.get.'''
        method = self.config.get
        self.get_value(method, 'Test', 'str', 'string')
        self.get_value_error(method, 'NO', 'bool', NoSectionError)
        self.get_value_error(method, 'Test', 'long', NoOptionError)

    def test_getint(self):
        '''Unit test for config.getint.'''
        method = self.config.getint
        self.get_value(method, 'Test', 'int', 5)
        self.get_value_error(method, 'NO', 'bool', NoSectionError)
        self.get_value_error(method, 'Test', 'long', NoOptionError)
        self.get_value_error(method, 'Test', 'str', ValueError)

    def test_getbool(self):
        '''Unit test for config.getbool.'''
        method = self.config.getbool
        self.get_value(method, 'Test', 'bool', False)
        self.get_value_error(method, 'NO', 'bool', NoSectionError)
        self.get_value_error(method, 'Test', 'long', NoOptionError)
        self.get_value_error(method, 'Test', 'str', ValueError)

    def get_value(self, method, section, option, value):
        '''A helper function for all get type funcions.'''
        self.assertEqual(method(section, option), value)

    def get_value_error(self, method, section, option, error):
        '''A helper function for all get type funcions which error raised.'''
        with self.assertRaises(error):
            method(section, option)


if __name__ == '__main__':
    unittest.main()
