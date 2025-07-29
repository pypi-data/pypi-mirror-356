# dbops-manager

A lightweight PostgreSQL operations manager for AWS Lambda.

## Features

- **CRUD Operations**: Execute, fetch, and manage PostgreSQL queries with ease.
- **Batch Operations**: Execute multiple queries in a single batch.
- **Transaction Support**: Use context managers for transaction handling with automatic rollback on errors.
- **Bulk Insert**: Efficiently insert multiple records using `execute_values`.
- **Logging**: Automatically log database operations to a dedicated table.
- **Error Handling**: Comprehensive exception handling for database operations.

## Installation

```bash
pip install dbops-manager
```

## Usage

### Basic Usage

```python
from dbops_manager import PostgresOps

# Initialize with configuration
config = {
    "dbname": "example",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}
db = PostgresOps.from_config(config)

# Execute a query
db.execute("INSERT INTO users (name) VALUES (%s)", ("John",))

# Fetch results
results = db.fetch("SELECT * FROM users")
print(results)

# Close the connection
db.close()
```

### Using Environment Variables

```python
from dbops_manager import PostgresOps

# Initialize using environment variables
db = PostgresOps.from_env()

# Execute a query
db.execute("INSERT INTO users (name) VALUES (%s)", ("Jane",))

# Fetch results
results = db.fetch("SELECT * FROM users")
print(results)

# Close the connection
db.close()
```

### Batch Operations

```python
from dbops_manager import PostgresOps

db = PostgresOps.from_config(config)

# Execute multiple queries in a batch
queries = [
    ("INSERT INTO users (name) VALUES (%s)", ("Alice",)),
    ("INSERT INTO users (name) VALUES (%s)", ("Bob",))
]
db.execute_batch(queries)

# Close the connection
db.close()
```

### Transaction Support

```python
from dbops_manager import PostgresOps

db = PostgresOps.from_config(config)

# Use a transaction
with db.transaction():
    db.execute("INSERT INTO users (name) VALUES (%s)", ("Charlie",))
    db.execute("UPDATE users SET status = %s WHERE name = %s", ("active", "Charlie"))

# Close the connection
db.close()
```

### Bulk Insert

```python
from dbops_manager import PostgresOps

db = PostgresOps.from_config(config)

# Bulk insert
values = [("David",), ("Eve",)]
db.execute_values("INSERT INTO users (name) VALUES %s", values)

# Close the connection
db.close()
```

### Logging

Logs are automatically stored in the `dbops_manager_logs` table. You can view them using:

```sql
SELECT * FROM dbops_manager_logs ORDER BY created_at DESC;
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 