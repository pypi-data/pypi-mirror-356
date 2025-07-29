"""Core PostgreSQL operations module."""

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union
import psycopg2
from psycopg2.extras import RealDictCursor
from .exceptions import ConnectionError, QueryError
from .config_loader import load_from_env, validate_config

class PostgresOps:
    """A lightweight PostgreSQL operations manager."""
    
    def __init__(self, config: Dict[str, str], logging_enabled: bool = False):
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
        if self.logging_enabled:
            self._create_logs_table()
    
    def _init_connection(self):
        """Initialize the database connection."""
        try:
            self._conn = psycopg2.connect(**self.config)
            # Set autocommit to False for transaction control
            self._conn.autocommit = False
        except psycopg2.Error as e:
            error_msg = f"Failed to initialize connection: {str(e)}"
            if self.logging_enabled:
                pass
            raise ConnectionError(error_msg)
    
    def _create_logs_table(self):
        """Create the logs table if it doesn't exist."""
        create_logs_table_sql = """
        CREATE TABLE IF NOT EXISTS dbops_manager_logs (
            id SERIAL PRIMARY KEY,
            operation_type VARCHAR(50) NOT NULL,
            query TEXT NOT NULL,
            params TEXT,
            execution_time DOUBLE PRECISION NOT NULL,
            rows_affected INTEGER,
            status VARCHAR(20) NOT NULL,
            error_message TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
        """
        try:
            self.execute(create_logs_table_sql)
        except Exception:
            pass
    
    def _log_operation(self, operation_type: str, query: str, params: Optional[List[Any]], 
                      execution_time: float, rows_affected: int, status: str, 
                      error_message: Optional[str] = None):
        """Log database operation to the logs table."""
        if not self.logging_enabled:
            return
        
        log_sql = """
        INSERT INTO dbops_manager_logs 
        (operation_type, query, params, execution_time, rows_affected, status, error_message)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        try:
            self.execute(log_sql, [
                operation_type,
                query,
                str(params) if params else None,
                execution_time,
                rows_affected,
                status,
                error_message
            ])
        except Exception:
            pass
    
    @classmethod
    def from_env(cls, env_prefix: str = "DB_", logging_enabled: bool = False) -> 'PostgresOps':
        """Create instance from environment variables."""
        config = load_from_env(env_prefix, logging_enabled)
        return cls(config, logging_enabled)
    
    @classmethod
    def from_config(cls, config: Dict[str, str], logging_enabled: bool = False) -> 'PostgresOps':
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
            pass
        
        start_time = datetime.now()
        cursor_factory = RealDictCursor if as_dict else None
        
        try:
            with self._conn.cursor(cursor_factory=cursor_factory) as cur:
                cur.execute(query, params)
                results = cur.fetchall()
                
                execution_time = (datetime.now() - start_time).total_seconds()
                self._log_operation(
                    "SELECT",
                    query,
                    params,
                    execution_time,
                    len(results),
                    "SUCCESS"
                )
                
                return results
        except psycopg2.Error as e:
            error_msg = f"Query execution failed: {str(e)}"
            execution_time = (datetime.now() - start_time).total_seconds()
            self._log_operation(
                "SELECT",
                query,
                params,
                execution_time,
                0,
                "ERROR",
                str(e)
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
            pass
        
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
                    params,
                    execution_time,
                    affected_rows,
                    "SUCCESS"
                )
                
                return affected_rows
        except psycopg2.Error as e:
            error_msg = f"Query execution failed: {str(e)}"
            execution_time = (datetime.now() - start_time).total_seconds()
            operation_type = self._get_operation_type(query)
            self._log_operation(
                operation_type,
                query,
                params,
                execution_time,
                0,
                "ERROR",
                str(e)
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