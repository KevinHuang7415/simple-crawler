'''
Helper functions for built-in logging module.
'''
import logging
from .filter import PackageFilter


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'filters': {
        'packageFilter': {
            '()': PackageFilter,
            "param": "crawler."
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'INFO',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'level': 'DEBUG',
            'filename': 'log\\ptt.log',
            'mode': 'a',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'crawler.console': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'INFO',
            'filters': ['packageFilter']
        },
        'crawler.file': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
            'filters': ['packageFilter']
        }
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG'
    }
}


def get_logger(module_name):
    '''Get logger with certain name.'''
    return logging.getLogger('.'.join(['crawler', module_name]))


def stop_log(module_name):
    '''Prevent log for module.'''
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.CRITICAL)
    logger.addFilter(logging.NullHandler())
    logger.propagate = False
