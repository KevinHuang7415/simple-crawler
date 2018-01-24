'''
Unit tests for ptt module.
'''
import logging
import time
import unittest
import win32serviceutil
import data.services as srv

logging.disable(logging.CRITICAL)


class ServicesTestCase(unittest.TestCase):
    '''Test cases for data.services.'''

    def test_service_operation(self):
        '''Unit test for data.services.service_operation.'''
        service_name = srv.SERVICES[0]

        srv.service_operation(service_name, srv.START)
        time.sleep(1)
        self.query_status(service_name, srv.StatusCode.SERVICE_RUNNING)

        srv.service_operation(service_name, srv.STOP)
        time.sleep(0.3)
        self.query_status(service_name, srv.StatusCode.SERVICE_STOPPED)

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
        self.query_status('AudioSrv', srv.StatusCode.SERVICE_RUNNING)

        with self.assertRaises(OSError):
            srv.query_status('NoThisService')

    def query_status(self, service_name, expect):
        '''A helper function for test_query_status.'''
        status = srv.query_status(service_name)
        self.assertEqual(status, expect)


if __name__ == '__main__':
    unittest.main()
