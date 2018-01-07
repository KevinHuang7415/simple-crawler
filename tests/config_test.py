'''
Unit tests for config module.
'''
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
        with self.assertRaises(ValueError):
            self.config.load('no_this_config')

        self.config.load()
        self.assertTrue(self.config.config.has_option('Crawler', 'board'))

        self.config.load(os.path.abspath(self.config_name))
        self.assertTrue(self.config.config.has_section('Test'))

    def test_get(self):
        '''Unit test for config.get.'''
        method = self.config.get
        self.get_value(method, 'Test', 'str', 'string')
        self.get_value(method, 'NO', 'bool', None)
        self.get_value(method, 'Test', 'long', None)

    def test_getint(self):
        '''Unit test for config.getint.'''
        method = self.config.getint
        self.get_value(method, 'Test', 'int', 5)
        self.get_value(method, 'NO', 'bool', None)
        self.get_value(method, 'Test', 'long', None)

    def test_getbool(self):
        '''Unit test for config.getbool.'''
        method = self.config.getbool
        self.get_value(method, 'Test', 'bool', False)
        self.get_value(method, 'NO', 'bool', None)
        self.get_value(method, 'Test', 'long', None)

    def get_value(self, method, section, option, value):
        '''A helper function for all get type funcions.'''
        self.assertEqual(method(section, option), value)


if __name__ == '__main__':
    unittest.main()
