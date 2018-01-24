'''
Helper functions for built-in logging module.
'''
import logging
import log_config

def load_config():
    '''Load configuration for logging.'''
    logging.config.dictConfig(log_config.LOGGING)


def get_logger(module_name):
    '''Get logger with certain name.'''
    return logging.getLogger('.'.join(['crawler', module_name]))
