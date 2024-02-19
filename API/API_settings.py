import os
import requests


class YandexDiskConnector:
    def __init__(self, token_api, remove_path):
        self.token_api = token_api
        self.remove_path = remove_path
