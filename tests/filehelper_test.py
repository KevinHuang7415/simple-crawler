'''
Unit tests for filehelper module.
'''
import logging
import os
import unittest
import filehelper as fh

logging.disable(logging.CRITICAL)


class FileHelperTestCase(unittest.TestCase):
    '''Test cases for filehelper.'''

    @classmethod
    def setUpClass(cls):
        '''The class level setup.'''
        cls.path = r'.\tests\for_test'
        cls.article = 'article'
        cls.title = 'title'

    def tearDown(self):
        '''The test case level clean-up.'''
        import shutil
        if os.path.exists(self.path):
            shutil.rmtree(self.path)

    def test_format_filename(self):
        '''Unit test for filehelper.test_format_filename.'''
        filename = fh.format_filename(r'a/b\c?d.e"f*g<h>i|j')
        self.assertEqual(filename, 'abcdefghij')

    def test_create_dir_if_not_exist(self):
        '''Unit test for filehelper.create_dir_if_not_exist.'''
        path = self.path
        fh.create_dir_if_not_exist(path)
        self.assertTrue(os.path.exists(path))

    def test_write_article(self):
        '''Unit test for filehelper.write_article.'''
        path = self.path
        fh.create_dir_if_not_exist(path)
        fh.write_article(self.article, self.title, path)

        filename = self.title + '.txt'
        file_path = os.path.join(path, filename)
        self.assertTrue(os.path.exists(file_path))


if __name__ == '__main__':
    unittest.main()
