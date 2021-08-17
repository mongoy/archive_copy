"""
Архивация и перенос
"""
import json
import os
import zipfile
import datetime
import time
from progress.bar import IncrementalBar
import logging


def check_dir(path_dir):
    """
    Скрипт проверяет наличие пути.
    Если файл, то выводит его размер, даты создания, открытия и модификации.
    Если каталог, выводит список вложенных в него файлов и каталогов.
    :return:
    status, log_text
    """
    status = 0
    if os.path.exists(path_dir):
        log_text = ""
        if os.path.isfile(path_dir):
            log_text += f'ФАЙЛ: {path_dir}\n\t'
            log_text += f'Размер:{round(os.path.getsize(path_dir) / 1024, 3)} Кб\n\t'
            log_text += f'Дата создания:{datetime.datetime.fromtimestamp(int(os.path.getctime(path_dir)))}\n\t'
            log_text += f'Дата последнего открытия:{datetime.datetime.fromtimestamp(int(os.path.getatime(path_dir)))}\n\t'
            log_text += f'Дата последнего изменения:{datetime.datetime.fromtimestamp(int(os.path.getmtime(path_dir)))}\n'
            status = 2
        elif os.path.isdir(path_dir):
            log_text = f'КАТАЛОГ: {path_dir}'
            status = 1
    else:
        log_text = 'Объект не найден'
    return status, log_text


def archive_directory(src, dst):
    src_dir = os.path.abspath(src)
    dst_dir = os.path.abspath(dst)
    arch_file = os.path.join(dst_dir, f"buh_{datetime.datetime.today().strftime('%Y-%m-%d %H_%M')}.zip")
    with zipfile.ZipFile(arch_file, "w") as zf:
        base_path = os.path.split(src)[0]
        # print(base_path)
        for root, dirs, files in os.walk(src):
            # print(root, dirs, files)
            bar = IncrementalBar("Заархивировано файлов", max=len(files))
            for file in files:
                zf.write(os.path.join(root, file))
                bar.next()
                # print(dirs)
                # time.sleep(1)
            bar.finish()
    return arch_file


def main():
    # create log file
    logging.basicConfig(filename='archive_buh.log', filemode='w', level=logging.INFO)
    start_time = time.monotonic()
    logging.info(f"Запуск: {datetime.datetime.now()}")
    # наличие файла конфигурации
    cfg = check_dir("config.json")
    if cfg[0] == 2:
        logging.info(cfg[1])
        with open("config.json", "r", encoding="utf-8") as conf:
            text = json.load(conf)  # dict
            src, dst = text.values()  #
            logging.info(f"{src}; {dst}")
        # наличие директори источника
        cfg = check_dir(src)
        if cfg[0] == 1:  # and (check_dir(dst) == 1):
            # создание архива
            arch_file = archive_directory(src, dst)
            logging.info(f"Время архивации: {time.monotonic() - start_time} сек.")
            logging.info(f"Местоположение архива: {arch_file}")
        else:
            logging.info(f"Проверьте наличие директорий: {src, dst}")
    else:
        logging.info("Проверьте наличие файла конфигурации: config.json")


if __name__ == '__main__':
    main()
