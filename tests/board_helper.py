'''
Public helper functions for unit testing.
'''
from tests.helper import read_files, load_jsons

COUNT_TEST_DATA = 2


def get_pages():
    '''Get all test data for board pages.'''
    return read_files(COUNT_TEST_DATA, 'testdata_input_board_', 'html')


def get_expects():
    '''Get all expect values for boards.'''
    return load_jsons(COUNT_TEST_DATA, 'expect_board_')


def setup():
    '''Setup all test data required by article.'''
    return get_pages(), get_expects()
