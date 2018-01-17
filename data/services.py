'''
Controller for database services.
'''
# import sys
import logging
import time
import win32serviceutil
import pywintypes

if __package__:
    LOGGER = logging.getLogger('.'.join(['crawler', __package__, __name__]))
else:
    LOGGER = logging.getLogger('.'.join(['crawler', __name__]))

POSTGRESQL = [
    'postgresql-x64-10',
    'pgAgent',
    'pgbouncer'
]

SERVICES = [*POSTGRESQL]

COMMANDS = {
    "st": {
        'api': win32serviceutil.StartService, 'errno': 1056  # already running
    },
    "sp": {
        'api': win32serviceutil.StopService, 'errno': 1062  # not running
    },
    "re": {
        'api': win32serviceutil.RestartService, 'errno': None  # dont care
    }
}


def service_operation(arg):
    '''Operations for services.'''
    command = COMMANDS[arg]
    api = command['api']
    errno = command['errno']

    for service in SERVICES:
        try:
            api(service)
        except pywintypes.error as err:
            if err.winerror == errno:
                pass
            else:
                LOGGER.error(
                    'Operation [%s] to database service failed :{1}', arg,
                    exc_info=True
                )


def start():
    '''Start services.'''
    service_operation('re')
    time.sleep(1)


def stop():
    '''Stop services.'''
    service_operation('sp')
    time.sleep(0.3)
