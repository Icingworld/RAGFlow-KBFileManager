"""
Module File: wwfilesystem.py
Description: This module maintains a filesystem for the root directory.

Author: Icingworld
Date: 2025-03-14
Version: 0.1.0
"""

import os
import time
from typing import List, Tuple
from utils.wwhash import calculate_file_hash
from utils.wwsqlite import SQLiteDB
from utils.wwlog import logger


class FileSystem:
    """A manager to maintain root file system.
    """
    def __init__(self, root_dir: str, suffix: List[str]):
        self.root_dir = root_dir
        self.suffix = suffix
        self.db = SQLiteDB()
        
    def check_db(self) -> None:
        """Check database and initialize it if not initialized.

        :return: None
        """
        logger.debug("Checking database...")
        self.db.create_table("ragflow", """
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL,
            filename TEXT NOT NULL,
            extension TEXT NOT NULL,
            hash TEXT NOT NULL,
            status INTEGER NOT NULL,
            doc_id TEXT DEFAULT NULL,
            
            UNIQUE(path)
        """)
        logger.debug("Database successfully initialized.")

    def scan_database(self) -> List[str]:
        """Scan the database and delete files that no longer exist.

        :return: list of removed files
        """
        logger.debug("Scanning database...")

        ret = self.db.fetch_all("SELECT path, status, doc_id FROM ragflow")
        removed_files = []

        for path, status, doc_id in ret:
            if not os.path.exists(path):
                logger.debug(f"File {path} not found, deleting from database.")
                self.db.delete("ragflow", "path =?", (path,))
                if not doc_id:
                    # it won't happen, maybe
                    logger.error(f"File {path} has no doc_id, failed to delete it.")
                    continue
                if status not in (0, 1):
                    logger.debug(f"File {path} not found, deleting from web.")
                    removed_files.append(doc_id)
        
        logger.debug("Scanning completed.")
        return removed_files

    def scan_files(self) -> None:
        """Scan files in the root directory and save their information to the database.

        :return: None
        """
        logger.debug("Scanning root directory...")

        for dir_path, dir_names, filenames in os.walk(self.root_dir):
            # skip hidden directories
            dir_names[:] = [d for d in dir_names if not d.startswith(".")]

            for filename in filenames:
                file_extension = os.path.splitext(filename)[1]
                if file_extension not in self.suffix:
                    logger.debug(f"File {file_path} has unsupported extension, skipping.")
                    continue

                file_path = os.path.join(dir_path, filename)
                hash_value = calculate_file_hash(file_path)

                # search file_path in the database
                if ret := self.db.fetch_one("SELECT hash FROM ragflow WHERE path = ?", (file_path,)):
                    # file already in the database
                    if hash_value == ret[0]:
                        # no need to update
                        logger.debug(f"File {file_path} already up-to-date.")
                        continue
                    else:
                        # file was changed, update file status to 1
                        logger.debug(f"File {file_path} changed.")
                        self.db.update("ragflow", f"hash = ?, status = ?", "path = ?", (hash_value, 1, file_path))
                else:
                    # file not in the database, insert it
                    relative_path = os.path.relpath(dir_path, self.root_dir)
                    relative_filename = os.path.join(relative_path, filename)
                    self.db.insert("ragflow", "path, filename, extension, hash, status",
                                   (file_path, relative_filename, file_extension, hash_value, 0))

        logger.debug("Scanning completed.")

    def update_files(self) -> List[str]:
        """Update files in the database.

        :return: list of removed files
        """
        removed_files = self.scan_database()
        self.scan_files()
        return removed_files

    def get_new_files(self) -> List[Tuple[str, str]]:
        """Get new files.

        :return: list of new files
        """
        return [(row[0], row[1]) for row in self.db.fetch_all("SELECT path, filename FROM ragflow WHERE status = 0")]
        
    def get_updated_files(self) -> List[Tuple[str, str, str]]:
        """Get updated files.

        :return: list of updated files
        """
        return [(row[0], row[1], row[2]) for row in self.db.fetch_all("SELECT doc_id, path, filename FROM ragflow WHERE status = 1")]

    def get_unprocessed_files(self) -> List[str]:
        """Get unprocessed files.

        :return: list of unprocessed files
        """
        return [row[0] for row in self.db.fetch_all("SELECT path FROM ragflow WHERE status = 2")]

    def set_file_id(self, file_path: str, file_id: str) -> None:
        """Set file id.

        :param file_path: file path
        :param file_id: file id
        :return: None
        """
        self.db.update("ragflow", "doc_id =?", "path =?", (file_id, file_path))

    def set_file_status(self, file_path: str, status: int) -> None:
        """Set file status.

        :param file_path: file path
        :param status: file status. 
         0 = unuploaded and new, 1 = unuploaded but update, 2 = uploaded but not processed, 3 = uploaded and processing, 4 = uploaded and processed
        :return: None
        """
        self.db.update("ragflow", "status =?", "path =?", (status, file_path))

    def set_files_status(self, file_paths: List[str], status: int) -> None:
        """Set files status.

        :param file_path: file paths
        :param status: file status. 
         0 = unuploaded and new, 1 = unuploaded but update, 2 = uploaded but not processed, 3 = uploaded and processing, 4 = uploaded and processed
        :return: None
        """
        for file_path in file_paths:
            self.db.update("ragflow", "status =?", "path =?", (status, file_path))

    def connect(self) -> None:
        """Connect to the database.

        :return: None
        """
        self.db.connect()

    def disconnect(self) -> None:
        """Close the database.

        :return: None
        """
        self.db.disconnect()
