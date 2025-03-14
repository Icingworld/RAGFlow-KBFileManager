"""
Module File: wwhash.py
Description: This module contains the hash functions for the project, especially for files.

Author: Icingworld
Date: 2025-03-14
Version: 0.1.0
"""

import hashlib
from .wwtime import timeit


@timeit("calculate_file_hash_content_binary used", "ms")
def calculate_file_hash_content_binary(content: bytes, algorithm: str = "sha256", chunk_size: int = 4096) -> str:
    """Calculate the hash value of binary content.

    :param content: binary file content
    :param algorithm: hash algorithm, supporting "sha256", "md5", etc.  default is sha256
    :param chunk_size: chunk size for reading file, default is 4096
    :return: hash value of the file
    """
    hash_func = hashlib.new(algorithm)
    
    # read the file in chunks and update the hash
    for offset in range(0, len(content), chunk_size):
        chunk = content[offset:offset+chunk_size]
        hash_func.update(chunk)
    
    return hash_func.hexdigest()

@timeit("calculate_file_hash used", "ms")
def calculate_file_hash(file_path: str, algorithm: str = "sha256", chunk_size: int = 4096) -> str:
    """Calculate the hash value of a file.

    :param file_path: path of the file
    :param algorithm: hash algorithm, supporting "sha256", "md5", etc.  default is sha256
    :param chunk_size: chunk size for reading file, default is 4096
    :return: hash value of the file
    """
    hash_func = hashlib.new(algorithm)

    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):  # read the file in chunks
            hash_func.update(chunk)

    return hash_func.hexdigest()
