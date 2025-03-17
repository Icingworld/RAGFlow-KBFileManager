"""
Module File: wwapi.py
Description: This module contains web operation.

Author: Icingworld
Date: 2025-03-14
Version: 0.1.0
"""

import requests
import json
import time
import math
from typing import List, Tuple
from utils.wwlog import logger


class WebApi:
    """Web operation api.
    """
    def __init__(self, url_base: str, auth: str, kb_id: str):
        self.url_base = url_base if url_base.endswith("/") else url_base + "/"
        self.headers = {
            "Authorization": auth,
        }
        self.kb_id = kb_id

    def get_files(self) -> List[Tuple[str, str]]:
        """Get all files from web.
        """
        res = []
        page = 1
        max_page = 0  # store max page number

        while page:
            # set max page size to 100
            url = self.url_base + "document/list?kb_id=" + self.kb_id + f"&keywords=&page={page}&page_size=100"
            response = requests.get(url, headers=self.headers)

            try:
                data = json.loads(response.text)["data"]
                docs = data["docs"]
                for doc in docs:
                    res.append((doc["name"], doc["doc_id"]))
                # calculate page num
                if max_page == 0:
                    max_page = math.ceil(data["total"] / 100)
                page = page + 1 if page < max_page else 0
            except Exception as e:
                logger.error(e)
                logger.debug(response.text)
                res.clear()
                break

            time.sleep(1)  # I think it's necessary

        return res

    def upload_file(self, file_path: str, file_name: str) -> bool:
        """Upload a file to web.
        """
        url = self.url_base + "document/upload"
        data = {
            "kb_id": self.kb_id
        }

        try:
            with open(file_path, "rb") as f:
                files = {
                    "file": (file_name, f)
                }
                response = requests.post(url, files = files, data = data, headers = self.headers)
                logger.debug(response.text)
                return json.loads(response.text)["message"] == "success"
        except Exception as e:
            logger.error(e)
            return False

    def upload_files(self, file_paths: List[str], file_names: List[str]) -> bool:
        """Upload files to web.
        """
        url = self.url_base + "document/upload"
        data = {
            "kb_id": self.kb_id
        }
        files = []
        file_objs = []
        for file_path, file_name in zip(file_paths, file_names):
            f = (file_name, open(file_path, "rb"))
            files.append(("file", f))
            file_objs.append(f)
        response = requests.post(url, files = files, data = data, headers = self.headers)
        # for f in file_objs:
        #     f.close()
        logger.debug(response.text)
        return response.status_code == 200

    def delete_file(self, file_id: str) -> bool:
        """Delete a file from web.
        """
        url = self.url_base + "document/rm"
        data = {
            "doc_id": [
                file_id
            ]
        }
        response = requests.post(url, data = data, headers = self.headers)
        logger.debug(response.text)
        return response.status_code == 200

    def delete_files(self, file_ids: List[str]) -> bool:
        """Delete files from web.
        """
        url = self.url_base + "document/rm"
        data = {
            "doc_id": file_ids
        }
        response = requests.post(url, data = data, headers = self.headers)
        logger.debug(response.text)
        return response.status_code == 200

    def parse_file(self, file_id: str) -> bool:
        """Start a file's parsing.
        """
        url = self.url_base + "document/run"
        data = {
            "doc_ids": [
                file_id
            ],
            "run": 1,
            "delete": "false"
        }
        response = requests.post(url, data = data, headers = self.headers)
        logger.debug(response.text)
        return response.status_code == 200

    def parse_files(self, file_ids: List[str]) -> bool:
        """Start files' parsing.
        """
        url = self.url_base + "document/run"
        data = {
            "doc_ids": file_ids,
            "run": 1,
            "delete": "false"
        }
        response = requests.post(url, data = data, headers = self.headers)
        logger.debug(response.text)
        return response.status_code == 200

    def cancel_file(self, file_id: str) -> bool:
        """Cancel a file's parsing.
        """
        url = self.url_base + "document/run"
        data = {
            "doc_ids": [
                file_id
            ],
            "run": 2,
            "delete": "false"
        }
        response = requests.post(url, data = data, headers = self.headers)
        logger.debug(response.text)
        return response.status_code == 200

    def cancel_files(self, file_ids: List[str]) -> bool:
        """Cancel files' parsing.
        """
        url = self.url_base + "document/run"
        data = {
            "doc_ids": file_ids,
            "run": 2,
            "delete": "false"
        }
        response = requests.post(url, data = data, headers = self.headers)
        logger.debug(response.text)
        return response.status_code == 200
