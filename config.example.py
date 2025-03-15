"""
Module File: config.py
Description: This module contains the configuration settings for the project.

Author: Icingworld
Date: 2025-03-14
Version: 0.1.0

Usage:
    Create a new config.py file in the same directory as main.py
    and fill in the configuration settings.
"""

# file config
FILE_SYSTEM_ROOT = ""  # root path of file system
FILE_SYSTEM_SUFFIX = [
    ""
]  # suffixes of file path

# manager config
MANAGER_PERIOD = 0  # period of manager in days
MANAGER_PARSE_STRATEGY = ""  # parse strategy

# RAGFlow config
RAGFLOW_URL = ""  # base url of ragflow
RAGFLOW_KNOWLEDGE_BASE_NAME = ""  # knowledge base name
RAGFLOW_PARSER = ""  # parser name, including "General", "Manual", "Paper", etc.
RAGFLOW_AUTHORIZATION = ""  # authorization string
RAGFLOW_KNOWLEDGE_BASE_ID = ""  # knowledge base id
