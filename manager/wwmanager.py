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


class Manager:
    def __init__(self, root_path: str, suffixes: List[str], period: int = 1):
        self.file_system = FileSystem(root_path, suffixes)
        self.period = period
        
    def run(self):
        while True:
            # connect to file system
            self.file_system.connect()

            # update all files
            self.file_system.update_files()
            # delete files that was removed
            if to_be_deleted := self.file_system.get_removed_files():
                # use delete api to delete files
                ...
                # clear deleted files
                self.file_system.clear_removed_files()
            # upload new files
            if to_be_uploaded := self.file_system.get_new_files():
                # use upload api to upload files
                ...
                # update file status to 2
                for file_path in to_be_uploaded:
                    self.file_system.db.update("ragflow", "status = ?", "path = ?", (2, file_path))
            # update updated files
            if to_be_updated := self.file_system.get_updated_files():
                # use delete and upload api to update files
                ...
                # update file status to 2
                for file_path in to_be_updated:
                    self.file_system.db.update("ragflow", "status = ?", "path = ?", (2, file_path))
            # start to parse files
            if to_be_parsed := self.file_system.get_unprocessed_files():
                # use parse api to parse files
                ...
                # update file status to 4
                for file_path in to_be_parsed:
                    self.file_system.db.update("ragflow", "status = ?", "path = ?", (4, file_path))

            # disconnect from file system
            self.file_system.disconnect()

            # sleep for period days
            time.sleep(self.period * 24 * 60 * 60)
