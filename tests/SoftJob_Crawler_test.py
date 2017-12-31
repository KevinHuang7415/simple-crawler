import json
import os
import unittest
from file_helper import DEFAULT_DIR
import SoftJob_Crawler
import ptt


TEST_DIR = 'tests'


def read_file(filename):
    with open(os.path.join(TEST_DIR, filename), 'r', encoding='utf-8') as file:
        return file.read()


def load_json(filename):
    with open(os.path.join(TEST_DIR, filename), 'r', encoding='utf-8') as file:
        return json.load(file)


class SoftJob_CrawlerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
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
            cls.articles[index] = ptt.Article(article_meta['board_name'], **article_meta['article_meta'])
            cls.articles[index].get_content(cls.pages[index])
            cls.contents[index] = cls.articles[index].format_article()


    def test_setup_path(self):
        SoftJob_Crawler.setup_path()
        self.assertEqual(os.path.isdir(DEFAULT_DIR), True)


    def test_crawler(self):
        #SoftJob_Crawler.crawler()
        #self.fail("Not implemented")
        pass


    def test_parse_board(self):
        articles_meta = SoftJob_Crawler.parse_board(None)
        self.assertEqual(articles_meta, None)


    def test_retrieve_article(self):
        articles = SoftJob_Crawler.retrieve_article()
        self.assertEqual(articles, None)

        for index, article in enumerate(self.articles.values()):
            self.retrieve_article(self.meta[index]['article_meta'], self.contents[index])


    def retrieve_article(self, meta, expect):
        article_content = SoftJob_Crawler.retrieve_article(**meta)
        self.assertEqual(article_content, expect)


    def test_save_article(self):
        for index, content in enumerate(self.contents.values()):
            self.save_article(content, self.meta[index]['article_meta'], self.expects[index]['filename'])


    def save_article(self, content, meta, expect):
        SoftJob_Crawler.save_article(content, **meta)
        self.assertEqual(os.path.isfile(os.path.join(DEFAULT_DIR, expect)), True)


if __name__ == '__main__':
    unittest.main()
