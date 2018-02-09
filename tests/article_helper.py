'''
Public helper functions for unit testing.
'''
from tests.helper import read_ranged_file, load_ranged_json

COUNT_TEST_DATA = 4


def get_page_list():
    '''Get all test data for article pages.'''
    return read_ranged_file(COUNT_TEST_DATA,
                            'testdata_input_article_',
                            'html')


def get_meta_list():
    '''Get all test data for article meta.'''
    return load_ranged_json(COUNT_TEST_DATA, 'article_meta_')


def get_expect_list():
    '''Get all expect values for articles.'''
    return load_ranged_json(COUNT_TEST_DATA, 'expect_article_')


def setup():
    '''Setup all test data required by article.'''
    return get_page_list(), get_meta_list(), get_expect_list()
