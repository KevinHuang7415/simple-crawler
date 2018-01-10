'''
Unit tests for config module.
'''
import logging
import unittest
import tests.board_helper
import tests.article_helper
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
        # board part
        cls.board_pages, cls.board_expects = tests.board_helper.setup()

        cls.board_dom = [
            dom_operation.get_board_content(board_page)
            for board_page in cls.board_pages
        ]

        cls.board_last_page = [
            board_expect['latest_page']
            for board_expect in cls.board_expects
        ]

        # article part
        cls.article_pages, cls.article_meta, cls.article_expects = tests.article_helper.setup()

        cls.article_dom = [
            dom_operation.get_article_content(article_page)
            for article_page in cls.article_pages
        ]

    def setUp(self):
        '''The test case level setup.'''
        for index, article_page in enumerate(self.article_pages):
            self.article_dom[index] =\
                dom_operation.get_article_content(article_page)

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
        for index, dom in enumerate(self.board_dom):
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
        for index, dom in enumerate(self.board_dom):
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
        for index, dom in enumerate(self.board_dom):
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

    def test_parse_article(self):
        '''Unit test for dom_operation.parse_article.'''
        for index, dom in enumerate(self.article_dom):
            self.parse_article(
                dom,
                self.article_expects[index]['article']
            )

    def parse_article(self, dom, expect):
        '''A helper function for test_get_create_time.'''
        content = dom_operation.parse_article(dom)['content']
        self.assertEqual(len(content), len(expect))

    def compare_meta(self, act, expect):
        '''Compare meta data between actual and expected.'''
        self.assertEqual(act['title'], expect['title'])
        self.assertEqual(act['href'], expect['href'])
        self.assertEqual(act['date'], expect['date'])
        self.assertEqual(act['author'], expect['author'])


if __name__ == '__main__':
    unittest.main()
