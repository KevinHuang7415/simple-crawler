'''
Unit tests for service module.
'''
import logging
import time
import unittest
import win32serviceutil
import data.services as services

logging.disable(logging.CRITICAL)


class ServicesTestCase(unittest.TestCase):
    '''Test cases for data.services.'''

    @classmethod
    def setUpClass(cls):
        services.terminate_database()

    def tearDown(self):
        services.terminate_database()

    def test_service_operation(self):
        '''Unit test for data.services.service_operation.'''
        service_name = services.SERVICES[0]

        services.service_operation(service_name, services.START)
        self.query_status(service_name, services.StatusCode.SERVICE_RUNNING)

        services.service_operation(service_name, services.STOP)
        self.query_status(service_name, services.StatusCode.SERVICE_STOPPED)

    def test_launch_database(self):
        '''Unit test for data.services.launch_database.'''
        services.launch_database()
        for service in services.SERVICES:
            self.query_status(service, services.StatusCode.SERVICE_RUNNING)

    def test_terminate_database(self):
        '''Unit test for data.services.terminate_database.'''
        services.terminate_database()
        for service in services.SERVICES:
            self.query_status(service, services.StatusCode.SERVICE_STOPPED)

    def test_query_status(self):
        '''Unit test for data.services.query_status'''
        self.query_status('AudioSrv', services.StatusCode.SERVICE_RUNNING)

        self.query_status('NoThisService', services.StatusCode.SERVICE_UNKNOWN)

    def query_status(self, service_name, expect):
        '''A helper function for test_query_status.'''
        status = services.query_status(service_name)
        self.assertEqual(status, expect)


if __name__ == '__main__':
    unittest.main()
