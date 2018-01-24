'''
Unit tests for ptt module.
'''
import logging
import unittest
import win32serviceutil
import data.services as srv

logging.disable(logging.CRITICAL)


class ServicesTestCase(unittest.TestCase):
    '''Test cases for data.services.'''

    def test_launch_database(self):
        '''Unit test for data.services.launch_database.'''
        srv.launch_database()
        for service in srv.SERVICES:
            self.assertEqual(
                win32serviceutil.QueryServiceStatus(service)[1],
                srv.StatusCode.SERVICE_RUNNING.value
            )

    def test_terminate_database(self):
        '''Unit test for data.services.terminate_database.'''
        srv.terminate_database()
        for service in srv.SERVICES:
            self.assertEqual(
                win32serviceutil.QueryServiceStatus(service)[1],
                srv.StatusCode.SERVICE_STOPPED.value
            )

    def test_query_status(self):
        '''Unit test for data.services.query_status'''
        status = srv.query_status('AudioSrv')
        self.assertEqual(status, srv.StatusCode.SERVICE_RUNNING)

        with self.assertRaises(OSError):
            srv.query_status('NoThisService')


if __name__ == '__main__':
    unittest.main()
