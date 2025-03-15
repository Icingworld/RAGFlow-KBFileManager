"""
Module File: wwsqlite.py
Description: This module contains the sqlite database for the project. This database is used to
store the file system information and the hash value of root directory.

Author: Icingworld
Date: 2025-03-14
Version: 0.1.0
"""

import sqlite3
from typing import Any, List, Tuple, Optional
from .wwlog import logger


class SQLiteDB:
    def __init__(self, db_path: str = "default.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def execute(self, query: str, params: Tuple = ()) -> None:
        """execute sql query.
        
        :param query: sql query
        :param params: sql query params
        :return: None
        """
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_one(self, query: str, params: Tuple = ()) -> Optional[Tuple]:
        """Fetch single record from database.

        :param query: SQL query
        :param params: SQL query parameters
        :return: Single record as a tuple, or None if no record found
        """
        self.cursor.execute(query, params)
        return self.cursor.fetchone()
    
    def fetch_all(self, query: str, params: Tuple = ()) -> List[Tuple]:
        """Fetch all records from database.

        :param query: SQL query
        :param params: SQL query parameters
        :return: List of tuples containing all records
        """
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def create_table(self, table_name: str, columns: str) -> None:
        """Create a table.
        
        :param table_name: table name
        :param columns: table columns
        """
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.execute(query)
    
    def insert(self, table: str, columns: str, values: Tuple) -> None:
        """Insert data into database.
        
        :param table: table name
        :param columns: table columns
        :param values: table values
        :return: None
        """
        placeholders = ', '.join(['?'] * len(values))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.execute(query, values)
    
    def update(self, table: str, set_clause: str, condition: str, params: Tuple) -> None:
        """Update data in database.

        :param table: table name
        :param set_clause: update clause
        :param condition: update condition
        :param params: update condition params
        :return: None
        """
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        self.execute(query, params)
    
    def delete(self, table: str, condition: str, params: Tuple) -> None:
        """Delete data from database.

        :param table: table name
        :param condition: delete condition
        :param params: delete condition params
        :return: None
        """
        query = f"DELETE FROM {table} WHERE {condition}"
        self.execute(query, params)

    def connect(self) -> None:
        """Connect to database if not connected.

        :return: None
        """
        if not self.conn:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
    
    def disconnect(self) -> None:
        """Close database connection if connected.
        
        :return: None
        """
        if self.conn:
            self.cursor.close()
            self.conn.close()
            self.cursor = None
            self.conn = None
    
    def __enter__(self) -> "SQLiteDB":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.disconnect()
