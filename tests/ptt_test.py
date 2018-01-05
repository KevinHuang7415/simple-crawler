'''
Unit tests for ptt module.
'''
import unittest
from tests.helper import read_file, load_json
import ptt


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
        cls.boards = {}
        cls.boards[0] = ptt.Board(cls.BOARD_NAME, 11)
        cls.boards[1] = ptt.Board(cls.BOARD_NAME, 11)  # 7 when 1/1

        cls.pages = {}
        cls.pages[0] = read_file('testdata_input_board_1.html')
        cls.pages[1] = read_file('testdata_input_board_2.html')

        cls.expects = {}
        cls.expects[0] = load_json('expect_board_1.json')
        cls.expects[1] = load_json('expect_board_2.json')

    def setUp(self):
        '''The test case level setup.'''
        for index, board in enumerate(self.boards.values()):
            board.set_url(self.BOARD_NAME)
            board._get_content(self.pages[index])

        self.boards[0].latest_page = True
        self.boards[1].latest_page = False

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
        for index, board in enumerate(self.boards.values()):
            self.find_prev_page_url(board, self.expects[index])

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
        for index, board in enumerate(self.boards.values()):
            self.get_articles_meta(board, self.expects[index]['articles_meta'])

    def get_articles_meta(self, board, expects):
        '''A helper function for test_get_articles_meta.'''
        articles_meta = board.get_articles_meta()

        for index, expect in enumerate(expects):
            self.compare_meta(articles_meta[index], expect)

    def test_remove_expired(self):
        '''Unit test for ptt.Board.remove_expired.'''
        for index, board in enumerate(self.boards.values()):
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


class ArticleTestCase(unittest.TestCase):
    '''Test cases for ptt.Article.'''

    @classmethod
    def setUpClass(cls):
        '''The class level setup.'''
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
            cls.articles[index] = ptt.Article(
                article_meta['board_name'],
                **article_meta['article_meta']
            )

    def setUp(self):
        '''The test case level setup.'''
        for index, article in enumerate(self.articles.values()):
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
        for index, article in enumerate(self.articles.values()):
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
