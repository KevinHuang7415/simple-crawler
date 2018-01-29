'''
Unit tests for config module.
'''
import logging
import unittest
import tests.board_helper
import tests.article_helper
import domparser as dp

logging.disable(logging.CRITICAL)


class BoardParserTestCase(unittest.TestCase):
    '''Test cases for domparser.BoardParser.'''

    @classmethod
    def setUpClass(cls):
        '''The class level setup.'''
        cls.pages, cls.expects = tests.board_helper.setup()

        cls.parsers = [
            dp.build_parser(dp.PageType.board, board_page)
            for board_page in cls.pages
        ]

        cls.last_page = [
            board_expect['latest_page']
            for board_expect in cls.expects
        ]

    def test_find_prev_page_url(self):
        '''Unit test for domparser.find_prev_page_url.'''
        for index, parser in enumerate(self.parsers):
            self.find_prev_page_url(parser, self.expects[index])

    def find_prev_page_url(self, parser, expect):
        '''A helper function for test_find_prev_page_url.'''
        if len(expect['articles_meta']) == len(expect['remove_expired']):
            url = parser.find_prev_page_url()
        else:
            url = None

        self.assertEqual(url, expect['prev_page_url'])

    def test_get_articles_meta(self):
        '''Unit test for domparser.get_articles_meta.'''
        for index, parser in enumerate(self.parsers):
            self.get_articles_meta(
                parser,
                self.last_page[index],
                self.expects[index]['articles_meta']
            )

    def get_articles_meta(self, parser, last_page, expects):
        '''A helper function for test_get_articles_meta.'''
        articles_meta = parser.get_articles_meta(last_page)
        self.assertEqual(len(articles_meta), len(expects))

        for index, expect in enumerate(expects):
            self.compare_meta(articles_meta[index], expect)

    def compare_meta(self, act, expect):
        '''Compare meta data between actual and expected.'''
        self.assertEqual(act['title'], expect['title'])
        self.assertEqual(act['href'], expect['href'])
        self.assertEqual(act['date'], expect['date'])
        self.assertEqual(act['author'], expect['author'])


class ArticleParserTestCase(unittest.TestCase):
    '''Test cases for domparser.ArticleParser.'''

    @classmethod
    def setUpClass(cls):
        '''The class level setup.'''
        cls.pages, cls.meta, cls.expects = tests.article_helper.setup()

    def setUp(self):
        '''The test case level setup.'''
        self.parsers = [
            dp.build_parser(dp.PageType.article, page)
            for page in self.pages
        ]

    def test_parse_article(self):
        '''Unit test for domparser.parse_article.'''
        for index, parser in enumerate(self.parsers):
            self.parse_article(parser, self.expects[index]['article'])

    def parse_article(self, parser, expect):
        '''A helper function for test_parse_article.'''
        content = parser.parse_article()[0]
        self.assertEqual(len(content), len(expect))


if __name__ == '__main__':
    unittest.main()
