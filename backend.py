import datetime
import os
import sys
import shutil
import re


def prepare_env():
    if os.path.exists(os.path.join(os.getcwd(), 'experiment_directory')):
        return print('Experiment Env уже существует')
    else:
        os.mkdir(f"{os.getcwd()}/experiment_directory/")
        with open(f"{os.getcwd()}/experiment_directory/test.txt", 'w') as file:
            file.write('Hello, world!')
        return print('Каталог Experiment для создан')


def clear_env():
    GodOfConsole.delete_filled_dir(GodOfConsole, 'experiment_directory')
    return print('Каталог Experiment удален \n _____________________________')


class GodOfConsole:
    workdirectory = None
    targetdirectory = None
    targetfile = None
    filemask = r'^[a-zA-Z0-9_]+\.[a-zA-Z0-9]+$'

    def check_data_format(self, data: str):
        """Хочу знать что за данные вводит пользователь"""
        if os.path.isfile(data):
            return "Это файл"
        elif os.path.isdir(data):
            return "Это папка"
        else:
            return "Это не файл и не папка"

    def check_filename_format(self, filename: str):
        """Регулярное выражение для проверки формата name.format"""
        return bool(re.match(self.filemask, filename))

    def is_absolute_path(self, path: str):
        """Method from os doc"""
        return os.path.isabs(path)

    def get_filename_from_path(self, absolute_path: str):
        """Method from os doc"""
        if self.is_absolute_path(absolute_path):
            return os.path.basename(absolute_path)

    def getworkdirectory(self):
        self.workdirectory = os.getcwd()
        return self.workdirectory

    def delete_filled_dir(self, top: str) -> bool:
        """Method from os doc"""
        for root, dirs, files in os.walk(top, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(top)
        return True

    def copy_file(self, path: str) -> bool:
        """(легкое) команда, которая позволяет копировать файл(пример использования: manager copy test.txt"""
        if self.is_absolute_path(path) or self.check_filename_format(path):
            source_path = os.path.join(self.getworkdirectory(), self.get_filename_from_path(path))
            destination_path = os.path.join(self.workdirectory, f'copy_{self.get_filename_from_path(path)}')
            if os.path.exists(source_path):
                shutil.copyfile(source_path, destination_path)
                print(f'Файл "{self.get_filename_from_path(path)}" успешно скопирован в "{self.workdirectory}"')
                return True
            else:
                print(f'Указанный файл "{self.get_filename_from_path(path)}" не найден')
                return False
        else:
            print('Error in copy method')

    def delete_file_or_dir(self, path: str):
        """команда, которая удаляет файл или папку(пример использования: manager delete folder_name)"""
        if os.path.isfile(path):
            os.remove(path)
            print(f"Файл '{path}' был удален")
        elif os.path.isdir(path):
            shutil.rmtree(path)
            print(f"Папка '{path}' была удалена")
        else:
            print(f"'{path}' не является ни файлом, ни папкой")

    def filecount_in_dir(self, path: str) -> int:
        """(среднее) команда, подсчитывающая количество файлов в папке (в том числе вложенные"""
        file_count = 0
        for root, dirs, files in os.walk(path):
            file_count += len(files)
        return file_count

    def find_files(self, path: str, mask: str):
        """(среднее) команда, ищущая все подходящие файлы в папке (в том числе
    вложенные) по фильтру (например, через регулярное выражение. Будет
    полезно почитать про библиотеку re)"""
        matching_files = []
        regex = re.compile(mask)

        for root, dirs, files in os.walk(path):
            for file in files:
                if regex.search(file):
                    matching_files.append(os.path.join(root, file))

        return matching_files

    def rename_file(self, path: str):
        """(среднее) команда, добавляющая в название файла дату его создания (если
    выбрана папка - во все файлы в папке, если есть ключ --recursive - во все
    файлы даже на нескольких уровнях вложения, метаданные файла можно
    получить например через библиотеку os)"""
        if self.check_data_format(path) == 'Это файл':
            # Получаем время создания файла
            creation_time = os.path.getctime(path)
            creation_date = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d')

            # Получаем директорию и имя файла
            directory, filename = os.path.split(path)

            # Создаем новое имя файла
            new_filename = f"{creation_date}_{filename}"
            new_path = os.path.join(directory, new_filename)

            # Переименовываем файл
            os.rename(path, new_path)
            return print(f"Файл '{path}' переименован в: '{new_path}'")
        else:
            return print('Error')

    def rename_files_in_dir(self, path: str, recursive: bool):
        if self.check_data_format(path) == 'Это папка':
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    self.rename_file(file_path)
                # Если не рекурсивный, выходим из цикла после первого уровня
                if not recursive:
                    break
        else:
            return print('Error')

    def analyse_workdir(self, path):
        """(сложное) команда, запускающая анализ всех вложенных папок и файлов, и
    выводящая информацию о том, насколько большие файлы находятся на уровне
    вызова. Способ вывода любой (но только через консоль), например:
    manager analyse"""
        pass