"""
Module File: wwfilesystem.py
Description: This module maintains a filesystem for the root directory.

Author: Icingworld
Date: 2025-03-14
Version: 0.1.0
"""

import os
import time
from utils.wwhash import calculate_file_hash
from utils.wwsqlite import SQLiteDB
from utils.wwlog import logger


class FileSystem:
    def __init__(self, root_dir: str, suffix: list[str]):
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
                # there are something to do
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
                        self.db.update("ragflow", f"hash = ?, modified_time = ?", "path = ?", (hash_value, int(time.time()), file_path))
                else:
                    # file not in the database, insert it
                    base_name = os.path.basename(file_path)
                    self.db.insert("ragflow", "path, filename, extension, hash, modified_time",
                                   (file_path, base_name, file_extension, hash_value, int(time.time())))

        logger.debug("Scanning completed.")
