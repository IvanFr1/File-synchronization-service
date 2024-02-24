import time
from datetime import datetime, timezone
import os
from loguru import logger
from API.API_settings import YandexDiskConnector
from config_data.config import token_api, remove_path, local_path


def setup_logger():
    logger.add(
        "logfile.log",
        rotation="5 MB",
        level="INFO",
        format="{function} {time:YYYY-MM-DD HH:mm:ss} {level: <8}{message}",
    )
    return logger


def synchronize():
    try:
        logger.info(f"Программа синхронизации файлов начинает работу с директорией {local_path}")

        connect = YandexDiskConnector(token_api, remove_path)
        remove_info = connect.get_cloud_files_info()
        local_files = os.listdir(local_path)
        for files in remove_info:
            if files not in local_files:
                connect.delete_file(files)
                try:
                    logger.info(f'Файл {files} успешно удален с Яндекс диска')
                except Exception as error_delete:
                    logger.error(f'Файл {files} ошибка при удалении с Яндекс диска: {error_delete}')

        for local_file in local_files:
            if local_file not in remove_info:
                local_file_path = os.path.join(local_path, local_file)
                connect.upload_file(local_file_path)
                try:
                    logger.info(f'Файл {local_file} успешно записан на Яндекс диск')
                except Exception as error_loaded:
                    logger.error(f'Файл {local_file} не записан на Яндекс диск. Ошибка: {error_loaded}')

        for cloud_file in remove_info:
            local_file_path = os.path.join(local_path, cloud_file)
            if os.path.exists(local_file_path):
                local_file_modified_time = os.path.getmtime(local_file_path)
                modified_datetime = datetime.fromtimestamp(local_file_modified_time, tz=timezone.utc)
                cloud_file_modified_time = remove_info[cloud_file]
                if modified_datetime > cloud_file_modified_time:
                    connect.update_file(local_file_path, cloud_file)
                    try:
                        logger.info(f'Файл {cloud_file} успешно перезаписан на Яндекс диск')
                    except Exception as error_upload:
                        logger.error(f'Файл {cloud_file} не перезаписан на Яндекс диск. Ошибка: {error_upload}')

    except Exception as err:
        logger.error(f"Программа синхронизации файлов не может начать работу с директорией {local_path}. Ошибка {err}")


def main():
    setup_logger()

    while True:
        synchronize()
        time.sleep(30)


if __name__ == "__main__":
    main()
