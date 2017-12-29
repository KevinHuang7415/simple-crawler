import os
import unittest
import file_helper

class FileHelperTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.path = r'.\tests\data'
        self.article = 'article'
        self.title = 'title'

    def tearDown(self):
        import shutil
        if os.path.exists(self.path):
            shutil.rmtree(self.path)

    def test_get_dir(self):
        path = r'.\tests'
        self.assertEqual(file_helper.get_dir([None, path]), path)
        self.assertEqual(file_helper.get_dir([None]), file_helper.DEFAULT_DIR)

    def test_format_filename(self):
        self.assertEqual(file_helper.format_filename(r'a/b\c?d.e"f*g<h>i|j'), 'abcdefghij')

    def test_create_dir_if_not_exist(self):
        path = self.path
        file_helper.create_dir_if_not_exist(path)
        self.assertTrue(os.path.exists(path))

    def test_write_article(self):
        path = self.path
        file_helper.create_dir_if_not_exist(path)
        file_helper.write_article(self.article, self.title, path)

        filename = self.title + '.txt'
        file_path = os.path.join(path, filename)
        self.assertTrue(os.path.exists(file_path))


if __name__ == '__main__':
    unittest.main()
