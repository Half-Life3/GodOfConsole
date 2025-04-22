import os
from os.path import isfile, isdir

import flet as ft
import io
import sys
from backend import GodOfConsole


def main(page: ft.Page):
    expanded_dirs = {}  # Состояние: путь -> раскрыт ли
    back_stack = []  # нужен для реализации кнопок вперед и назад
    forward_stack = []  # нужен для реализации кнопок вперед и назад
    selected_item = None  # переменная для хранения выделенного элемента

    # e - это событие, которое передаёт flet, e = None - нужен когда хочется вручную вызвать функцию update_display
    def update_display(e=None):
        lv.controls.clear()
        lv.controls.extend(render_directory(path.value))
        page.update()

    def button_back(e=None):
        parent_path = os.path.dirname(path.value)
        # path.value = parent_path
        if parent_path != path.value:
            back_stack.append(path.value)
            path.value = parent_path
            forward_stack.clear()
            update_display()

    def button_ahead(e=None):
        if back_stack:
            forward_stack.append(path.value)
            path.value = back_stack.pop()
            update_display()

    page.title = "Файловый менеджер"

    path = ft.TextField(label="Есть только путь", value=os.getcwd(), width=900, height=50)
    path_row = ft.Row([
        ft.ElevatedButton("Назад", on_click=button_back, width=60, height=60, style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=0)
        )),
        path,
        ft.ElevatedButton("Обновить", on_click=update_display, width=90, height=60, style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=0)
        )),
        ft.ElevatedButton("Вперед", on_click=button_ahead, width=80, height=60, style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=0)
        ))
    ])
    page.add(path_row)

    def copy(e):
        """Копирование файла локально"""
        if selected_item is None:
            return
        else:
            GodOfConsole.copy_file(userdata=selected_item, destination_path=None)
            update_display()

    def delete(e):
        """Удаление файла"""
        if selected_item is None:
            return
        else:
            GodOfConsole.delete_file_or_dir(userdata=selected_item)
            update_display()

    def rename(e):
        """Переименовать файл"""
        if selected_item is None:
            return
        else:
            GodOfConsole.rename(path=selected_item, recursive=False)
            update_display()

    def rename_r(e):
        """Переименовать файл"""
        if selected_item is None:
            return
        else:
            GodOfConsole.rename(path=selected_item, recursive=True)
            update_display()

    def capture_print(func, *args, **kwargs):
        """Метод для пеерехвата инфы из print()"""
        # Создаем объект для захвата вывода
        captured_output = io.StringIO()
        sys.stdout = captured_output  # Перенаправляем stdout в StringIO

        func(*args, **kwargs)  # Вызываем функцию, которая вызывает print()

        # Восстанавливаем stdout
        sys.stdout = sys.__stdout__

        return captured_output.getvalue()  # Возвращаем захваченный вывод

    def find(e):
        """Найти файлы по маске re. Извините за грубый вывод - если найдено много файлов, они не влезают в алерт"""

        if selected_item is None:
            return
        if selected_item and isdir(selected_item):

            dlg = ft.AlertDialog(
                title=ft.Text(
                    f"Найденные файлы:\n {capture_print(GodOfConsole.find_files, path=selected_item, mask=find_textfield.value)}",size=10)
            )
            page.open(dlg)
            update_display()

    def filecount(e):
        """Команда, подсчитывающая количество файлов в папке (в том числе вложенные)"""
        if selected_item is None:
            return
        if selected_item and isdir(selected_item):
            dlg = ft.AlertDialog(
                title=ft.Text(
                    f"Количество файлов:\n {capture_print(GodOfConsole.filecount_in_dir, path=selected_item)}")
            )
            page.open(dlg)
            update_display()


    def analyse(e):
        """Команда, запускающая анализ всех вложенных папок и файлов"""
        if selected_item is None:
            return
        if selected_item and isdir(selected_item) and sizelimit_textfield.value:
            dlg = ft.AlertDialog(
                title=ft.Text(
                    f"Найденные файлы:\n {capture_print(GodOfConsole.analyse_workdir, path=selected_item, size_limit=int(sizelimit_textfield.value))}", size=10)
            )
            page.open(dlg)
            update_display()

    find_textfield = ft.TextField(label="Найти по маске", value=None, width=300, height=50)
    sizelimit_textfield = ft.TextField(label="Sizelimit(byte)", value=None, width=140, height=50)

    util_row = ft.Row([
        ft.ElevatedButton("local copy", on_click=copy, width=100, height=40, style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=0)
        )),
        ft.ElevatedButton("delete", on_click=delete, width=80, height=40, style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=0)
        )),
        ft.ElevatedButton("rename", on_click=rename, width=80, height=40, style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=0)
        )),
        ft.ElevatedButton("rename_r", on_click=rename_r, width=80, height=40, style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=0)
        )),
        ft.ElevatedButton("find", on_click=find, width=80, height=40, style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=0)
        )),
        find_textfield,
        ft.ElevatedButton("filecount", on_click=filecount, width=80, height=40, style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=0)
        )),
        ft.ElevatedButton("analyse", on_click=analyse, width=80, height=40, style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=0)
        )),
        sizelimit_textfield
    ])
    page.add(util_row)

    lv = ft.ListView(expand=True, spacing=10, padding=20, auto_scroll=False)
    page.add(lv)

    def select_item(e, full_path):
        """Функция для работы с выделением элемента"""
        nonlocal selected_item
        if selected_item and selected_item == full_path:
            selected_item = None
        elif selected_item != full_path:
            selected_item = full_path
        else:
            selected_item = full_path  # Обновляем выделенный элемент
        update_display()

    def render_directory(path, level=0):
        items = []

        try:
            entries = sorted(os.listdir(path))
        except Exception as e:
            return [ft.Text(f"{'    ' * level}❌ Ошибка доступа: {e}")]

        for item in entries:
            full_path = os.path.join(path, item)
            indent = '    ' * level

            def on_item_click(e, path=full_path):
                select_item(e, path)

            # Изменяем стиль текста в зависимости от того, выбран ли элемент
            item_style = ft.TextStyle(color="blue" if selected_item == full_path else None)

            if os.path.isdir(full_path):
                is_expanded = expanded_dirs.get(full_path, False)

                def toggle_expand(e, path=full_path):
                    expanded_dirs[path] = not expanded_dirs.get(path, False)
                    update_display()

                icon = "expand_more" if is_expanded else "chevron_right"

                items.append(
                    ft.Row([
                        ft.IconButton(icon=icon, on_click=toggle_expand, icon_size=16),
                        ft.Container(content=ft.Text(f"{indent}📁 {item}", style=item_style), on_click=on_item_click)
                    ])
                )

                if is_expanded:
                    items.extend(render_directory(full_path, level + 1))

            else:
                items.append(ft.Row([
                    ft.Container(width=34),  # отступ под иконку
                    ft.Container(content=ft.Text(f"{indent}📄 {item}", style=item_style), on_click=on_item_click)
                ]))
        return items


ft.app(target=main)
