"""Core PostgreSQL operations module."""

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union
import psycopg2
from psycopg2.extras import RealDictCursor, execute_values
from .exceptions import ConnectionError, QueryError, TransactionError
from .config_loader import load_from_env, validate_config
import logging
import os
from dotenv import load_dotenv
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PostgresOps:
    """A lightweight PostgreSQL operations manager."""
    
    def __init__(self, config: Dict[str, str], logging_enabled: bool = True):
        """
        Initialize PostgresOps with database configuration.
        
        Args:
            config: Dictionary containing database connection parameters
            logging_enabled: Whether to enable operation logging
        """
        self.config = config
        self.conn = None
        self.cursor = None
        self.logging_enabled = logging_enabled
        self._in_transaction = False
        self._connect()
        if logging_enabled:
            self._setup_logging()
    
    @classmethod
    def from_env(cls, logging_enabled: bool = True) -> 'PostgresOps':
        """
        Create PostgresOps instance from environment variables.
        
        Args:
            logging_enabled: Whether to enable operation logging
            
        Returns:
            PostgresOps instance
        """
        load_dotenv()
        config = {
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT")
        }
        return cls(config, logging_enabled)

    @classmethod
    def from_config(cls, config: Dict[str, str], logging_enabled: bool = True) -> 'PostgresOps':
        """
        Create PostgresOps instance from provided configuration.
        
        Args:
            config: Dictionary containing database connection parameters
            logging_enabled: Whether to enable operation logging
            
        Returns:
            PostgresOps instance
        """
        return cls(config, logging_enabled)

    def _connect(self):
        """Establish database connection."""
        try:
            self.conn = psycopg2.connect(**self.config)
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        except Exception as e:
            raise Exception(f"Failed to connect to database: {str(e)}")

    def _setup_logging(self):
        """Create logging table if it doesn't exist."""
        create_log_table_query = """
        CREATE TABLE IF NOT EXISTS dbops_manager_logs (
            id SERIAL PRIMARY KEY,
            operation VARCHAR(50),
            query TEXT,
            params TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        try:
            self.execute(create_log_table_query, log=False)
        except Exception as e:
            print(f"Warning: Could not create logging table: {str(e)}")
            self.logging_enabled = False

    def _log_operation(self, operation: str, query: str, params: Optional[Union[tuple, dict]] = None):
        """Log database operation."""
        if not self.logging_enabled:
            return
        if "dbops_manager_logs" in query:
            return
        try:
            params_str = str(params) if params else None
            log_query = """
            INSERT INTO dbops_manager_logs (operation, query, params)
            VALUES (%s, %s, %s)
            """
            self.execute(log_query, (operation, query, params_str), log=False)
        except Exception as e:
            print(f"Warning: Could not log operation: {str(e)}")
            # Don't disable logging for a single failed log entry

    @contextmanager
    def transaction(self):
        """Context manager for database transactions."""
        self._in_transaction = True
        try:
            yield
            self.conn.commit()
            if self.logging_enabled:
                self._log_operation("TRANSACTION", "Transaction committed", None)
        except Exception as e:
            self.conn.rollback()
            if self.logging_enabled:
                self._log_operation("TRANSACTION", "Transaction rolled back", str(e))
            raise TransactionError(f"Transaction failed: {str(e)}")
        finally:
            self._in_transaction = False

    def execute(self, query: str, params: Optional[Union[tuple, dict]] = None, log: bool = True) -> None:
        """
        Execute a query without returning results.
        
        Args:
            query: SQL query to execute
            params: Query parameters
        """
        try:
            self.cursor.execute(query, params)
            if not self._in_transaction:
                self.conn.commit()
            if self.logging_enabled and log:
                self._log_operation("EXECUTE", query, params)
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Query execution failed: {str(e)}")

    def fetch(self, query: str, params: Optional[Union[tuple, dict]] = None) -> List[Dict[str, Any]]:
        """
        Execute a query and return results.
        
        Args:
            query: SQL query to execute
            params: Query parameters
            
        Returns:
            List of dictionaries containing query results
        """
        try:
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            self._log_operation("FETCH", query, params)
            return results
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Query execution failed: {str(e)}")

    def close(self):
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute_batch(self, queries: List[Tuple[str, Optional[Union[tuple, dict]]]], 
                     use_transaction: bool = True) -> None:
        """
        Execute multiple queries in a batch.
        
        Args:
            queries: List of (query, params) tuples
            use_transaction: Whether to wrap queries in a transaction
        """
        if use_transaction:
            with self.transaction():
                self._execute_batch_internal(queries)
        else:
            self._execute_batch_internal(queries)

    def _execute_batch_internal(self, queries: List[Tuple[str, Optional[Union[tuple, dict]]]]) -> None:
        """Internal method for batch execution."""
        for query, params in queries:
            try:
                self.cursor.execute(query, params)
                if self.logging_enabled:
                    self._log_operation("BATCH_EXECUTE", query, params)
            except Exception as e:
                raise QueryError(f"Batch query execution failed: {str(e)}")

    def execute_values(self, query: str, values: List[tuple], 
                      template: Optional[str] = None, 
                      page_size: int = 100) -> None:
        """
        Execute a query with multiple values using execute_values.
        
        Args:
            query: SQL query to execute
            values: List of tuples containing values to insert
            template: Optional template for the values
            page_size: Number of values to insert at once
        """
        try:
            execute_values(self.cursor, query, values, template=template, page_size=page_size)
            self.conn.commit()
            if self.logging_enabled:
                self._log_operation("EXECUTE_VALUES", query, f"Values count: {len(values)}")
        except Exception as e:
            self.conn.rollback()
            raise QueryError(f"Execute values failed: {str(e)}")

    def fetch_many(self, query: str, params: Optional[Union[tuple, dict]] = None, 
                  size: int = 1000) -> List[Dict[str, Any]]:
        """
        Fetch results in chunks to handle large result sets.
        
        Args:
            query: SQL query to execute
            params: Query parameters
            size: Number of rows to fetch at once
            
        Returns:
            List of dictionaries containing query results
        """
        try:
            self.cursor.execute(query, params)
            results = []
            while True:
                rows = self.cursor.fetchmany(size)
                if not rows:
                    break
                results.extend(rows)
            if self.logging_enabled:
                self._log_operation("FETCH_MANY", query, f"Fetched {len(results)} rows")
            return results
        except Exception as e:
            self.conn.rollback()
            raise QueryError(f"Fetch many failed: {str(e)}")