'''
Filters for logging.
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
