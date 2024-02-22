import os
import requests
from config_data.config import local_path


class YandexDiskConnector:
    def __init__(self, token_api, remove_path):
        self.token_api = token_api
        self.remove_path = remove_path
        self.local_path = local_path
        self.initial_url = 'https://cloud-api.yandex.net/v1/disk'

    def _get_headers(self):
        return {'Content-Type': 'application/json', 'Accept': 'application/json',
                'Authorization': f'OAuth {self.token_api}'}

    def get_cloud_files_info(self):
        headers = self._get_headers()
        url = f'{self.initial_url}/resources?path={self.remove_path}&type=file&limit=100'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            files_info = response.json().get('_embedded', {}).get('items', [])
            filtered_info = dict()

            for file_info in files_info:
                name = file_info.get('name')
                created = file_info.get('created')

                filtered_info[name] = created

            return filtered_info
        else:
            return []

    def upload_files_in_directory(self, local_directory):
        headers = self._get_headers()
        local_files = [f for f in os.listdir(local_directory) if os.path.isfile(os.path.join(local_directory, f))]

        for local_file in local_files:

            local_path = os.path.join(local_directory, local_file)

            try:
                response = requests.get(f'{self.initial_url}/resources/upload?path={self.remove_path}/{local_file}',
                                        headers=headers)
                response.raise_for_status()

                upload_url = response.json()['href']

                with open(local_path, 'rb') as file:
                    response = requests.put(upload_url, files={'file': file})
                    response.raise_for_status()

            except requests.exceptions.RequestException as e:
                print(f"Error during file upload: {e}")

    def delete_file(self, file_name):
        headers = self._get_headers()
        encoded_file_name = file_name.replace(" ", "%20")  # Если в имени файла есть пробелы

        url = f"{self.initial_url}/resources?path={self.remove_path}/{encoded_file_name}"

        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()

            print(f"File {file_name} deleted successfully from Yandex Disk.")

        except requests.exceptions.RequestException as e:
            print(f"Error during file deletion: {e}")

#     def update_file(self, file_name):
#         headers = self._get_headers()
#
#         try:
#             # Читаем содержимое файла
#             with open(os.path.join(self.local_path, file_name), 'rb') as file:
#                 file_content = file.read()
#
#             # Отправляем PUT-запрос для обновления файла напрямую на Яндекс Диск
#             url = f"{self.initial_url}/resources/upload"
#             params = {
#                 "path": f"{self.remove_path}/{file_name}",
#                 "overwrite": "true"  # Указываем, что мы хотим перезаписать существующий файл
#             }
#             response = requests.put(url, headers=headers, params=params, data=file_content)
#             response.raise_for_status()
#
#             print(f"File {file_name} updated successfully on Yandex Disk.")
#
#         except requests.exceptions.RequestException as e:
#             print(f"Error during file update: {e}")
#
#
# result = YandexDiskConnector(token_api, remove_path)
#
# print(result.update_file('tytyt.txt'))
