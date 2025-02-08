import unittest
import os
from backend import *


class TestBackend(unittest.TestCase):
    def setUp(self):
        prepare_env()

    def tearDown(self):
        clear_env()

    def test_workdirectory(self):
        actual_data = os.getcwd()
        expected_data = r'X:\Projects\GodOfConsole'
        self.assertEqual(actual_data, expected_data)

    def test_prepare_environment(self):
        expect_data = ['test.txt']
        actual_data = os.listdir(os.path.join(os.getcwd(), 'experiment_directory'))
        self.assertEqual(actual_data, expect_data)

    def test_copy(self):

        copy_file_in_workdir('test.txt')
        source_path = os.path.join(os.getcwd(), 'experiment_directory')
        self.assertEqual(os.listdir(source_path), ['copy_test.txt', 'test.txt'])

    def test_delete_file(self):



    def test_delete_dir(self):
        pass

    def test_filecount_in_dir(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=1)
