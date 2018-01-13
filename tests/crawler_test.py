'''
Unit tests for crawler module.
'''
import logging
import os
import unittest
from tests.helper import load_jsons
import tests.article_helper
import crawler
import ptt
import dom_operation as op

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
            board_name = article_meta['board_name']
            article_meta = article_meta['article_meta']

            cls.articles[index] = ptt.Article(board_name, **article_meta)
            cls.articles[index].dom = op.get_article_content(cls.pages[index])

            cls.contents[index] = cls.articles[index].format_article()

    def setUp(self):
        '''The test case level setup.'''
        crawler.setup()

    def tearDown(self):
        '''The test case level clean-up.'''
        crawler.shutdown()

    def test_setup(self):
        '''Unit test for crawler.setup.'''
        data_path = crawler.CONFIG.get('Crawler', 'data_path')
        self.assertTrue(os.path.isdir(data_path))

    @unittest.skip("just skipping")
    def test_crawler(self):
        '''Unit test for crawler.crawler.'''
        crawler.crawler()
        self.fail("Not implemented")

    def test_parse_board(self):
        '''Unit test for crawler.parse_board.'''
        articles_meta = crawler.parse_board(None)
        self.assertEqual(articles_meta, None)

    def test_retrieve_article(self):
        '''Unit test for crawler.retrieve_article.'''
        articles = crawler.retrieve_article()
        self.assertEqual(articles, None)

        for index, meta in enumerate(self.meta):
            self.retrieve_article(meta['article_meta'], self.contents[index])

    def retrieve_article(self, meta, expect):
        '''A helper function for test_retrieve_article.'''
        article_content = crawler.retrieve_article(**meta)
        self.assertEqual(article_content, expect)

    def test_save_article(self):
        '''Unit test for crawler.save_article.'''
        for index, content in enumerate(self.contents.values()):
            article_meta = self.meta[index]['article_meta']
            expect = self.expects[index]['filename']
            self.save_article(content, article_meta, expect)

    def save_article(self, content, meta, expect):
        '''A helper function for test_save_article.'''
        crawler.save_article(content, **meta)

        path = os.path.join(crawler.CONFIG.get('Crawler', 'data_path'), expect)
        self.assertEqual(os.path.isfile(path), True)


if __name__ == '__main__':
    unittest.main()
