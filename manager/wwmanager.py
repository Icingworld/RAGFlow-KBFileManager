"""
Module File: wwmanager.py
Description: This module contains manager of RAGFlow knowledge base files.

Author: Icingworld
Date: 2025-03-14
Version: 0.1.0
"""

import time
from typing import List
from filesystem.wwfilesystem import FileSystem
from api.wwapi import WebApi


class Manager:
    """Manager of RAGFlow knowledge base files.
    """
    def __init__(self, root_path: str, suffixes: List[str], url_base: str, auth: str, kb_id: str, period: int = 1):
        self.file_system = FileSystem(root_path, suffixes)
        self.api = WebApi(url_base, auth, kb_id)
        self.period = period
        
    def run(self) -> None:
        while True:
            # connect to file system
            self.file_system.connect()
            
            # check database and initialize it if not initialized
            self.file_system.check_db()

            # update all files
            if to_be_deleted := self.file_system.update_files():
                # use delete api to delete files
                self.api.delete_files(to_be_deleted)
            # upload new files
            if to_be_uploaded := self.file_system.get_new_files():
                # use upload api to upload files
                file_paths = [x[0] for x in to_be_uploaded]
                file_names = [x[1] for x in to_be_uploaded]
                self.api.upload_files(file_paths, file_names)
                # update file status to 2
                for file_path in file_paths:
                    self.file_system.db.update("ragflow", "status = ?", "path = ?", (2, file_path))
            # update updated files
            if to_be_updated := self.file_system.get_updated_files():
                # use delete and upload api to update files
                # here should consider file is changed but not uploaded yet
                ...
                # update file status to 2
                for file_path in to_be_updated:
                    # self.file_system.db.update("ragflow", "status = ?", "path = ?", (2, file_path))
                    ...
            # start to parse files
            if to_be_parsed := self.file_system.get_unprocessed_files():
                # use parse api to parse files
                ...
                # update file status to 4
                for file_path in to_be_parsed:
                    # self.file_system.db.update("ragflow", "status = ?", "path = ?", (4, file_path))
                    ...

            # disconnect from file system
            self.file_system.disconnect()

            # sleep for period days
            time.sleep(self.period * 24 * 60 * 60)
