# DB Operations Manager

A Python package for managing database operations with a focus on logging and simple CRUD operations.

## Features

- **Simple CRUD Operations**: Insert, update, delete, and fetch data from your database.
- **Logging**: Automatically log database operations to a `dbops_manager_logs` table.
- **Concurrency Support**: Use multiple workers to perform concurrent database operations.

## Installation

```bash
pip install dbops-manager
```

## Usage

### Basic Usage

```python
from dbops_manager import PostgresOps

# Initialize the database connection
db = PostgresOps({
    'dbname': 'your_db',
    'user': 'your_user',
    'password': 'your_password',
    'host': 'localhost',
    'port': '5432'
}, logging_enabled=True)

# Insert a row
db.execute(
    "INSERT INTO your_table (name, age) VALUES (%s, %s)",
    ["Alice", 30]
)

# Fetch data
data = db.fetch("SELECT * FROM your_table")
print(data)

# Close the connection
db.close()
```

### Concurrent Operations

```python
import concurrent.futures

def insert_row(db, worker_id):
    db.execute(
        "INSERT INTO your_table (name, age) VALUES (%s, %s)",
        [f"Worker-{worker_id}", 20 + worker_id]
    )

# Use ThreadPoolExecutor to insert rows concurrently
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(insert_row, db, i) for i in range(10)]
    concurrent.futures.wait(futures)
```

## Logging

The package automatically logs database operations to a `dbops_manager_logs` table. You can query this table to see the history of operations.

```python
logs = db.fetch("SELECT * FROM dbops_manager_logs ORDER BY created_at DESC LIMIT 10")
print(logs)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 