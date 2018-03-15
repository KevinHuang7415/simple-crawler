'''
Helper functions for built-in logging module.
'''
import logging
import logging.config
from pysite.loggers.helpers import LOGGING as LOG_SETTING
import pysite.loggers.helpers as log_helper


get_logger = log_helper.get_logger
stop_log = log_helper.stop_log


def load_config():
    '''Load configuration for logging.'''
    logging.config.dictConfig(LOG_SETTING)


def shutdown():
    '''Terminate logging action.'''
    logging.shutdown()
