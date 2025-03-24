import os
import flet as ft

def main(page: ft.Page):
    page.title = "Файловый менеджер"
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Компоненты
    path_input = ft.TextField(label="Путь к папке", value=os.getcwd(), width=400)
    file_list = ft.ListView(expand=True)


    def update_file_list(path):
        file_list.controls.clear()
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    file_list.controls.append(ft.ListTile(title=item, on_click=lambda e, p=item_path: update_file_list(p)))
                else:
                    file_list.controls.append(ft.ListTile(title=item))
        except Exception as e:
            file_list.controls.append(ft.ListTile(title=f"Ошибка: {e}"))

        file_list.update()

    def on_path_change(e):
        update_file_list(path_input.value)

    path_input.on_submit = on_path_change
    page.add(path_input, file_list)

    # Инициализация списка файлов
    update_file_list(os.getcwd())

ft.app(target=main)
