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
    @classmethod
    def setUpClass(cls):
        cls.board = ptt.Board('Soft_Job', 5)
        #cls.board.get_dom()
        cls.page_1 = read_file('testdata_input_1.html')
        cls.expect_1 = load_json('expect_1.json')
        cls.page_2 = read_file('testdata_input_2.html')
        cls.expect_2 = load_json('expect_2.json')


    def setUp(self):
        return self.board.set_url(self.board.board_name, True)


    # TODO use mock to avoid real internet access
    def test_get_dom(self):
        board = self.board
        board.get_dom()
        self.assertNotEqual(board.dom, None)

        board.set_url()
        with self.assertRaises(ValueError) as cm:
            board.get_dom()


    def test_page_to_soup(self):
        board = self.board
        board.page_to_soup(self.page_1)
        self.assertEqual(board.dom.find('title').text, self.expect_1['html_title'])


    def test_find_prev_page_url(self):
        self.find_prev_page_url(self.page_1, self.expect_1)
        self.find_prev_page_url(self.page_2, self.expect_2)


    def find_prev_page_url(self, page, expect):
        board = self.board

        board.page_to_soup(page)
        # this condition is decided outside being tested function
        if should_choose_atcual(expect):
            board.find_prev_page_url()
        else:
            board.url = None
        self.assertEqual(board.url, expect['prev_page_url'])



    def test_get_articles_meta(self):
        board = self.board

        board.page_to_soup(self.page_1)
        self.compare_all_meta(board.get_articles_meta(), self.expect_1['articles_meta'])

        board.page_to_soup(self.page_2)
        self.compare_all_meta(board.get_articles_meta(), self.expect_2['articles_meta'])


    def test_get_article_blocks(self):
        self.get_article_blocks(self.page_1, len(self.expect_1['articles_meta']))
        self.get_article_blocks(self.page_2, len(self.expect_2['articles_meta']))


    def get_article_blocks(self, page, expect):
        board = self.board

        board.page_to_soup(page)
        article_blocks = [
                article_block
                for article_block in board.get_article_blocks()
                if article_block.find('a')
        ]
        self.assertEqual(len(article_blocks), expect)


    def test_get_article_meta(self):
        self.get_article_meta(self.page_1, self.expect_1['articles_meta'][0])
        self.get_article_meta(self.page_2, self.expect_2['articles_meta'][0])


    def get_article_meta(self, page, expect):
        board = self.board

        board.page_to_soup(page)
        article_meta = next(
                board.get_article_meta(article_block)
                for article_block in board.get_article_blocks()
                if article_block.find('a')
        )
        self.compare_meta(article_meta, expect)


    def test_remove_expired(self):
        self.remove_expired(self.page_1, self.expect_1['remove_expired'])
        self.remove_expired(self.page_2, self.expect_2['remove_expired'])


    def remove_expired(self, page, expect):
        board = self.board

        board.page_to_soup(page)
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
