'''
Unit tests for config module.
'''
import logging
import unittest
import tests.board_helper
import tests.article_helper
import domparser as dp

logging.disable(logging.CRITICAL)


def _should_choose_atcual(data):
    '''A helper function to combine key-value pair'''
    return len(data['articles_meta']) == len(data['remove_expired'])


class DomOperationTestCase(unittest.TestCase):
    '''Test cases for domparser.'''

    BOARD_NAME = 'Soft_Job'

    @classmethod
    def setUpClass(cls):
        '''The class level setup.'''
        # board part
        cls.board_pages, cls.board_expects = tests.board_helper.setup()

        cls.board_parsers = [
            dp.DOMParser.builder(dp.PageType.board, board_page)
            for board_page in cls.board_pages
        ]

        cls.board_last_page = [
            board_expect['latest_page']
            for board_expect in cls.board_expects
        ]

        # article part
        cls.article_pages, cls.article_meta, cls.article_expects =\
            tests.article_helper.setup()

        cls.article_parsers = [
            dp.DOMParser.builder(dp.PageType.article, article_page)
            for article_page in cls.article_pages
        ]

    def setUp(self):
        '''The test case level setup.'''
        for index, article_page in enumerate(self.article_pages):
            self.article_parsers[index].dom =\
                dp.DOMParser.get_article_content(article_page)

    def test_get_board_content(self):
        '''Unit test for domparser.get_board_content.'''
        dom = dp.DOMParser.get_board_content(self.board_pages[0])
        self.assertEqual(
            dom.find('title').text,
            self.board_expects[0]['html_title']
        )

    def test_get_article_content(self):
        '''Unit test for domparser.get_article_content.'''
        dom = dp.DOMParser.get_article_content(self.article_pages[0])
        self.assertNotEqual(dom, None)

    def test_find_prev_page_url(self):
        '''Unit test for domparser.find_prev_page_url.'''
        for index, parser in enumerate(self.board_parsers):
            self.find_prev_page_url(parser, self.board_expects[index])

    def find_prev_page_url(self, parser, expect):
        '''A helper function for test_find_prev_page_url.'''
        # this condition is decided outside being tested function
        if _should_choose_atcual(expect):
            url = parser.find_prev_page_url()
        else:
            url = None

        self.assertEqual(url, expect['prev_page_url'])

    def test_get_articles_meta(self):
        '''Unit test for domparser.get_articles_meta.'''
        for index, parser in enumerate(self.board_parsers):
            self.get_articles_meta(
                parser,
                self.board_last_page[index],
                self.board_expects[index]['articles_meta']
            )

    def get_articles_meta(self, parser, last_page, expects):
        '''A helper function for test_get_article_blocks.'''
        articles_meta = parser.get_articles_meta(last_page)
        self.assertEqual(len(articles_meta), len(expects))

        for index, expect in enumerate(expects):
            self.compare_meta(articles_meta[index], expect)

    def test_parse_article(self):
        '''Unit test for domparser.parse_article.'''
        for index, parser in enumerate(self.article_parsers):
            self.parse_article(parser, self.article_expects[index]['article'])

    def parse_article(self, parser, expect):
        '''A helper function for test_get_create_time.'''
        content = parser.parse_article()['content']
        self.assertEqual(len(content), len(expect))

    def compare_meta(self, act, expect):
        '''Compare meta data between actual and expected.'''
        self.assertEqual(act['title'], expect['title'])
        self.assertEqual(act['href'], expect['href'])
        self.assertEqual(act['date'], expect['date'])
        self.assertEqual(act['author'], expect['author'])


if __name__ == '__main__':
    unittest.main()
