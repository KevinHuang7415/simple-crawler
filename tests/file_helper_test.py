'''
Unit tests for file_helper module.
'''
import os
import unittest
import file_helper


class FileHelperTestCase(unittest.TestCase):
    '''Test cases for file_helper.'''

    @classmethod
    def setUpClass(cls):
        '''The class level setup.'''
        cls.path = r'.\tests\data'
        cls.article = 'article'
        cls.title = 'title'

    def tearDown(self):
        '''The test case level clean-up.'''
        import shutil
        if os.path.exists(self.path):
            shutil.rmtree(self.path)

    def test_get_dir(self):
        '''Unit test for file_helper.get_dir.'''
        path = r'.\tests'
        self.assertEqual(file_helper.get_dir([None, path]), path)
        self.assertEqual(file_helper.get_dir([None]), file_helper.DEFAULT_DIR)

    def test_format_filename(self):
        '''Unit test for file_helper.test_format_filename.'''
        filename = file_helper.format_filename(r'a/b\c?d.e"f*g<h>i|j')
        self.assertEqual(filename, 'abcdefghij')

    def test_create_dir_if_not_exist(self):
        '''Unit test for file_helper.create_dir_if_not_exist.'''
        path = self.path
        file_helper.create_dir_if_not_exist(path)
        self.assertTrue(os.path.exists(path))

    def test_write_article(self):
        '''Unit test for file_helper.write_article.'''
        path = self.path
        file_helper.create_dir_if_not_exist(path)
        file_helper.write_article(self.article, self.title, path)

        filename = self.title + '.txt'
        file_path = os.path.join(path, filename)
        self.assertTrue(os.path.exists(file_path))


if __name__ == '__main__':
    unittest.main()
