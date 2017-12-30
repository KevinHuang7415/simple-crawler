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
        cls.board = {}
        cls.board[0] = ptt.Board(cls.BOARD_NAME, 6)
        cls.board[1] = ptt.Board(cls.BOARD_NAME, 6)
        #cls.board.get_dom()
        cls.page = {}
        cls.page[0] = read_file('testdata_input_1.html')
        cls.page[1] = read_file('testdata_input_2.html')

        cls.expect = {}
        cls.expect[0] = load_json('expect_1.json')
        cls.expect[1] = load_json('expect_2.json')


    def setUp(self):
        for index, board in enumerate(self.board.values()):
            board.set_url(self.BOARD_NAME, True)
            board.page_to_soup(self.page[index])

        self.board[0].latest_page = True
        self.board[1].latest_page = False


    # TODO use mock to avoid real internet access
    def test_get_dom(self):
        board = self.board[0]
        board.get_dom()
        self.assertNotEqual(board.dom, None)

        board.set_url()
        with self.assertRaises(ValueError) as cm:
            board.get_dom()


    def test_page_to_soup(self):
        board = self.board[0]
        board.page_to_soup(self.page[0])
        self.assertEqual(board.dom.find('title').text, self.expect[0]['html_title'])


    def test_find_prev_page_url(self):
        for index, board in enumerate(self.board.values()):
            self.find_prev_page_url(board, self.expect[index])


    def find_prev_page_url(self, board, expect):
        # this condition is decided outside being tested function
        if should_choose_atcual(expect):
            board.find_prev_page_url()
        else:
            board.url = None
        self.assertEqual(board.url, expect['prev_page_url'])


    def test_get_articles_meta(self):
        for index, board in enumerate(self.board.values()):
            self.get_articles_meta(board, self.expect[index]['articles_meta'])


    def get_articles_meta(self, board, expect):
        self.compare_all_meta(board.get_articles_meta(), expect)


    def test_get_article_blocks(self):
        for index, board in enumerate(self.board.values()):
            self.get_article_blocks(board, len(self.expect[index]['articles_meta']))


    def get_article_blocks(self, board, expect):
        article_blocks = [
                article_block
                for article_block in board.get_article_blocks()
                if article_block.find('a')
        ]
        self.assertEqual(len(article_blocks), expect)


    def test_get_article_meta(self):
        for index, board in enumerate(self.board.values()):
            self.get_article_meta(board, self.expect[index]['articles_meta'][0])


    def get_article_meta(self, board, expect):
        article_meta = next(
                board.get_article_meta(article_block)
                for article_block in board.get_article_blocks()
                if article_block.find('a')
        )
        self.compare_meta(article_meta, expect)


    def test_remove_expired(self):
        for index, board in enumerate(self.board.values()):
            self.remove_expired(board, self.expect[index]['remove_expired'])


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


if __name__ == '__main__':
    unittest.main()
