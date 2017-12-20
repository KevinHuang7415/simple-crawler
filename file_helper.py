'''
Helper functions for file operations.
'''

import errno
import os
from os import path
import re
import sys

DEFAULT_DIR = '.'

def get_dir(argv):
    '''Find the directory assigned in arguments.'''
    if (len(argv) > 1 and path.isdir(argv[1])):
        return argv[1]
    else:
        return DEFAULT_DIR

PATTERN = re.compile(r'[.\\/:*?"<>|\r\n]')
def format_filename(name):
    '''Make the name matches file naming restriction.'''
    return PATTERN.sub('', name)


def create_dir_if_not_exist(dir_path):
    '''Create the directory if it does not exist.'''
    try:
        os.makedirs(dir_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def write_article(article, title, dir_path):
    '''Write article to file.'''
    filename = format_filename(title) + '.txt'

    with open(path.join(dir_path, filename), 'w', encoding='utf-8') as f:
        try:
            f.write(article)
        except IOError as e:
            print('I/O error on writing file {0}({1}): {2}'.format(filename, e.errno, e.strerror))
        except:
            print("Unexpected error on writing file {0}:{1}".format(filename, sys.exc_info()[0]))
