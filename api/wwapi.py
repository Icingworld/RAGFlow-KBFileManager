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
from utils.wwencrypt import rsa_psw


class WebApi:
    """Web operation api.
    """
    def __init__(self, url_base: str, email: str, password: str, kb_id: str):
        self.url_base = url_base if url_base.endswith("/") else url_base + "/"
        self.email = email
        self.password = password
        self.headers = {
            "Authorization": "",
        }
        self.kb_id = kb_id

    def login(self) -> bool:
        """Login to web.
        """
        url = self.url_base + "user/login"
        data = {
            "email": self.email,
            "password": self.__encrypt_passwd()
        }

        try:
            response = requests.post(url, data = json.dumps(data))
            code = json.loads(response.text).get("code")
            if code == 0:
                logger.debug("Login success.")
                auth = response.headers.get("Authorization")
                if auth:
                    self.headers["Authorization"] = auth
                    return True
                else:
                    logger.error("Authorization not found.")
                    return False
            else:
                logger.debug(response.text)
                logger.error("Login failed.")
                return False
        except Exception as e:
            logger.error(e)
            logger.debug(response.text)
            return False

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
                data = json.loads(response.text).get("data")
                docs = data.get("docs")
                for doc in docs:
                    res.append((doc.get("name"), doc.get("id")))
                # calculate page num
                if max_page == 0:
                    max_page = math.ceil(data.get("total") / 100)
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
                return json.loads(response.text).get("code") == 0
        except Exception as e:
            logger.error(e)
            return False

    def upload_files(self, file_paths: List[str], file_names: List[str]) -> bool:
        """Upload multiple files to web.
        """
        url = self.url_base + "document/upload"
        data = {
            "kb_id": self.kb_id
        }
        
        files = []

        try:
            for file_path, file_name in zip(file_paths, file_names):
                f = open(file_path, "rb")
                files.append(("file", (file_name, f)))

            response = requests.post(url, files = files, data = data, headers = self.headers)
            logger.debug(response.text)
            return json.loads(response.text).get("code") == 0
        except Exception as e:
            logger.error("uploads")
            logger.error(e)
            return False
        finally:
            # close all files
            for _, (_, file_obj) in files:
                file_obj.close()


    def delete_file(self, file_id: str) -> bool:
        """Delete a file from web.
        """
        url = self.url_base + "document/rm"
        data = {
            "doc_id": [
                file_id
            ]
        }

        try:
            response = requests.post(url, data = json.dumps(data), headers = self.headers)
            logger.debug(response.text)
            return json.loads(response.text).get("code") == 0
        except Exception as e:
            logger.error(e)
            return False

    def delete_files(self, file_ids: List[str]) -> bool:
        """Delete files from web.
        """
        url = self.url_base + "document/rm"
        data = {
            "doc_id": file_ids
        }

        try:
            response = requests.post(url, data = json.dumps(data), headers = self.headers)
            logger.debug(response.text)
            return json.loads(response.text).get("code") == 0
        except Exception as e:
            logger.error(e)
            return False

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

        try:
            response = requests.post(url, data = json.dumps(data), headers = self.headers)
            logger.debug(response.text)
            return json.loads(response.text).get("code") == 0
        except Exception as e:
            logger.error(e)
            return False

    def parse_files(self, file_ids: List[str]) -> bool:
        """Start files' parsing.
        """
        url = self.url_base + "document/run"
        data = {
            "doc_ids": file_ids,
            "run": 1,
            "delete": "false"
        }
        
        try:
            response = requests.post(url, data = json.dumps(data), headers = self.headers)
            logger.debug(response.text)
            return json.loads(response.text).get("code") == 0
        except Exception as e:
            logger.error(e)
            return False

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
        
        try:
            response = requests.post(url, data = json.dumps(data), headers = self.headers)
            logger.debug(response.text)
            return json.loads(response.text).get("code") == 0
        except Exception as e:
            logger.error(e)
            return False

    def cancel_files(self, file_ids: List[str]) -> bool:
        """Cancel files' parsing.
        """
        url = self.url_base + "document/run"
        data = {
            "doc_ids": file_ids,
            "run": 2,
            "delete": "false"
        }
        
        try:
            response = requests.post(url, data = json.dumps(data), headers = self.headers)
            logger.debug(response.text)
            return json.loads(response.text).get("code") == 0
        except Exception as e:
            logger.error(e)
            return False

    def __encrypt_passwd(self) -> str:
        """Encrypt password.
        """
        public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArq9XTUSeYr2+N1h3Afl/z8Dse/2yD0ZGrKwx+EEEcdsBLca9Ynmx3nIB5obmLlSfmskLpBo0UACBmB5rEjBp2Q2f3AG3Hjd4B+gNCG6BDaawuDlgANIhGnaTLrIqWrrcm4EMzJOnAOI1fgzJRsOOUEfaS318Eq9OVO3apEyCCt0lOQK6PuksduOjVxtltDav+guVAA068NrPYmRNabVKRNLJpL8w4D44sfth5RvZ3q9t+6RTArpEtc5sh5ChzvqPOzKGMXW83C95TxmXqpbK6olN4RevSfVjEAgCydH6HN6OhtOQEcnrU97r9H0iZOWwbw3pVrZiUkuRD1R56Wzs2wIDAQAB
-----END PUBLIC KEY-----"""
        return rsa_psw(self.password, public_key)
