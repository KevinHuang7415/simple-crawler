'''
Unit tests for ptt module.
'''
import logging
import unittest
import win32serviceutil
import data.services

logging.disable(logging.CRITICAL)


class ServicesTestCase(unittest.TestCase):
    '''Test cases for data.services.'''

    def test_start(self):
        '''Unit test for data.services.start.'''
        data.services.start()
        for service in data.services.SERVICES:
            self.assertEqual(
                win32serviceutil.QueryServiceStatus(service)[1],
                4  # running
            )

    def test_stop(self):
        '''Unit test for data.services.stop.'''
        data.services.stop()
        for service in data.services.SERVICES:
            self.assertEqual(
                win32serviceutil.QueryServiceStatus(service)[1],
                1  # stopped
            )


if __name__ == '__main__':
    unittest.main()