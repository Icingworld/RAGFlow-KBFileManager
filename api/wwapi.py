"""
Module File: wwapi.py
Description: This module contains web operation.

Author: Icingworld
Date: 2025-03-14
Version: 0.1.0
"""

import requests


class WebApi:
    """Web operation api.
    """
    def __init__(self, url_base: str, auth: str, kb_name: str, kb_id: str):
        self.url_base = url_base if url_base.endswith("/") else url_base + "/"
        self.headers = {
            "Authorization": auth,
        }
        self.kb_name = kb_name
        self.kb_id = kb_id

    def get_files(self):
        """Get all files from web.
        """
        url = self.url_base + "document/list?kb_id=" + self.kb_id + "&page=1&page_size=1"
        response = requests.get(url, headers=self.headers)
        ...

    def upload(self, file_path: str) -> bool:
        """Upload a file to web.
        """
        url = self.url_base + "document/upload"
        data = {
            "kb_name": self.kb_name,
            "kb_id": self.kb_id
        }
        response = None

        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(url, files = files, data = data, headers = self.headers)
        
        return response.status_code == 200

    def delete(self, file_path: str) -> bool:
        """Delete a file from web.
        """
        url = self.url_base + "document/delete"
        ...

    def parse(self, file_path: str, status: int) -> bool:
        """Control a file's parsing.
        """
        url = self.url_base + "document/run"
        ...