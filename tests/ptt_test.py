'''
Unit tests for ptt module.
'''
from datetime import date
import logging
import unittest
import tests.board_helper
import tests.article_helper
import ptt

logging.disable(logging.CRITICAL)


class AbstractPageTestCase(unittest.TestCase):
    '''Test cases for ptt.Page.'''

    @classmethod
    def setUpClass(cls):
        '''The class level setup.'''
        cls.page = ptt.AbstractPage()

    def test_set_url(self):
        '''Unit test for ptt.Page.set_url.'''
        page = self.page

        page.set_url()
        self.assertEqual(page.url, None)

        uri = 'board/index.html'
        page.set_url(uri)
        self.assertEqual(page.url, uri)

    # TODO use mock to avoid real internet access
    def test_retrieve_dom(self):
        '''Unit test for ptt.Page.retrieve_dom.'''
        self.page.set_url()
        with self.assertRaises(ValueError):
            self.page.retrieve_dom()


def _should_choose_atcual(data):
    '''A helper function to combine key-value pair'''
    return len(data['articles_meta']) == len(data['remove_expired'])


class BoardTestCase(unittest.TestCase):
    '''Test cases for ptt.Board.'''

    BOARD_NAME = 'Soft_Job'

    @classmethod
    def setUpClass(cls):
        '''The class level setup.'''
        date_diff = (date.today() - date(year=2017, month=12, day=25)).days

        cls.pages, cls.expects = tests.board_helper.setup()

        cls.boards = [
            ptt.Board(cls.BOARD_NAME, date_diff)
            for index in range(len(cls.pages))
        ]

    def setUp(self):
        '''The test case level setup.'''
        for index, board in enumerate(self.boards):
            board.set_url(self.BOARD_NAME)
            board._get_content(self.pages[index])
            board.latest_page = self.expects[index]['latest_page']

    def test_set_url(self):
        '''Unit test for ptt.Board.set_url.'''
        board_name = self.BOARD_NAME
        board = ptt.Board(board_name, 11)

        board.set_url()
        self.assertEqual(board.url, None)

        board.set_url(board_name)
        self.assertEqual(board.url, '/bbs/{0}/index.html'.format(board_name))

    # TODO use mock to avoid real internet access
    def test_retrieve_dom(self):
        '''Unit test for ptt.Board.retrieve_dom.'''
        board = self.boards[0]

        board.retrieve_dom()
        self.assertNotEqual(board.dom, None)

        board.set_url()
        with self.assertRaises(ValueError):
            board.retrieve_dom()

    def test_find_prev_page_url(self):
        '''Unit test for ptt.Board.find_prev_page_url.'''
        for index, board in enumerate(self.boards):
            self.find_prev_page_url(board, self.expects[index])

        board = self.build_test_board()
        with self.assertRaises(ValueError):
            board.find_prev_page_url()

    def find_prev_page_url(self, board, expect):
        '''A helper function for test_find_prev_page_url.'''
        # this condition is decided outside being tested function
        if _should_choose_atcual(expect):
            board.find_prev_page_url()
        else:
            board.url = None

        self.assertEqual(board.url, expect['prev_page_url'])

    def test_get_articles_meta(self):
        '''Unit test for ptt.Board.get_articles_meta.'''
        for index, board in enumerate(self.boards):
            self.get_articles_meta(board, self.expects[index]['articles_meta'])

        board = self.build_test_board()
        with self.assertRaises(ValueError):
            board.get_articles_meta()

    def get_articles_meta(self, board, expects):
        '''A helper function for test_get_articles_meta.'''
        articles_meta = board.get_articles_meta()

        for index, expect in enumerate(expects):
            self.compare_meta(articles_meta[index], expect)

    def test_remove_expired(self):
        '''Unit test for ptt.Board.remove_expired.'''
        for index, board in enumerate(self.boards):
            self.remove_expired(board, self.expects[index]['remove_expired'])

    def remove_expired(self, board, expects):
        '''A helper function for test_remove_expired.'''
        after_remove = board.remove_expired(board.get_articles_meta())

        for index, expect in enumerate(expects):
            self.compare_meta(after_remove[index], expect)

    def compare_meta(self, act, expect):
        '''Compare meta data between actual and expected.'''
        self.assertEqual(act['title'], expect['title'])
        self.assertEqual(act['href'], expect['href'])
        self.assertEqual(act['date'], expect['date'])
        self.assertEqual(act['author'], expect['author'])

    def build_test_board(self):
        '''Build a temporary board object.'''
        board = ptt.Board(self.BOARD_NAME, 0)
        board._get_content(None)
        return board


class ArticleTestCase(unittest.TestCase):
    '''Test cases for ptt.Article.'''

    @classmethod
    def setUpClass(cls):
        '''The class level setup.'''
        cls.pages, cls.meta, cls.expects = tests.article_helper.setup()

        cls.articles = [
            ptt.Article(
                article_meta['board_name'],
                **article_meta['article_meta']
            )
            for article_meta in cls.meta
        ]

    def setUp(self):
        '''The test case level setup.'''
        for index, article in enumerate(self.articles):
            article.set_url(self.meta[index]['article_meta']['href'])
            article._get_content(self.pages[index])

    # TODO use mock to avoid real internet access
    def test_retrieve_dom(self):
        '''Unit test for ptt.Article.retrieve_dom.'''
        article = self.articles[0]

        article.retrieve_dom()
        self.assertNotEqual(article.dom, None)

        article.set_url()
        with self.assertRaises(ValueError):
            article.retrieve_dom()

    def test_format_article(self):
        '''Unit test for ptt.Article.format_article.'''
        for index, article in enumerate(self.articles):
            self.format_article(article, self.expects[index]['article'])

        article = ptt.Article(
            self.meta[0]['board_name'],
            **self.meta[0]['article_meta']
        )
        article._get_content(None)
        with self.assertRaises(ValueError):
            article.format_article()

    def format_article(self, article, expect):
        '''A helper function for test_format_article.'''
        content = article.format_article()
        self.assertEqual(len(content), len(expect))
        # self.assertEqual(article.format_article(), expect)


if __name__ == '__main__':
    unittest.main()
