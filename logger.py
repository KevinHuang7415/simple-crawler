'''
Helper functions for built-in logging module.
'''
import logging
import logging.config


def load_config():
    '''Load configuration for logging.'''

    class PackageFilter(logging.Filter):
        '''Custom logging filter.'''

        def __init__(self, param='crawler'):
            super().__init__()
            self.param = param

        def filter(self, record):
            if self.param is None:
                return True
            return record.getMessage().startswith(self.param)

    logging_config = {
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
    logging.config.dictConfig(logging_config)


def get_logger(module_name):
    '''Get logger with certain name.'''
    return logging.getLogger('.'.join(['crawler', module_name]))


def stop_log(module_name):
    '''Prevent log for module.'''
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.CRITICAL)
    logger.addFilter(logging.NullHandler())
    logger.propagate = False


def shutdown():
    '''Terminate logging action.'''
    logging.shutdown()
