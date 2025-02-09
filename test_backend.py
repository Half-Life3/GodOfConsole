import unittest
import os
import backend


class TestBackend(unittest.TestCase):
    def setUp(self):
        backend.prepare_env()

    def tearDown(self):
        backend.clear_env()

    def test_workdirectory(self):
        actual_data = os.getcwd()
        expected_data = r'X:\Projects\GodOfConsole'
        self.assertEqual(actual_data, expected_data)

    def test_prepare_environment(self):
        expect_data = ['test.txt']
        actual_data = os.listdir(os.path.join(os.getcwd(), 'experiment_directory'))
        self.assertEqual(actual_data, expect_data)

    def test_copy(self):
        # copy_file_in_workdir('test.txt')
        source_path = os.path.join(os.getcwd(), 'experiment_directory')
        self.assertEqual(os.listdir(source_path), ['copy_test.txt', 'test.txt'])

    def test_delete_file(self):
        pass

    def test_delete_dir(self):
        pass

    def test_check_data_format_fileExist(self):
        object1 = backend.GodOfConsole()
        expect_data = 'Это файл'
        actual_data = object1.check_data_format('test.txt')
        self.assertEqual(expect_data, actual_data)

    def test_check_data_format_fileExist(self):
        object1 = backend.GodOfConsole()
        expect_data = 'Это файл'
        actual_data = object1.check_data_format(r'X:\Projects\GodOfConsole\test.txt')
        self.assertEqual(expect_data, actual_data)

    def test_check_data_format_fileNoExist(self):
        object1 = backend.GodOfConsole()
        expect_data = 'Это не файл и не папка'
        actual_data = object1.check_data_format('test.txtx')
        self.assertEqual(expect_data, actual_data)

    def test_check_data_format_DirExist(self):
        object1 = backend.GodOfConsole()
        expect_data = 'Это папка'
        actual_data = object1.check_data_format('test')
        self.assertEqual(expect_data, actual_data)

    def test_check_data_format(self):
        pass


if __name__ == '__main__':
    unittest.main(verbosity=1)
