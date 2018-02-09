'''
Public helper functions for unit testing.
'''
from tests.helper import read_ranged_file, load_ranged_json

COUNT_TEST_DATA = 2


def get_page_list():
    '''Get all test data for board pages.'''
    return read_ranged_file(COUNT_TEST_DATA, 'testdata_input_board_', 'html')


def get_expect_list():
    '''Get all expect values for boards.'''
    return load_ranged_json(COUNT_TEST_DATA, 'expect_board_')


def setup():
    '''Setup all test data required by article.'''
    return get_page_list(), get_expect_list()
