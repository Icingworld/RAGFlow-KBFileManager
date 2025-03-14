"""
Module File: wwhash.py
Description: This module contains the hash functions for the project, especially for files.

Author: Icingworld
Date: 2025-03-14
Version: 0.1.0
"""

import hashlib
from wwtime import timeit

@timeit("calculate_file_hash", "ms")
def calculate_file_hash(content: bytes, algorithm: str = 'sha256', chunk_size: int = 4096) -> str:
    """Calculate the hash value of a file.

    :param content: binary file content
    :param algorithm: hash algorithm, supporting "sha256", "md5", etc.  default is sha256
    :param chunk_size: chunk size for reading file, default is 4096
    :return: hash value of the file
    """
    hash_func = hashlib.new(algorithm)
    
    # Read the file in chunks and update the hash
    for offset in range(0, len(content), chunk_size):
        chunk = content[offset:offset+chunk_size]
        hash_func.update(chunk)
    
    return hash_func.hexdigest()