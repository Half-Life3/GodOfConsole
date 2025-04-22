import datetime
import os
import sys
import shutil
import re
from dataclasses import dataclass
from logging import raiseExceptions
from subprocess import check_call


def prepare_env():
    if os.path.exists(os.path.join(os.getcwd(), 'experiment_directory')):
        return print('Experiment Env уже существует')
    else:
        os.mkdir(f"{os.getcwd()}/experiment_directory/")
        with open(f"{os.getcwd()}/experiment_directory/test.txt", 'w') as file:
            file.write('Hello, world!')
        return print('Каталог Experiment создан')


def clear_env():

    GodOfConsole.delete_filled_dir(GodOfConsole, 'experiment_directory')
    return print('Каталог Experiment удален \n _____________________________')


class GodOfConsole:
    _workdirectory: str = os.getcwd()
    _destination: str
    _filename: str
    filemask = r'^[a-zA-Z0-9_]+\.[a-zA-Z0-9]+$'

    @classmethod
    def get_workdirectory(cls):
        return cls._workdirectory

    @classmethod
    def set_workdirectory(cls, value):
        if os.path.exists(value):
            cls._workdirectory = value
        else:
            print('Путь не существует')

    @classmethod
    def get_destination(cls):
        return cls._destination

    @classmethod
    def set_destination(cls, value):
        if value == None:
            cls._destination = cls.get_workdirectory()
        elif os.path.exists(value):
            cls._destination = value
            print(f'destination set to {cls._destination}')

        else:
            print('Путь не существует')

    @classmethod
    def get_filename(cls):
        return cls._filename

    @classmethod
    def set_filename(cls, value):
        # если полный путь с именем
        if os.path.isfile(value):
            cls._filename = os.path.basename(value)
        cls._filename = value

    @classmethod
    def get_abs_path_for_file(cls, data: str):
        """Хочу знать что за данные вводит пользователь"""
        if cls.check_filename_format(data) and os.path.isfile(data):
            return os.path.join(cls.get_workdirectory(), data)
        else:
            raise TypeError('Это не файл')

    @classmethod
    def check_filename_format(cls, filename: str) -> bool:
        """Регулярное выражение для проверки формата name.format"""
        return bool(re.match(cls.filemask, filename))

    def check_exist_file(cls, data: str) -> bool:

        return os.path.exists(data)

    @classmethod
    def is_absolute_path(cls, path: str):
        """Method from os doc"""
        return os.path.isabs(path)

    @classmethod
    def get_filename_from_path(cls, absolute_path: str):
        """Method from os doc"""
        if cls.is_absolute_path(absolute_path):
            return os.path.basename(absolute_path)

    def delete_filled_dir(cls, top: str) -> bool:
        """Method from os doc"""
        if os.path.exists(top):
            for root, dirs, files in os.walk(top, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(top)
            return True
        else:
            raise FileNotFoundError

    @classmethod
    def copy_file(cls, userdata: str, destination_path: str = None):
        """(легкое) команда, которая позволяет копировать файл(пример использования: manager copy test.txt"""
        cls.set_filename(userdata)
        cls.set_destination(destination_path)
        file_name_without_extension, file_extension = os.path.splitext(cls.get_filename())
        new_file_name = file_name_without_extension + "_copy" + file_extension
        shutil.copyfile(os.path.join(cls.get_workdirectory(), cls.get_filename()),
                        os.path.join(cls.get_destination(), new_file_name))
        return print(
            f'Файл "{cls.get_filename()}" успешно скопирован в "{cls.get_destination()}"')

    @classmethod
    def delete_file_or_dir(cls, userdata: str):
        """команда, которая удаляет файл или папку(пример использования: manager delete folder_name)"""
        if os.path.isfile(userdata):
            os.remove(userdata)
            print(f"Файл '{userdata}' был удален")
        elif os.path.isdir(userdata):
            shutil.rmtree(userdata)
            print(f"Папка '{userdata}' была удалена")
        else:
            print(f"'{userdata}' - невалидные данные")

    @classmethod
    def filecount_in_dir(cls, path: str):
        """(среднее) команда, подсчитывающая количество файлов в папке (в том числе вложенные"""
        file_count = 0
        for root, dirs, files in os.walk(path):
            file_count += len(files)
        return print(file_count)

    @classmethod
    def find_files(cls, path: str, mask: str):
        """(среднее) команда, ищущая все подходящие файлы в папке (в том числе
    вложенные) по фильтру (например, через регулярное выражение. Будет
    полезно почитать про библиотеку re)"""
        matching_files = []
        regex = re.compile(mask)

        for root, dirs, files in os.walk(path):
            for file in files:
                if regex.search(file):
                    print(f'{root}{file}\n')
                    matching_files.append(os.path.join(root, file))

        return print(matching_files)

    @classmethod
    def rename(cls, path: str, recursive: bool):
        """(среднее) команда, добавляющая в название файла дату его создания (если
    выбрана папка - во все файлы в папке, если есть ключ --recursive - во все
    файлы даже на нескольких уровнях вложения, метаданные файла можно
    получить например через библиотеку os)"""
        if os.path.isfile(path):
            cls._renamefile(path)
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    cls._renamefile(file_path)
                # Если не рекурсивный, выходим из цикла после первого уровня
                if not recursive:
                    break
        else:
            return print('Error')

    @classmethod
    def _renamefile(cls, path: str):
        """(среднее) команда, добавляющая в название файла дату его создания (если
    выбрана папка - во все файлы в папке, если есть ключ --recursive - во все
    файлы даже на нескольких уровнях вложения, метаданные файла можно
    получить например через библиотеку os)"""
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

    @classmethod
    def analyse_workdir(cls, path: str, size_limit: int):
        """(сложное) команда, запускающая анализ всех вложенных папок и файлов, и
    выводящая информацию о том, насколько большие файлы находятся на уровне
    вызова. Способ вывода любой (но только через консоль), например:
    manager analyse"""
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                    if file_size > size_limit:
                        print(f"Файл: {file_path}, Размер: {file_size} байт")
                except Exception as e:
                    print(f"Не удалось получить размер файла {file_path}: {e}")
