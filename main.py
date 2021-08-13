"""
Архивация и копирование
"""
import json
import os
import zipfile
import datetime
import time


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
            print(f'КАТАЛОГ: {path_dir}')
            # print('Список объектов в нем: ', os.listdir(path_dir))
            status = 1
    else:
        print('Объект не найден')
    return status


def archive_directory(src):
    base_dir = os.path.abspath(src)
    with zipfile.ZipFile("qqq.zip", "w") as zf:
        base_path = os.path.split(src)[0]
        # print(base_path)
        for root, dirs, files in os.walk(src):
            # print(root, dirs, files)
            for file in files:
                zf.write(os.path.join(root, file))
                # print(dirs)
    return


def move_zip_file(file, path):
    os.replace(file, path)


def main():
    start_time = time.monotonic()
    # наличие файла конфигурации
    if check_dir("config.json") == 2:
        with open("config.json", "r", encoding="utf-8") as conf:
            text = json.load(conf)  # dict
            src, dst = text.values()  #
            print(src, dst)
        # наличие директорий
        if (check_dir(src) == 1) and (check_dir(dst) == 1):
            # создание архива
            # archive_directory(src)
            # print(f"Время архивации - {time.monotonic() - start_time} сек.")
            # # перенос архива
            move_zip_file("qqq.zip", os.path.join(os.getcwd(), dst))
        else:
            print(f"Проверьте наличие директорий: {src, dst}")
    else:
        print("Проверьте наличие файла конфигурации - config.json")

    # archive_directory()
    # copy_zip_file()


if __name__ == '__main__':
    main()
