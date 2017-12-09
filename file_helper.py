import errno
import os
from os import path
import re

DEFAULT_DIR = '.'

def get_dir(argv):
    if (len(argv) > 1 and path.isdir(argv[1])):
        return argv[1]
    else:
        return DEFAULT_DIR

def format_filename(title):
    pattern = re.compile(r'[.\\/:*?"<>|\r\n]')
    return pattern.sub('', title)


def create_dir_if_not_exist(dir_path):
    try:
        os.makedirs(dir_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def write_article(article, title, dir_path):
    filename = format_filename(title) + '.txt'
    
    with open(path.join(dir_path, filename), 'w', encoding='utf-8') as f:
        try:
            f.write(article)
        except Exception as e:
            print('Failed to write file "' + filename + '": ' + e.reason)