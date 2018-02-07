'''
Helper functions for built-in logging module.
'''
import logging
import logging.config as loggingconfig
import log_config


def load_config():
    '''Load configuration for logging.'''
    loggingconfig.dictConfig(log_config.LOGGING)


def get_logger(module_name):
    '''Get logger with certain name.'''
    return logging.getLogger('.'.join(['crawler', module_name]))


def stop_log(module_name):
    '''Prevent log for module.'''
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.CRITICAL)
    logger.addFilter(logging.NullHandler())
    logger.propagate = False
