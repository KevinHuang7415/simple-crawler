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

    def test_start(self):
        '''Unit test for data.services.start.'''
        srv.start()
        for service in srv.SERVICES:
            self.assertEqual(
                win32serviceutil.QueryServiceStatus(service)[1],
                srv.StatusCode.SERVICE_RUNNING.value
            )

    def test_stop(self):
        '''Unit test for data.services.stop.'''
        srv.stop()
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
