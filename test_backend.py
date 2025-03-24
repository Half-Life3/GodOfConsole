import unittest
import os
import backend
from backend import GodOfConsole


class TestBackend(unittest.TestCase):
    def setUp(self):
        backend.prepare_env()

    def tearDown(self):
        backend.clear_env()


    def test_prepare_environment(self):
        expect_data = ['test.txt']
        actual_data = os.listdir(os.path.join(os.getcwd(), 'experiment_directory'))
        print(f'{expect_data} соответствует {actual_data}')
        self.assertEqual(actual_data, expect_data)

    def test_copy(self):
        expect_data = ['test.txt', 'test_copy.txt']
        destinatation = os.path.join(os.getcwd(), 'experiment_directory')
        GodOfConsole.set_workdirectory(destinatation)
        GodOfConsole.copy_file(userdata='test.txt', destination_path=destinatation)
        actual_data = os.listdir(os.path.join(os.getcwd(), 'experiment_directory'))
        print(f'{expect_data} соответствует {actual_data}')
        self.assertEqual(expect_data, actual_data)

    def test_delete_file(self):
        expect_data = []
        userdata = os.path.join(os.getcwd(), 'experiment_directory', 'test.txt')
        GodOfConsole.delete_file_or_dir(userdata=userdata)
        actual_data = os.listdir(os.path.join(os.getcwd(), 'experiment_directory'))
        print(f'{expect_data} соответствует {actual_data}')
        self.assertEqual(expect_data, actual_data)

    def test_delete_dir(self):
        userdata = os.path.join(os.getcwd(), 'experiment_directory')
        GodOfConsole.delete_file_or_dir(userdata=userdata)
        self.assertEqual(False, os.path.exists(userdata))
        os.mkdir(userdata)

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
