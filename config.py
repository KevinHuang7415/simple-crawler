'''
Configuration utility module.
'''
import configparser
import logging
import os
import singleton

DEFAULT_FILE = r'config\ptt_crawler.conf'
LOGGER = logging.getLogger('.'.join(['crawler', __name__]))
DEFAULT_CONFIGS = {
    'Crawler': {
        'term_date': 10,
        'board': 'Soft_Job',
        'data_path': 'data',
    }
}


class Config(singleton.Singleton):
    """description of class"""

    PATH = None

    def __init__(self):
        if not self.PATH:
            self.config = configparser.ConfigParser()
            self.__use_default = False

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'{self.PATH!r}, {self.__use_default!r})'
        )

    @property
    def use_default(self):
        '''Getter of use_default'''
        return self.__use_default

    @use_default.setter
    def use_default(self, value):
        '''Setter of use_default'''
        if self.__use_default != value:
            self.config.clear()

            if value is True:
                self.config.read_dict(DEFAULT_CONFIGS)

        self.__use_default = value

    def load(self, path=DEFAULT_FILE):
        '''Load the configuration file.'''
        self.PATH = os.path.abspath(path)

        if not self.config.read(self.PATH):
            msg = 'Failed to open configuration file: {0}'.format(self.PATH)
            raise ValueError(msg)

    def __get_value(self, method, section, option):
        '''Fetch a value from configuration.'''
        try:
            return method(section, option)
        except configparser.NoSectionError:
            LOGGER.error('Section [%s] not exists.', section)
            return None
        except configparser.NoOptionError:
            LOGGER.error(
                'Option [%s] not exists in section [%s].',
                option, section
            )
            return None

    def get(self, section, option):
        '''Fetch a string value from configuration.'''
        return self.__get_value(self.config.get, section, option)

    def getint(self, section, option):
        '''Fetch a integer value from configuration.'''
        return self.__get_value(self.config.getint, section, option)

    def getbool(self, section, option):
        '''Fetch a boolean value from configuration.'''
        return self.__get_value(self.config.getboolean, section, option)
