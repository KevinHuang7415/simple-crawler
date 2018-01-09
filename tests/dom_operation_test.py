'''
Unit tests for config module.
'''
import logging
import unittest
from tests.helper import read_file, load_json
import dom_operation

logging.disable(logging.CRITICAL)


def _should_choose_atcual(data):
    '''A helper function to combine key-value pair'''
    return len(data['articles_meta']) == len(data['remove_expired'])


class DomOperationTestCase(unittest.TestCase):
    '''Test cases for dom_operation.'''

    BOARD_NAME = 'Soft_Job'

    @classmethod
    def setUpClass(cls):
        '''The class level setup.'''
        cls.board_pages = {}
        cls.board_pages[0] = read_file('testdata_input_board_1.html')
        cls.board_pages[1] = read_file('testdata_input_board_2.html')

        cls.board_dom = {}
        for index, board_page in enumerate(cls.board_pages.values()):
            cls.board_dom[index] = dom_operation.get_board_content(board_page)

        cls.board_last_page = {}

        cls.board_expects = {}
        cls.board_expects[0] = load_json('expect_board_1.json')
        cls.board_expects[1] = load_json('expect_board_2.json')


        cls.article_pages = {}
        cls.article_pages[0] = read_file('testdata_input_article_1.html')
        cls.article_pages[1] = read_file('testdata_input_article_2.html')

        cls.article_dom = {}
        for index, article_page in enumerate(cls.article_pages.values()):
            cls.article_dom[index] = dom_operation.get_article_content(article_page)

        cls.article_meta = {}
        cls.article_meta[0] = load_json('article_meta_1.json')
        cls.article_meta[1] = load_json('article_meta_2.json')

        cls.article_expects = {}
        cls.article_expects[0] = load_json('expect_article_1.json')
        cls.article_expects[1] = load_json('expect_article_2.json')

    def setUp(self):
        '''The test case level setup.'''
        self.board_last_page[0] = True
        self.board_last_page[1] = False

        for index, article_page in enumerate(self.article_pages.values()):
            self.article_dom[index] = dom_operation.get_article_content(article_page)

    def test_get_board_content(self):
        '''Unit test for dom_operation.get_board_content.'''
        dom = dom_operation.get_board_content(self.board_pages[0])
        self.assertEqual(
            dom.find('title').text,
            self.board_expects[0]['html_title']
        )

    def test_get_article_content(self):
        '''Unit test for dom_operation.get_article_content.'''
        dom = dom_operation.get_article_content(self.article_pages[0])
        self.assertNotEqual(dom, None)

    def test_find_prev_page_url(self):
        '''Unit test for dom_operation.find_prev_page_url.'''
        for index, dom in enumerate(self.board_dom.values()):
            self.find_prev_page_url(dom, self.board_expects[index])

    def find_prev_page_url(self, dom, expect):
        '''A helper function for test_find_prev_page_url.'''
        # this condition is decided outside being tested function
        if _should_choose_atcual(expect):
            url = dom_operation.find_prev_page_url(dom)
        else:
            url = None

        self.assertEqual(url, expect['prev_page_url'])

    def test_get_article_blocks(self):
        '''Unit test for dom_operation.get_article_blocks.'''
        for index, dom in enumerate(self.board_dom.values()):
            self.get_article_blocks(
                dom,
                self.board_last_page[index],
                len(self.board_expects[index]['articles_meta'])
            )

    def get_article_blocks(self, dom, last_page, expect):
        '''A helper function for test_get_article_blocks.'''
        article_blocks = [
            article_block
            for article_block in dom_operation.get_article_blocks(dom, last_page)
            if article_block.find('a')
        ]
        self.assertEqual(len(article_blocks), expect)

    def test_get_article_meta(self):
        '''Unit test for dom_operation.get_article_meta.'''
        for index, dom in enumerate(self.board_dom.values()):
            self.get_article_meta(
                dom,
                self.board_last_page[index],
                self.board_expects[index]['articles_meta'][0]
            )

    def get_article_meta(self, dom, last_page, expect):
        '''A helper function for test_get_article_meta.'''
        article_meta = next(
            dom_operation.get_article_meta(article_block)
            for article_block in dom_operation.get_article_blocks(dom, last_page)
            if article_block.find('a')
        )

        self.compare_meta(article_meta, expect)

    def test_get_create_time(self):
        '''Unit test for dom_operation.get_create_time.'''
        for index, dom in enumerate(self.article_dom.values()):
            self.get_create_time(dom, self.article_expects[index]['create_time'])

    def get_create_time(self, dom, expect):
        '''A helper function for test_get_create_time.'''
        self.assertEqual(dom_operation.get_create_time(dom), expect)

    def compare_meta(self, act, expect):
        '''Compare meta data between actual and expected.'''
        self.assertEqual(act['title'], expect['title'])
        self.assertEqual(act['href'], expect['href'])
        self.assertEqual(act['date'], expect['date'])
        self.assertEqual(act['author'], expect['author'])


if __name__ == '__main__':
    unittest.main()
