'''
Unit tests for Singleton module.
'''
import unittest
from singleton import Singleton


class SingletonTestCase(unittest.TestCase):
    '''Test cases for Singleton.'''

    def test_new(self):
        '''Unit test for SoftJob_Crawler.__new__.'''
        singleton_one = Singleton()
        singleton_two = Singleton()
        self.assertEqual(singleton_one, singleton_two)


if __name__ == '__main__':
    unittest.main()
