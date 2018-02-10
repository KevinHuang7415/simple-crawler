'''
Controller for database services which run on Windows platform.
'''
from enum import IntEnum
import time
import win32serviceutil
import pywintypes
import logger

LOGGER = logger.get_logger(__name__)


class StatusCode(IntEnum):
    ''''Enumeration of service status code.'''
    SERVICE_UNKNOWN = 0x00000000
    SERVICE_STOPPED = 0x00000001
    SERVICE_START_PENDING = 0x00000002
    SERVICE_STOP_PENDING = 0x00000003
    SERVICE_RUNNING = 0x00000004
    SERVICE_CONTINUE_PENDING = 0x00000005
    SERVICE_PAUSE_PENDING = 0x00000006
    SERVICE_PAUSED = 0x00000007


class ErrorCode(IntEnum):
    '''Enumeration of service error code.'''
    ERROR_SERVICE_ALREADY_RUNNING = 0x420
    ERROR_SERVICE_NOT_ACTIVE = 0x426


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
        'errno': ErrorCode.ERROR_SERVICE_ALREADY_RUNNING,
        'status': StatusCode.SERVICE_RUNNING
    },
    STOP: {
        'api': win32serviceutil.StopService,
        'errno': ErrorCode.ERROR_SERVICE_NOT_ACTIVE,
        'status': StatusCode.SERVICE_STOPPED
    },
    RESTART: {
        'api': win32serviceutil.RestartService,
        'errno': ErrorCode.ERROR_SERVICE_ALREADY_RUNNING,
        'status': StatusCode.SERVICE_RUNNING
    }
}


def service_operation(service, cmd):
    '''Operations for services.'''
    command = COMMANDS[cmd]
    api = command['api']
    errno = command['errno']
    status = command['status']

    try:
        api(service)
    except pywintypes.error as err:
        if errno.value == err.winerror:
            pass
        else:
            LOGGER.exception(
                'Operation [%s] to database service failed.',
                cmd
            )
            raise OSError

    for _ in range(16):
        now_status = query_status(service)
        if now_status == status:
            break
        time.sleep(0.25)
    else:
        LOGGER.warning(
            'Failed to change service [%s] to status [%s]',
            service,
            cmd
        )
        raise OSError


def launch_database():
    '''Start services.'''
    LOGGER.info('Launch database services.')
    for service in SERVICES:
        service_operation(service, START)


def terminate_database():
    '''Stop services.'''
    LOGGER.info('Terminate database services.')
    for service in SERVICES:
        service_operation(service, STOP)


def query_status(service_name):
    '''Query service status.'''
    try:
        raw_status = win32serviceutil.QueryServiceStatus(service_name)[1]
        return StatusCode(raw_status)
    except pywintypes.error:
        LOGGER.warning('Failed to query status of service [%s]')
        return StatusCode.SERVICE_UNKNOWN
