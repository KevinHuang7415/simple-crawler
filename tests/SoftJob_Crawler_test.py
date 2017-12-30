import unittest
import SoftJob_Crawler

class SoftJob_CrawlerTest(unittest.TestCase):
    def test_crawler(self):
        #SoftJob_Crawler.crawler()
        self.fail("Not implemented")


    def test_parse_board(self):
        articles_meta = SoftJob_Crawler.parse_board(None)
        self.assertEqual(articles_meta, None)


    def test_get_web_page(self):
        url = ''
        self.assertGreater(len(SoftJob_Crawler.get_web_page(url)), 0)
        url = '/bbs/wtgh/index.html'
        self.assertEqual(SoftJob_Crawler.get_web_page(url), None)


    def test_articles_meta(self):
        #SoftJob_Crawler.get_articles_meta()
        self.fail("Not implemented")


    def test_get_article_content(self):
        #SoftJob_Crawler.get_article_content()
        self.fail("Not implemented")


    def test_save_article(self):
        #SoftJob_Crawler.save_article()
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
