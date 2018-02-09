'''
Public helper functions for unit testing.
'''
import json
import os


TEST_DIR = r'tests\test_data'


def read_file(filename):
    '''A helper function to read file.'''
    with open(os.path.join(TEST_DIR, filename), 'r', encoding='utf-8') as file:
        return file.read()


def read_ranged_file(count, name, ext):
    '''A helper function to read files.'''
    return [
        read_file('{}{}.{}'.format(name, index + 1, ext))
        for index in range(count)
    ]


def load_json(filename):
    '''A helper function to read JSON-format file.'''
    with open(os.path.join(TEST_DIR, filename), 'r', encoding='utf-8') as file:
        return json.load(file)


def load_ranged_json(count, name):
    '''A helper function to read JSON-format files.'''
    return [
        load_json('{}{}.json'.format(name, index + 1))
        for index in range(count)
    ]
