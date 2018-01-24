'''
Controller for database services.
'''
from enum import Enum
import time
import win32serviceutil
import pywintypes
import logger

LOGGER = logger.get_logger(__package__, __name__)

class StatusCode(Enum):
    ''''Enumeration of service status code.'''
    SERVICE_STOPPED = 0x00000001
    SERVICE_START_PENDING = 0x00000002
    SERVICE_STOP_PENDING = 0x00000003
    SERVICE_RUNNING = 0x00000004
    SERVICE_CONTINUE_PENDING = 0x00000005
    SERVICE_PAUSE_PENDING = 0x00000006
    SERVICE_PAUSED = 0x00000007

POSTGRESQL = [
    'postgresql-x64-10',
    'pgAgent',
    'pgbouncer'
]

SERVICES = [*POSTGRESQL]

START = 'start'
STOP = 'stop'
RESTART = 'restart'

COMMANDS = {
    START: {
        'api': win32serviceutil.StartService,
        'errno': 1056,  # already running
        'status': StatusCode.SERVICE_RUNNING
    },
    STOP: {
        'api': win32serviceutil.StopService,
        'errno': 1062,  # not running
        'status': StatusCode.SERVICE_STOPPED
    },
    RESTART: {
        'api': win32serviceutil.RestartService,
        'errno': None,  # dont care
        'status': StatusCode.SERVICE_RUNNING
    }
}


def service_operation(cmd):
    '''Operations for services.'''
    command = COMMANDS[cmd]
    api = command['api']
    errno = command['errno']

    for service in SERVICES:
        try:
            api(service)
        except pywintypes.error as err:
            if errno and errno == err.winerror:
                pass
            else:
                LOGGER.error(
                    'Operation [%s] to database service failed :{1}', cmd,
                    exc_info=True
                )


def launch_database():
    '''Start services.'''
    LOGGER.info('Launch database services.')
    service_operation(RESTART)
    time.sleep(1)


def terminate_database():
    '''Stop services.'''
    LOGGER.info('Terminate database services.')
    service_operation(STOP)
    time.sleep(0.3)


def query_status(service_name):
    '''Query service status.'''
    try:
        raw_status = win32serviceutil.QueryServiceStatus(service_name)[1]
        return StatusCode(raw_status)
    except pywintypes.error:
        LOGGER.warning('Failed to query status of service [%s]')
        raise OSError
