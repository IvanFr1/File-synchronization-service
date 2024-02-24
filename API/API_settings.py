import os
import requests
from config_data.config import token_api, remove_path, local_path

class YandexDiskConnector:
    def __init__(self, token_api, remove_path):
        self.token_api = token_api
        self.remove_path = remove_path
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
                response = requests.get(f'{self.initial_url}/resources/upload?path={self.remove_path}/'
                                        f'{local_file}&overwrite=true',
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
        encoded_file_name = file_name.replace(" ", "%20")

        url = f"{self.initial_url}/resources?path={self.remove_path}/{encoded_file_name}"

        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()

            print(f"File {file_name} deleted successfully from Yandex Disk.")

        except requests.exceptions.RequestException as e:
            print(f"Error during file deletion: {e}")

    def update_file(self, local_file_path, file_name):
        try:
            self.delete_file(file_name)

            self.upload_files_in_directory(local_file_path)

            print(f"File {file_name} overwritten successfully on Yandex Disk.")

        except requests.exceptions.RequestException as e:
            print(f"Error during file update: {e}")


# connector = YandexDiskConnector(token_api, remove_path)
# print(connector.upload_files_in_directory(local_path))
# print(connector.update_file(local_path, 'tytyt.txt'))
# print(connector.get_cloud_files_info())
