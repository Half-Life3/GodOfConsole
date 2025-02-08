import os
import sys
import shutil
import re

class GodOfConsole:



    def delete_filled_dir(top: str) -> bool:
        for root, dirs, files in os.walk(top, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(top)
        return True


    def prepare_env():
        workdirectory = os.getcwd()
        if os.path.exists(os.path.join(os.getcwd(), 'experiment_directory')):
            return print('Experiment Env уже существует')
        else:
            os.mkdir(f"{workdirectory}/experiment_directory/")
            with open(f"{workdirectory}/experiment_directory/test.txt", 'w') as file:
                file.write('Hello, world!')
            return print('Каталог Experiment для создан')


    def clear_env():
        delete_filled_dir('experiment_directory')
        return print('Каталог Experiment удален \n _____________________________')


    def copy_file_in_workdir(file_name: str) -> bool:
        """(легкое) команда, которая позволяет копировать файл(пример использования: manager copy test.txt"""
        workdirectory = os.path.join(os.getcwd(), 'experiment_directory')
        source_path = os.path.join(workdirectory, file_name)
        destination_path = os.path.join(workdirectory, f'copy_{file_name}')
        if os.path.exists(source_path):
            shutil.copyfile(source_path, destination_path)
            print(f'Файл "{file_name}" успешно скопирован в "{workdirectory}".')
            return True
        else:
            print(f'Указанный файл "{file_name}" не найден.')
            return False


    def delete_file_or_dir(file_name: str):
        """команда, которая удаляет файл или папку(пример использования: manager delete folder_name)"""
        filemask = r'^[a-zA-Z0-9_]+\.[a-zA-Z0-9]+$'
        if bool(re.match(filemask, file_name)):
            os.remove(file_name)
            return print(f'File {file_name} has been deleted.')
        else:
            delete_filled_dir(file_name)
            return print(f'Directory {file_name} has been deleted.')


    def filecount_in_dir() -> int:
        """(среднее) команда, подсчитывающая количество файлов в папке (в том числе вложенные"""
        pass

    def find_files(mask: str):
        """(среднее) команда, ищущая все подходящие файлы в папке (в том числе
    вложенные) по фильтру (например, через регулярное выражение. Будет
    полезно почитать про библиотеку re)"""
        pass

    def rename_files():
        """(среднее) команда, добавляющая в название файла дату его создания (если
    выбрана папка - во все файлы в папке, если есть ключ --recursive - во все
    файлы даже на нескольких уровнях вложения, метаданные файла можно
    получить например через библиотеку os)"""
        pass

    def analyse_workdir():
        """(сложное) команда, запускающая анализ всех вложенных папок и файлов, и
    выводящая информацию о том, насколько большие файлы находятся на уровне
    вызова. Способ вывода любой (но только через консоль), например:
    manager analyse"""
        pass