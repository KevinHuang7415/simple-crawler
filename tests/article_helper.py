'''
Public helper functions for unit testing.
'''
from tests.helper import read_files, load_jsons

COUNT_TEST_DATA = 4


def get_pages():
    '''Get all test data for article pages.'''
    return read_files(COUNT_TEST_DATA, 'testdata_input_article_', 'html')


def get_meta():
    '''Get all test data for article meta.'''
    return load_jsons(COUNT_TEST_DATA, 'article_meta_')


def get_expects():
    '''Get all expect values for articles.'''
    return load_jsons(COUNT_TEST_DATA, 'expect_article_')


def setup():
    '''Setup all test data required by article.'''
    return get_pages(), get_meta(), get_expects()
