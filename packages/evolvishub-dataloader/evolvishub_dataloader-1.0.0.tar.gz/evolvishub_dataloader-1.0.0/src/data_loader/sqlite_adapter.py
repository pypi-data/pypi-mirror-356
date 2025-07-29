import sqlite3
import asyncio
from typing import Any, Dict, List, Optional
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SQLiteAdapter:
    """SQLite database adapter for data operations."""
    
    def __init__(self, db_path: str):
        """
        Initialize the SQLite adapter.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        logger.info(f"Initialized SQLite adapter with database at {db_path}")
    
    def connect(self) -> None:
        """Establish connection to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            logger.info("Successfully connected to SQLite database")
        except sqlite3.Error as e:
            logger.error(f"Error connecting to SQLite database: {e}")
            raise
    
    def disconnect(self) -> None:
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
            logger.info("Disconnected from SQLite database")
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        Execute a SQL query and return the results.
        
        Args:
            query (str): SQL query to execute
            params (Optional[tuple]): Query parameters
            
        Returns:
            List[Dict[str, Any]]: Query results as a list of dictionaries
        """
        try:
            if not self.conn:
                self.connect()
            
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            if self.cursor.description:
                columns = [col[0] for col in self.cursor.description]
                return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
            return []
            
        except sqlite3.Error as e:
            logger.error(f"Error executing query: {e}")
            raise
    
    def execute_many(self, query: str, params_list: List[tuple]) -> None:
        """
        Execute multiple SQL statements with different parameters.
        
        Args:
            query (str): SQL query to execute
            params_list (List[tuple]): List of parameter tuples
        """
        try:
            if not self.conn:
                self.connect()
            
            self.cursor.executemany(query, params_list)
            self.conn.commit()
            
        except sqlite3.Error as e:
            logger.error(f"Error executing multiple statements: {e}")
            raise
    
    def commit(self) -> None:
        """Commit the current transaction."""
        if self.conn:
            self.conn.commit()
            logger.debug("Transaction committed")

    async def insert_data(self, table_name: str, data: List[Dict[str, Any]]) -> int:
        """
        Insert data into a table asynchronously.

        Args:
            table_name (str): Name of the table to insert into
            data (List[Dict[str, Any]]): Data to insert

        Returns:
            int: Number of records inserted
        """
        if not data:
            return 0

        try:
            if not self.conn:
                self.connect()

            # Create table if it doesn't exist (synchronously to avoid thread issues)
            self._create_table_if_not_exists_sync(table_name, data[0])

            # Prepare insert statement
            columns = list(data[0].keys())
            placeholders = ', '.join(['?' for _ in columns])
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

            # Convert data to tuples
            values = [tuple(record[col] for col in columns) for record in data]

            # Execute insert synchronously to avoid thread issues
            self.cursor.executemany(query, values)
            self.conn.commit()

            logger.info(f"Inserted {len(data)} records into {table_name}")
            return len(data)

        except sqlite3.Error as e:
            logger.error(f"Error inserting data into {table_name}: {e}")
            raise

    def _create_table_if_not_exists_sync(self, table_name: str, sample_record: Dict[str, Any]) -> None:
        """
        Create table if it doesn't exist based on sample record (synchronous version).

        Args:
            table_name (str): Name of the table
            sample_record (Dict[str, Any]): Sample record to infer schema
        """
        try:
            # Check if table exists
            check_query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
            self.cursor.execute(check_query, (table_name,))
            exists = self.cursor.fetchone()

            if not exists:
                # Create table with inferred schema
                columns = []
                for key, value in sample_record.items():
                    if isinstance(value, int):
                        col_type = "INTEGER"
                    elif isinstance(value, float):
                        col_type = "REAL"
                    elif isinstance(value, bool):
                        col_type = "BOOLEAN"
                    else:
                        col_type = "TEXT"
                    columns.append(f"{key} {col_type}")

                create_query = f"CREATE TABLE {table_name} ({', '.join(columns)})"
                self.cursor.execute(create_query)
                self.conn.commit()
                logger.info(f"Created table {table_name}")

        except sqlite3.Error as e:
            logger.error(f"Error creating table {table_name}: {e}")
            raise