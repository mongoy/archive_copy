"""
Архивация и копирование
"""
import json
import os
import zipfile
import datetime


def check_dir(path_dir):
    """
    Скрипт проверяет наличие пути.
    Если файл, то выводит его размер, даты создания, открытия и модификации.
    Если каталог, выводит список вложенных в него файлов и каталогов.
    :return:
    """
    status = 0
    if os.path.exists(path_dir):
        if os.path.isfile(path_dir):
            print(f'ФАЙЛ: {path_dir}')
            print('Размер:', round(os.path.getsize(path_dir) / 1024, 3), 'Кб')
            print('Дата создания:', \
                  datetime.datetime.fromtimestamp(int(os.path.getctime(path_dir))))
            print('Дата последнего открытия:', \
                  datetime.datetime.fromtimestamp(int(os.path.getatime(path_dir))))
            print('Дата последнего изменения:', \
                  datetime.datetime.fromtimestamp(int(os.path.getmtime(path_dir))))
            status = 2
        elif os.path.isdir(path_dir):
            print('КАТАЛОГ')
            print('Список объектов в нем: ', os.listdir(path_dir))
            status = 1
    else:
        print('Объект не найден')
    return status


def archive_directory():
    base_dir = os.path.abspath("")
    with zipfile.ZipFile("qqq.zip", "w") as zf:
        pass


def copy_zip_file():
    pass


def main():
    # наличие файла конфигурации
    if check_dir("config.json") == 2:
        with open("config.json", "r", encoding="utf-8") as conf:
            text = json.load(conf)  # dict
            src, dst = text.values()  #
            print(src, dst)

    # archive_directory()
    # copy_zip_file()


if __name__ == '__main__':
    main()
