import unittest
import ptt

class PttTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.page = ptt.Page()

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

if __name__ == '__main__':
    unittest.main()
