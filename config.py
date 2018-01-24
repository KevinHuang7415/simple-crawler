'''
Configuration utility module.
'''
import configparser
import os
import singleton
import logger

LOGGER = logger.get_logger(__name__)

DEFAULT_FILE = r'config\ptt_crawler.conf'

DEFAULT_CONFIGS = {
    'Crawler': {
        'term_date': 10,
        'board': 'Soft_Job',
        'data_path': 'data_txt',
    }
}


class Config(singleton.Singleton):
    """description of class"""

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.path = None

    def __repr__(self):
        return f'{self.__class__.__name__}('f'{self.path!r})'

    def load_default(self):
        '''Load configuration using default dictionary.'''
        self.config.clear()
        self.config.read_dict(DEFAULT_CONFIGS)

    def load(self, path=DEFAULT_FILE):
        '''Load the configuration file.'''
        new_path = os.path.abspath(path)
        new_config = configparser.ConfigParser()

        if not new_config.read(new_path):
            msg = 'Failed to open configuration file: {0}'.format(new_path)
            raise ValueError(msg)

        self.config = new_config
        self.path = new_path

    @staticmethod
    def __get_value(method, section, option):
        '''Fetch a value from configuration.'''
        try:
            return method(section, option)
        except configparser.NoSectionError:
            LOGGER.error('Section [%s] not exists.', section)
            raise
        except configparser.NoOptionError:
            LOGGER.error(
                'Option [%s] not exists in section [%s].',
                option, section
            )
            raise
        except ValueError:
            LOGGER.error('Inconsistent type between method and option value.')
            raise

    def get(self, section, option):
        '''Fetch a string value from configuration.'''
        return self.__get_value(self.config.get, section, option)

    def getint(self, section, option):
        '''Fetch a integer value from configuration.'''
        return self.__get_value(self.config.getint, section, option)

    def getbool(self, section, option):
        '''Fetch a boolean value from configuration.'''
        return self.__get_value(self.config.getboolean, section, option)
