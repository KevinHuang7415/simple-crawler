'''
Unit tests for crawler module.
'''
import os
import unittest
from tests.helper import read_file, load_json
import crawler
import ptt


class CrawlerTestCase(unittest.TestCase):
    '''Test cases for crawler.'''

    @classmethod
    def setUpClass(cls):
        '''The class level setup.'''
        cls.path = 'test_path'

        cls.pages = {}
        cls.pages[0] = read_file('testdata_input_article_1.html')
        cls.pages[1] = read_file('testdata_input_article_2.html')

        cls.meta = {}
        cls.meta[0] = load_json('article_meta_1.json')
        cls.meta[1] = load_json('article_meta_2.json')

        cls.expects = {}
        cls.expects[0] = load_json('expect_crawler_1.json')
        cls.expects[1] = load_json('expect_crawler_2.json')

        cls.contents = {}
        cls.articles = {}
        for index, article_meta in enumerate(cls.meta.values()):
            board_name = article_meta['board_name']
            article_meta = article_meta['article_meta']

            cls.articles[index] = ptt.Article(board_name, **article_meta)
            cls.articles[index]._get_content(cls.pages[index])

            cls.contents[index] = cls.articles[index].format_article()

        crawler.setup()

    def test_setup(self):
        '''Unit test for crawler.setup.'''
        crawler.setup()
        data_path = crawler.CONFIG.get('Crawler', 'data_path')
        self.assertTrue(os.path.isdir(data_path))

    @unittest.skip("just skipping")
    def test_crawler(self):
        '''Unit test for crawler.crawler.'''
        #crawler.crawler()
        #self.fail("Not implemented")
        pass

    def test_parse_board(self):
        '''Unit test for crawler.parse_board.'''
        articles_meta = crawler.parse_board(None)
        self.assertEqual(articles_meta, None)

    def test_retrieve_article(self):
        '''Unit test for crawler.retrieve_article.'''
        articles = crawler.retrieve_article()
        self.assertEqual(articles, None)

        for index, meta in enumerate(self.meta.values()):
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
