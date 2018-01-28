'''
Create configuration for logging.
'''
import logging


class PackageFilter(logging.Filter):
    '''Custom logging filter.'''

    def __init__(self, param='crawler'):
        super().__init__()
        self.param = param

    def filter(self, record):
        if self.param is None:
            return True
        return record.getMessage().startswith(self.param)


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
