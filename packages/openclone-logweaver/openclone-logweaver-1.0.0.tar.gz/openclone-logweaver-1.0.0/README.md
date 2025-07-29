# LogWeaver - Asynchronous Database Logging for Python

LogWeaver is a Python logging package that provides asynchronous, database-backed logging with queuing and threading. Designed for high-performance applications that need reliable logging without blocking main execution threads.

## Features

- **Asynchronous Logging**: Queue-based system with background thread processing
- **Database Storage**: PostgreSQL backend with automatic connection management
- **Run Number Tracking**: Session-based logging with unique run identifiers
- **Rich Metadata**: Timestamps, IP addresses, machine names, and custom tags
- **Non-blocking**: Main application threads never wait for database operations
- **Configurable**: Adjustable log levels, write frequency, and custom tags

## Installation

```bash
pip install logweaver
```

## Quick Start

```python
import LogWeaver

# Initialize database connection
LogWeaver.InitializeLogWeaver("localhost", 5432, "mydb", "user", "password")

# Create logger instance
logger = LogWeaver.LogWeaver("MyApp", "192.168.1.100")

# Log messages
logger.log("Application started", LogWeaver.LogWeaver.INFO)
logger.log("Error occurred", LogWeaver.LogWeaver.ERROR, ["error", "startup"])
```

## Usage

### Basic Logging
```python
# Different log levels
logger.log("Info message", LogWeaver.LogWeaver.INFO)
logger.log("Warning message", LogWeaver.LogWeaver.WARNING)
logger.log("Error message", LogWeaver.LogWeaver.ERROR)
logger.log("Debug message", LogWeaver.LogWeaver.DEBUG)
logger.log("Critical message", LogWeaver.LogWeaver.CRITICAL)
```

### Tagged Logging
```python
# Add custom tags for categorization
logger.log("Database connection established", 
          LogWeaver.LogWeaver.INFO, 
          ["database", "startup", "connection"])
```

### Configuration
```python
# Set log write frequency (default: 1 second)
LogWeaver.set_db_log_frequency(5)  # Write every 5 seconds
```

## Database Schema

LogWeaver requires a PostgreSQL table with the following structure:

```sql
CREATE TABLE log (
    id SERIAL PRIMARY KEY,
    run_number INTEGER,
    application_name VARCHAR(255),
    open_clone_log BOOLEAN,
    timestamp TIMESTAMP,
    message TEXT,
    tags TEXT,
    level VARCHAR(50),
    machine_name VARCHAR(255),
    ip_address VARCHAR(45)
);
```

## Architecture

- **Queue-based**: Logs are queued in memory and written periodically
- **Threading**: Background daemon thread handles database operations
- **Timezone**: Timestamps in US/Eastern timezone
- **Cleanup**: Automatic cleanup on application exit

## Requirements

- Python 3.8+
- PostgreSQL database
- psycopg2-binary
- pytz

## License

MIT License