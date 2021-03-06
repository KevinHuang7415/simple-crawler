'''
Helper functions for file operations.
'''
import errno
import os
from os import path
import re
import logger

LOGGER = logger.get_logger(__name__)

_PATTERN = re.compile(r'[.\\/:*?"<>|\r\n]')


def format_filename(name):
    '''Make the name matches file naming restriction.'''
    return _PATTERN.sub('', name)


def create_dir_if_not_exist(dir_path):
    '''Create the directory if it does not exist.'''
    LOGGER.info('create directory [%s].', dir_path)

    try:
        os.makedirs(dir_path)
    except OSError as err:
        if err.errno != errno.EEXIST:
            LOGGER.exception('Failed to write file.')
            raise


def write_article(article, title, dir_path):
    '''Write article to file.'''
    filename = format_filename(title) + '.txt'

    with open(path.join(dir_path, filename), 'w', encoding='utf-8') as file:
        LOGGER.debug('Write article with filename [%s].', filename)
        try:
            file.write(article)
        except Exception:
            LOGGER.exception('Failed to write file.')
