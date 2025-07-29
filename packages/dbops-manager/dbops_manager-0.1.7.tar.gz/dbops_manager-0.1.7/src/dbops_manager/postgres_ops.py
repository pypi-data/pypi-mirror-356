"""Core PostgreSQL operations module."""

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union
import psycopg2
from psycopg2.extras import RealDictCursor, execute_values
from .exceptions import ConnectionError, QueryError
from .config_loader import load_from_env, validate_config
import logging
import concurrent.futures
import io
import csv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PostgresOps:
    """A lightweight PostgreSQL operations manager."""
    
    def __init__(self, config: Dict[str, str], logging_enabled: bool = True):
        """
        Initialize PostgreSQL operations manager.
        
        Args:
            config: PostgreSQL configuration dictionary
            logging_enabled: Enable logging for database operations
        """
        self.logging_enabled = logging_enabled
        validate_config(config, logging_enabled)
        self.config = config
        self._conn = None
        self._init_connection()
    
    def _init_connection(self):
        """Initialize the database connection."""
        try:
            self._conn = psycopg2.connect(**self.config)
            self._conn.autocommit = True
            if self.logging_enabled:
                self._create_logs_table()
        except Exception as e:
            error_msg = f"Failed to initialize connection: {str(e)}"
            logger.error(error_msg)
            raise ConnectionError(error_msg)
    
    def _create_logs_table(self):
        """Create the logs table if it doesn't exist."""
        try:
            self.execute("""
                CREATE TABLE IF NOT EXISTS dbops_manager_logs (
                    id SERIAL PRIMARY KEY,
                    operation VARCHAR(50),
                    query TEXT,
                    params TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        except Exception as e:
            logger.error(f"Failed to create logs table: {str(e)}")
    
    def _log_operation(self, operation, query, params):
        """Log database operation to the logs table."""
        if not self.logging_enabled:
            return
        
        try:
            self.execute(
                "INSERT INTO dbops_manager_logs (operation, query, params) VALUES (%s, %s, %s)",
                (operation, query, str(params))
            )
        except Exception as e:
            logger.error(f"Failed to log operation: {str(e)}")
    
    @classmethod
    def from_env(cls, env_prefix: str = "DB_", logging_enabled: bool = True) -> 'PostgresOps':
        """Create instance from environment variables."""
        config = load_from_env(env_prefix, logging_enabled)
        return cls(config, logging_enabled)
    
    @classmethod
    def from_config(cls, config: Dict[str, str], logging_enabled: bool = True) -> 'PostgresOps':
        """Create instance from configuration dictionary."""
        return cls(config, logging_enabled)
    
    def fetch(
        self,
        query: str,
        params: Optional[List[Any]] = None,
        as_dict: bool = True
    ) -> List[Union[Dict[str, Any], Tuple]]:
        """
        Execute a SELECT query and fetch all results.
        
        Args:
            query: SQL query string
            params: Query parameters for parameterized queries
            as_dict: Return results as dictionaries (default: True)
        
        Returns:
            List of query results
        
        Raises:
            QueryError: If query execution fails
        """
        if self.logging_enabled:
            self._log_operation("fetch", query, params)
        
        start_time = datetime.now()
        cursor_factory = RealDictCursor if as_dict else None
        
        try:
            with self._conn.cursor(cursor_factory=cursor_factory) as cur:
                cur.execute(query, params)
                results = cur.fetchall()
                
                execution_time = (datetime.now() - start_time).total_seconds()
                self._log_operation(
                    "fetch",
                    query,
                    params
                )
                
                return results
        except Exception as e:
            error_msg = f"Fetch operation failed: {str(e)}"
            logger.error(error_msg)
            execution_time = (datetime.now() - start_time).total_seconds()
            self._log_operation(
                "fetch",
                query,
                params
            )
            
            if self.logging_enabled:
                pass
            self._conn.rollback()
            raise QueryError(error_msg)
    
    def execute(
        self,
        query: str,
        params: Optional[List[Any]] = None
    ) -> int:
        """
        Execute a modification query (INSERT, UPDATE, DELETE).
        
        Args:
            query: SQL query string
            params: Query parameters for parameterized queries
        
        Returns:
            Number of affected rows
        
        Raises:
            QueryError: If query execution fails
        """
        if self.logging_enabled:
            self._log_operation("execute", query, params)
        
        start_time = datetime.now()
        
        try:
            with self._conn.cursor() as cur:
                cur.execute(query, params)
                self._conn.commit()
                affected_rows = cur.rowcount
                
                execution_time = (datetime.now() - start_time).total_seconds()
                operation_type = self._get_operation_type(query)
                self._log_operation(
                    operation_type,
                    query,
                    params
                )
                
                return affected_rows
        except Exception as e:
            error_msg = f"Query execution failed: {str(e)}"
            logger.error(error_msg)
            execution_time = (datetime.now() - start_time).total_seconds()
            operation_type = self._get_operation_type(query)
            self._log_operation(
                operation_type,
                query,
                params
            )
            
            if self.logging_enabled:
                pass
            self._conn.rollback()
            raise QueryError(error_msg)
    
    def _get_operation_type(self, query: str) -> str:
        """Determine the type of operation from the query."""
        query = query.strip().upper()
        if query.startswith("INSERT"):
            return "INSERT"
        elif query.startswith("UPDATE"):
            return "UPDATE"
        elif query.startswith("DELETE"):
            return "DELETE"
        elif query.startswith("CREATE"):
            return "CREATE"
        elif query.startswith("DROP"):
            return "DROP"
        elif query.startswith("ALTER"):
            return "ALTER"
        elif query.startswith("TRUNCATE"):
            return "TRUNCATE"
        else:
            return "OTHER"
    
    def close(self) -> None:
        """Close the database connection."""
        if self._conn and not self._conn.closed:
            self._conn.close()

    def chunked_iterable(self, iterable, size):
        """Generator that yields chunks of the iterable without loading all into memory."""
        for i in range(0, len(iterable), size):
            yield iterable[i:i + size]

    def bulk_insert(self, table: str, data: List[Dict[str, Any]], batch_size: int = 200, num_threads: int = 2):
        if not data:
            return

        batches = list(self.chunked_iterable(data, batch_size))

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(self._insert_batch, table, batch) for batch in batches]
            for future in concurrent.futures.as_completed(futures):
                future.result()  # raises any exception from the thread

    def _insert_batch(self, table: str, batch: List[Dict[str, Any]]):
        if not batch:
            return

        conn = None
        cursor = None
        try:
            conn = self._conn
            cursor = conn.cursor()
            columns = list(batch[0].keys())
            values = [[row[col] for col in columns] for row in batch]
            insert_query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES %s"

            execute_values(cursor, insert_query, values)

            if self.logging_enabled:
                self._log_operation("bulk_insert", insert_query, values[:3])  # log sample

            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Bulk insert failed: {e}")
            raise QueryError(f"Bulk insert failed: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                self._conn.close()

    def close_pool(self):
        if self._conn:
            self._conn.close() 