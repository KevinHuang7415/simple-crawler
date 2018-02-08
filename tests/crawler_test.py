'''
Unit tests for crawler module.
'''
import logging
import unittest
from tests.helper import load_jsons
import tests.article_helper
import crawler
import domparser as dp
import ptt

logging.disable(logging.CRITICAL)


class CrawlerTestCase(unittest.TestCase):
    '''Test cases for crawler.'''

    @classmethod
    def setUpClass(cls):
        '''The class level setup.'''
        cls.path = 'test_path'

        cls.pages, cls.meta, _ = tests.article_helper.setup()
        cls.expects = load_jsons(len(cls.pages), 'expect_crawler_')

        cls.contents = {}
        cls.articles = {}
        for index, article_meta in enumerate(cls.meta):
            article_meta = article_meta['article_meta']

            cls.articles[index] = ptt.Article(**article_meta)
            cls.articles[index].parser =\
                dp.build_parser(dp.PageType.article, cls.pages[index])

            cls.contents[index] = cls.articles[index].parse_content()

    def setUp(self):
        '''The test case level setup.'''
        crawler.setup()

    def tearDown(self):
        '''The test case level clean-up.'''
        crawler.shutdown()

    def test_setup(self):
        '''Unit test for crawler.setup.'''
        self.assertIsNotNone(crawler.CONFIG.path)

    @unittest.skip('Nothing can really be tested.')
    def test_shutdown(self):
        '''Unit test for crawler.shutdown.'''
        crawler.shutdown()
        self.fail("Not implemented")

    @unittest.skip('Not a unit for unit test. Integration testing required.')
    def test_crawler(self):
        '''Unit test for crawler.crawler.'''
        crawler.crawler()
        self.fail("Not implemented")

    @unittest.skip('Enough to test ptt.Board only.')
    def test_parse_board(self):
        '''Unit test for crawler.parse_board.'''
        articles_meta = crawler.parse_board(None)
        self.assertIsNone(articles_meta)

    @unittest.skip('Enough to test ptt.Article only.')
    def test_retrieve_articles(self):
        '''Unit test for crawler.retrieve_articles.'''
        raise NotImplementedError

    @unittest.skip('Tests for database required.')
    def test_save_article(self):
        '''Unit test for crawler.save_article.'''
        raise NotImplementedError

    @unittest.skip('Tests for database required.')
    def test_update_article(self):
        '''Unit test for crawler.update_article.'''
        raise NotImplementedError


if __name__ == '__main__':
    unittest.main()
