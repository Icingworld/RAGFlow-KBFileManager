"""
Module File: wwlog.py
Description: This module contains the logging function for the project.

Author: Icingworld
Date: 2025-03-14
Version: 0.1.0
"""

import logging


class Logger:
    def __init__(self):
        # setup logging
        self.logger = logging.getLogger("RAGFlow-KBFileManager")
        self.logger.setLevel(logging.DEBUG)  # set logging level to debug

        # create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        console_handler.setFormatter(formatter)

        # add console handler to logger
        self.logger.addHandler(console_handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)


logger = Logger()
