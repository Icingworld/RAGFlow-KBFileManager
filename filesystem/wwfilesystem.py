"""
Module File: wwfilesystem.py
Description: This module maintains a filesystem for the root directory.

Author: Icingworld
Date: 2025-03-14
Version: 0.1.0
"""

import os
import time
from typing import List
from utils.wwhash import calculate_file_hash
from utils.wwsqlite import SQLiteDB
from utils.wwlog import logger


class FileSystem:
    def __init__(self, root_dir: str, suffix: List[str]):
        self.root_dir = root_dir
        self.suffix = suffix
        self.db = SQLiteDB()

        self.removed_files = []
        
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
            modified_time INTEGER NOT NULL,
            status INTEGER NOT NULL DEFAULT 0,
            
            UNIQUE(path)
        """)
        logger.debug("Database successfully initialized.")

    def scan_database(self) -> None:
        """Scan the database and delete files that no longer exist.

        :return: None
        """
        logger.debug("Scanning database...")
        paths = [row[0] for row in self.db.fetch_all("SELECT path FROM ragflow")]
        for file_path in paths:
            if not os.path.exists(file_path):
                logger.debug(f"File {file_path} not found, deleting from database.")
                self.db.delete("ragflow", "path =?", (file_path,))
                self.removed_files.append(file_path)
        logger.debug("Scanning completed.")

    def scan_files(self) -> None:
        """Scan files in the root directory and save their information to the database.

        :return: None
        """
        logger.debug("Scanning root directory...")

        for dir_path, dir_names, filenames in os.walk(self.root_dir):
            # skip hidden directories
            dir_names[:] = [d for d in dir_names if not d.startswith(".")]

            for filename in filenames:
                file_path = os.path.join(dir_path, filename)
                hash_value = calculate_file_hash(file_path)
                file_extension = os.path.splitext(filename)[1]

                if file_extension not in self.suffix:
                    continue

                # search file_path in the database
                if ret := self.db.fetch_one("SELECT * FROM ragflow WHERE path = ?", (file_path,)):
                    # file already in the database
                    if hash_value == ret[4]:
                        # no need to update
                        logger.debug(f"File {file_path} already up-to-date.")
                        continue
                    else:
                        # file was changed, update file status to 0(default)
                        logger.debug(f"File {file_path} changed.")
                        self.db.update("ragflow", f"hash = ?, modified_time = ?, status = ?", "path = ?", (hash_value, int(time.time()), 1, file_path))
                else:
                    # file not in the database, insert it
                    base_name = os.path.basename(file_path)
                    self.db.insert("ragflow", "path, filename, extension, hash, modified_time",
                                   (file_path, base_name, file_extension, hash_value, int(time.time())))

        logger.debug("Scanning completed.")

    def update_files(self) -> None:
        """Update files in the database.

        :return: None
        """
        self.scan_database()
        self.scan_files()

    def get_removed_files(self) -> list[str]:
        """Get removed files.

        :return: list of removed files
        """
        return self.removed_files

    def clear_removed_files(self) -> None:
        """Clear removed files.

        :return: None
        """
        self.removed_files.clear()

    def get_new_files(self) -> list[str]:
        """Get new files.

        :return: list of new files
        """
        return [row[0] for row in self.db.fetch_all("SELECT path FROM ragflow WHERE status = 0")]
        
    def get_updated_files(self) -> list[str]:
        """Get updated files.

        :return: list of updated files
        """
        return [row[0] for row in self.db.fetch_all("SELECT path FROM ragflow WHERE status = 1")]

    def get_unprocessed_files(self) -> list[str]:
        """Get unprocessed files.

        :return: list of unprocessed files
        """
        return [row[0] for row in self.db.fetch_all("SELECT path FROM ragflow WHERE status = 2")]

    def set_file_status(self, file_path: str, status: int) -> None:
        """Set file status.

        :param file_path: file path
        :param status: file status. 
         0 = unuploaded and new, 1 = unuploaded but update, 2 = uploaded but not processed, 3 = uploaded and processing, 4 = uploaded and processed
        :return: None
        """
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
