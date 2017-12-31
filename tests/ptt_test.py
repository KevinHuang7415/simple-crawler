import json
import os
import unittest
import ptt

TEST_DIR = 'tests'

class PageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = ptt.Page()


    def test_set_url(self):
        page = self.page

        page.set_url()
        self.assertEqual(page.url, None)

        page.set_url(use_join=True)
        self.assertEqual(page.url, '/bbs/index.html')

        uri = 'board'
        page.set_url(uri)
        self.assertEqual(page.url, uri)

        page.set_url(uri, True)
        self.assertEqual(page.url, '/bbs/{0}/index.html'.format(uri))


    def test_get_web_page(self):
        self.assertNotEqual(self.page.get_web_page(0), None)

        self.page.set_url()
        with self.assertRaises(ValueError) as cm:
            self.page.get_web_page()


def read_file(filename):
    with open(os.path.join(TEST_DIR, filename), 'r', encoding='utf-8') as file:
        return file.read()


def load_json(filename):
    with open(os.path.join(TEST_DIR, filename), 'r', encoding='utf-8') as file:
        return json.load(file)


def should_choose_atcual(data):
    return len(data['articles_meta']) == len(data['remove_expired'])


class BoardTest(unittest.TestCase):

    BOARD_NAME = 'Soft_Job'

    @classmethod
    def setUpClass(cls):
        cls.boards = {}
        cls.boards[0] = ptt.Board(cls.BOARD_NAME, 7)
        cls.boards[1] = ptt.Board(cls.BOARD_NAME, 7) # 7 when 1/1

        cls.pages = {}
        cls.pages[0] = read_file('testdata_input_board_1.html')
        cls.pages[1] = read_file('testdata_input_board_2.html')

        cls.expects = {}
        cls.expects[0] = load_json('expect_board_1.json')
        cls.expects[1] = load_json('expect_board_2.json')


    def setUp(self):
        for index, board in enumerate(self.boards.values()):
            board.set_url(self.BOARD_NAME, True)
            board.page_to_soup(self.pages[index])

        self.boards[0].latest_page = True
        self.boards[1].latest_page = False


    # TODO use mock to avoid real internet access
    def test_get_dom(self):
        board = self.boards[0]
        board.get_dom()
        self.assertNotEqual(board.dom, None)

        board.set_url()
        with self.assertRaises(ValueError) as cm:
            board.get_dom()


    def test_page_to_soup(self):
        board = self.boards[0]
        board.page_to_soup(self.pages[0])
        self.assertEqual(board.dom.find('title').text, self.expects[0]['html_title'])

        board.page_to_soup(None)
        self.assertEqual(board.dom, None)


    def test_find_prev_page_url(self):
        for index, board in enumerate(self.boards.values()):
            self.find_prev_page_url(board, self.expects[index])


    def find_prev_page_url(self, board, expect):
        # this condition is decided outside being tested function
        if should_choose_atcual(expect):
            board.find_prev_page_url()
        else:
            board.url = None
        self.assertEqual(board.url, expect['prev_page_url'])


    def test_get_articles_meta(self):
        for index, board in enumerate(self.boards.values()):
            self.get_articles_meta(board, self.expects[index]['articles_meta'])


    def get_articles_meta(self, board, expect):
        self.compare_all_meta(board.get_articles_meta(), expect)


    def test_get_article_blocks(self):
        for index, board in enumerate(self.boards.values()):
            self.get_article_blocks(board, len(self.expects[index]['articles_meta']))


    def get_article_blocks(self, board, expect):
        article_blocks = [
                article_block
                for article_block in board.get_article_blocks()
                if article_block.find('a')
        ]
        self.assertEqual(len(article_blocks), expect)


    def test_get_article_meta(self):
        for index, board in enumerate(self.boards.values()):
            self.get_article_meta(board, self.expects[index]['articles_meta'][0])


    def get_article_meta(self, board, expect):
        article_meta = next(
                board.get_article_meta(article_block)
                for article_block in board.get_article_blocks()
                if article_block.find('a')
        )
        self.compare_meta(article_meta, expect)


    def test_remove_expired(self):
        for index, board in enumerate(self.boards.values()):
            self.remove_expired(board, self.expects[index]['remove_expired'])


    def remove_expired(self, board, expect):
        after_remove = board.remove_expired(board.get_articles_meta())
        self.compare_all_meta(after_remove, expect)


    def compare_meta(self, act, expect):
        self.assertEqual(act['title'], expect['title'])
        self.assertEqual(act['href'], expect['href'])
        self.assertEqual(act['date'], expect['date'])
        self.assertEqual(act['author'], expect['author'])


    def compare_all_meta(self, acts, expects):
        for index, expect in enumerate(expects):
            self.compare_meta(acts[index], expect)


class ArticleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = {}
        cls.pages[0] = read_file('testdata_input_article_1.html')
        cls.pages[1] = read_file('testdata_input_article_2.html')

        cls.meta = {}
        cls.meta[0] = load_json('article_meta_1.json')
        cls.meta[1] = load_json('article_meta_2.json')

        cls.expects = {}
        cls.expects[0] = load_json('expect_article_1.json')
        cls.expects[1] = load_json('expect_article_2.json')

        cls.articles = {}
        for index, article_meta in enumerate(cls.meta.values()):
            cls.articles[index] = ptt.Article(article_meta['board_name'], **article_meta['article_meta'])


    def setUp(self):
        for index, article in enumerate(self.articles.values()):
            article.set_url(self.meta[index]['article_meta']['href'])
            article.get_content(self.pages[index])


    # TODO use mock to avoid real internet access
    def test_get_dom(self):
        article = self.articles[0]
        article.get_dom()
        self.assertNotEqual(article.dom, None)

        article.set_url()
        with self.assertRaises(ValueError) as cm:
            article.get_dom()


    def test_get_content(self):
        article = self.articles[0]
        article.get_content(self.pages[0])
        self.assertNotEqual(article.dom, None)

        article.get_content(None)
        self.assertEqual(article.dom, None)


    def test_format_article(self):
        for index, article in enumerate(self.articles.values()):
            self.format_article(article, self.expects[index]['article'])


    def format_article(self, article, expect):
        content = article.format_article()
        self.assertEqual(len(content), len(expect))
        #self.assertEqual(article.format_article(), expect)

    def test_get_create_time(self):
        for index, article in enumerate(self.articles.values()):
            self.get_create_time(article, self.expects[index]['create_time'])


    def get_create_time(self, article, expect):
        self.assertEqual(article.get_create_time(), expect)


if __name__ == '__main__':
    unittest.main()
