# DBops Manager

A Python package for managing database operations with a focus on logging and CRUD operations.

## Installation

You can install the package using pip:

```bash
pip install dbops-manager==0.1.6
```

## Features

- **Connection Management**: Easily manage database connections with support for environment variables.
- **CRUD Operations**: Perform Create, Read, Update, and Delete operations on your database.
- **Logging**: Log operations to the database for better tracking and debugging.

## Usage

### Basic Usage

```python
from dbops_manager.postgres_ops import PostgresOps

# Initialize the PostgreSQL operations
db_ops = PostgresOps()

# Create a table
db_ops.create_table('test_table', 'id SERIAL PRIMARY KEY, name VARCHAR(100), age INTEGER')

# Insert a row
db_ops.insert('test_table', {'name': 'Alice', 'age': 30})

# Fetch rows
rows = db_ops.fetch('test_table')
print(rows)

# Update a row
db_ops.update('test_table', {'name': 'Bob'}, 'id = 1')

# Delete a row
db_ops.delete('test_table', 'id = 1')
```

### Logging

The package logs operations to the `dbops_manager_logs` table. Ensure that the `logging_enabled` parameter is set to `True` when initializing `PostgresOps`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 