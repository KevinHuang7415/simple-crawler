'''
Unit tests for ptt module.
'''
from datetime import date
import logging
import unittest
import tests.board_helper
import tests.article_helper
import ptt
import domparser as dp
import datetimehelper as dh

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
        self.assertIsNone(page.url)

        uri = 'board/index.html'
        page.set_url(uri)
        self.assertEqual(page.url, uri)

    def test_retrieve_dom(self):
        '''Unit test for ptt.Page.retrieve_dom.'''
        self.page.set_url()
        with self.assertRaises(ValueError):
            self.page.retrieve_dom()


def retrieve_dom(self, pagetype, page):
    '''A monkey patch for AbstractPage.retrieve_dom.'''
    try:
        self.parser = dp.build_parser(pagetype, page)
    except (KeyError, TypeError):
        raise ValueError


class BoardTestCase(unittest.TestCase):
    '''Test cases for ptt.Board.'''

    BOARD_NAME = 'Soft_Job'

    @classmethod
    def setUpClass(cls):
        '''The class level setup.'''
        # Date that test data created at 2017/12/25
        date_diff = (date.today() - date(year=2017, month=12, day=25)).days

        cls.page_list, cls.expect_list = tests.board_helper.setup()

        cls.board_list = [
            ptt.Board(cls.BOARD_NAME, date_diff)
            for _ in range(len(cls.page_list))
        ]

        cls.retrieve_dom = ptt.Board.retrieve_dom
        ptt.Board.retrieve_dom = retrieve_dom

    @classmethod
    def tearDownClass(cls):
        '''The class level cleanup.'''
        ptt.Board.retrieve_dom = cls.retrieve_dom
        ptt.close_session()

    def setUp(self):
        '''The test case level setup.'''
        for index, board in enumerate(self.board_list):
            board.set_url(self.BOARD_NAME)
            board.parser = dp.build_parser(
                dp.PageType.board,
                self.page_list[index]
            )
            board.latest_page = self.expect_list[index]['latest_page']

    def test_set_url(self):
        '''Unit test for ptt.Board.set_url.'''
        board_name = self.BOARD_NAME
        board = ptt.Board(board_name, 11)

        board.set_url()
        self.assertIsNone(board.url)

        board.set_url(board_name)
        self.assertEqual(board.url, '/bbs/{0}/index.html'.format(board_name))

    def test_retrieve_dom(self):
        '''Unit test for ptt.Board.retrieve_dom.'''
        for index, board in enumerate(self.board_list):
            board.retrieve_dom(
                dp.PageType.board,
                self.page_list[index]
            )
            self.assertNotEqual(board.parser, None)

        board = self.board_list[0]
        board.set_url()
        with self.assertRaises(ValueError):
            board.retrieve_dom(None, None)

    def test_find_prev_page_url(self):
        '''Unit test for ptt.Board.find_prev_page_url.'''
        for index, board in enumerate(self.board_list):
            self.find_prev_page_url(board, self.expect_list[index])

        board = self.build_test_board()
        with self.assertRaises(ValueError):
            board.find_prev_page_url()

    def find_prev_page_url(self, board, expect):
        '''A helper function for test_find_prev_page_url.'''
        if len(expect['articles_meta']) == len(expect['remove_expired']):
            board.find_prev_page_url()
        else:
            board.url = None

        self.assertEqual(board.url, expect['prev_page_url'])

    def test_all_articles_meta(self):
        '''Unit test for ptt.Board.all_articles_meta.'''
        for index, board in enumerate(self.board_list):
            self.all_articles_meta(
                board,
                self.expect_list[index]['remove_expired']
            )

        board = self.build_test_board()
        with self.assertRaises(ValueError):
            board.all_articles_meta()

    def all_articles_meta(self, board, expect_list):
        '''A helper function for test_all_articles_meta.'''
        article_meta_list = board.all_articles_meta()

        for index, expect in enumerate(expect_list):
            self.compare_meta(article_meta_list[index], expect)

    def compare_meta(self, act, expect):
        '''Compare meta data between actual and expected.'''
        self.assertEqual(act['title'], expect['title'])
        self.assertEqual(act['href'], expect['href'])
        self.assertEqual(act['date'], expect['date'])
        self.assertEqual(act['author'], expect['author'])

    def build_test_board(self):
        '''Build a temporary board object.'''
        board = ptt.Board(self.BOARD_NAME, 0)
        return board


class ArticleTestCase(unittest.TestCase):
    '''Test cases for ptt.Article.'''

    @classmethod
    def setUpClass(cls):
        '''The class level setup.'''
        cls.page_list, cls.meta_list, cls.expect_list =\
            tests.article_helper.setup()

        cls.article_list = [
            ptt.Article(**article_meta['article_meta'])
            for article_meta in cls.meta_list
        ]

        cls.retrieve_dom = ptt.Article.retrieve_dom
        ptt.Article.retrieve_dom = retrieve_dom

    @classmethod
    def tearDownClass(cls):
        '''The class level cleanup.'''
        ptt.Article.retrieve_dom = cls.retrieve_dom

    def setUp(self):
        '''The test case level setup.'''
        for index, article in enumerate(self.article_list):
            article.set_url(self.meta_list[index]['article_meta']['href'])
            article.parser = dp.build_parser(
                dp.PageType.article,
                self.page_list[index]
            )

    def test_retrieve_dom(self):
        '''Unit test for ptt.Article.retrieve_dom.'''
        for index, article in enumerate(self.article_list):
            article.retrieve_dom(dp.PageType.article, self.page_list[index])
            self.assertNotEqual(article.parser, None)

        article = self.article_list[0]
        article.set_url()
        with self.assertRaises(ValueError):
            article.retrieve_dom(None, None)

    def test_parse_content(self):
        '''Unit test for ptt.Article.parse_content.'''
        for index, article in enumerate(self.article_list):
            self.parse_content(article, self.expect_list[index])

        meta = self.meta_list[0]
        article = ptt.Article(**meta['article_meta'])
        article.parser = None
        with self.assertRaises(ValueError):
            article.parse_content()

    def parse_content(self, article, expect):
        '''A helper function for test_format_article.'''
        content, create_time, last_edit_time = article.parse_content()
        self.assertEqual(len(content), len(expect['article']))
        self.assertEqual(create_time, dh.to_datetime(expect['create_time']))
        self.assertEqual(
            last_edit_time,
            dh.to_datetime(expect['last_modify_time'])
        )


if __name__ == '__main__':
    unittest.main()
