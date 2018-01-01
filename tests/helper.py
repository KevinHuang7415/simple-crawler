'''
Public helper functions for unit testing.
'''
import json
import os


TEST_DIR = 'tests'


def read_file(filename):
    '''A helper function to read file.'''
    with open(os.path.join(TEST_DIR, filename), 'r', encoding='utf-8') as file:
        return file.read()


def load_json(filename):
    '''A helper function to read JSON-format file.'''
    with open(os.path.join(TEST_DIR, filename), 'r', encoding='utf-8') as file:
        return json.load(file)
