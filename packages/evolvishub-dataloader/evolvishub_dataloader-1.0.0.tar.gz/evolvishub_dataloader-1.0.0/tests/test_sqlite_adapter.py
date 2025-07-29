"""Tests for the SQLite adapter module."""

import pytest
import sqlite3
import tempfile
import asyncio
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.data_loader.sqlite_adapter import SQLiteAdapter


@pytest.fixture
def temp_db():
    """Create a temporary database file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    yield db_path
    # Cleanup
    Path(db_path).unlink(missing_ok=True)


@pytest.fixture
def adapter(temp_db):
    """Create a SQLiteAdapter instance for testing."""
    return SQLiteAdapter(temp_db)


@pytest.fixture
def connected_adapter(adapter):
    """Create a connected SQLiteAdapter instance for testing."""
    adapter.connect()
    yield adapter
    adapter.disconnect()


def test_init(temp_db):
    """Test SQLiteAdapter initialization."""
    adapter = SQLiteAdapter(temp_db)
    
    assert adapter.db_path == temp_db
    assert adapter.conn is None
    assert adapter.cursor is None


def test_connect(adapter):
    """Test database connection."""
    adapter.connect()
    
    assert adapter.conn is not None
    assert adapter.cursor is not None
    assert isinstance(adapter.conn, sqlite3.Connection)
    
    adapter.disconnect()


def test_connect_invalid_path():
    """Test connection with invalid database path."""
    # Use a path that doesn't exist and can't be created
    invalid_path = "/invalid/path/database.db"
    adapter = SQLiteAdapter(invalid_path)
    
    with pytest.raises(sqlite3.Error):
        adapter.connect()


def test_disconnect(connected_adapter):
    """Test database disconnection."""
    assert connected_adapter.conn is not None
    
    connected_adapter.disconnect()
    
    assert connected_adapter.conn is None
    assert connected_adapter.cursor is None


def test_disconnect_when_not_connected(adapter):
    """Test disconnection when not connected."""
    # Should not raise an error
    adapter.disconnect()
    assert adapter.conn is None


def test_execute_query_select(connected_adapter):
    """Test executing a SELECT query."""
    # Create a test table
    connected_adapter.cursor.execute("CREATE TABLE test (id INTEGER, name TEXT)")
    connected_adapter.cursor.execute("INSERT INTO test VALUES (1, 'John'), (2, 'Jane')")
    connected_adapter.conn.commit()
    
    # Test query
    result = connected_adapter.execute_query("SELECT * FROM test ORDER BY id")
    
    assert len(result) == 2
    assert result[0] == {'id': 1, 'name': 'John'}
    assert result[1] == {'id': 2, 'name': 'Jane'}


def test_execute_query_with_params(connected_adapter):
    """Test executing a query with parameters."""
    # Create a test table
    connected_adapter.cursor.execute("CREATE TABLE test (id INTEGER, name TEXT)")
    connected_adapter.cursor.execute("INSERT INTO test VALUES (1, 'John'), (2, 'Jane')")
    connected_adapter.conn.commit()
    
    # Test parameterized query
    result = connected_adapter.execute_query("SELECT * FROM test WHERE id = ?", (1,))
    
    assert len(result) == 1
    assert result[0] == {'id': 1, 'name': 'John'}


def test_execute_query_no_results(connected_adapter):
    """Test executing a query that returns no results."""
    # Create a test table
    connected_adapter.cursor.execute("CREATE TABLE test (id INTEGER, name TEXT)")
    connected_adapter.conn.commit()
    
    result = connected_adapter.execute_query("SELECT * FROM test")
    
    assert result == []


def test_execute_query_non_select(connected_adapter):
    """Test executing a non-SELECT query."""
    result = connected_adapter.execute_query("CREATE TABLE test (id INTEGER, name TEXT)")
    
    assert result == []


def test_execute_query_auto_connect(adapter):
    """Test that execute_query automatically connects if not connected."""
    # Create a test table
    result = adapter.execute_query("CREATE TABLE test (id INTEGER)")
    
    assert adapter.conn is not None
    assert result == []
    
    adapter.disconnect()


def test_execute_query_error(connected_adapter):
    """Test executing an invalid query."""
    with pytest.raises(sqlite3.Error):
        connected_adapter.execute_query("INVALID SQL QUERY")


def test_execute_many(connected_adapter):
    """Test executing multiple statements."""
    # Create a test table
    connected_adapter.cursor.execute("CREATE TABLE test (id INTEGER, name TEXT)")
    
    # Test executemany
    params_list = [(1, 'John'), (2, 'Jane'), (3, 'Bob')]
    connected_adapter.execute_many("INSERT INTO test VALUES (?, ?)", params_list)
    
    # Verify data was inserted
    result = connected_adapter.execute_query("SELECT * FROM test ORDER BY id")
    assert len(result) == 3
    assert result[0] == {'id': 1, 'name': 'John'}


def test_execute_many_auto_connect(adapter):
    """Test that execute_many automatically connects if not connected."""
    # Create a test table first
    adapter.execute_query("CREATE TABLE test (id INTEGER, name TEXT)")
    
    # Test executemany
    params_list = [(1, 'John'), (2, 'Jane')]
    adapter.execute_many("INSERT INTO test VALUES (?, ?)", params_list)
    
    assert adapter.conn is not None
    
    adapter.disconnect()


def test_execute_many_error(connected_adapter):
    """Test execute_many with invalid query."""
    with pytest.raises(sqlite3.Error):
        connected_adapter.execute_many("INVALID SQL", [(1,), (2,)])


def test_commit(connected_adapter):
    """Test manual commit."""
    # Create a test table and insert data without auto-commit
    connected_adapter.cursor.execute("CREATE TABLE test (id INTEGER)")
    connected_adapter.cursor.execute("INSERT INTO test VALUES (1)")
    
    # Commit manually
    connected_adapter.commit()
    
    # Verify data is committed
    result = connected_adapter.execute_query("SELECT * FROM test")
    assert len(result) == 1


def test_commit_when_not_connected(adapter):
    """Test commit when not connected."""
    # Should not raise an error
    adapter.commit()


@pytest.mark.asyncio
async def test_insert_data_basic(connected_adapter):
    """Test basic data insertion."""
    data = [
        {'id': 1, 'name': 'John', 'age': 25},
        {'id': 2, 'name': 'Jane', 'age': 30}
    ]
    
    result = await connected_adapter.insert_data('users', data)
    
    assert result == 2
    
    # Verify data was inserted
    rows = connected_adapter.execute_query("SELECT * FROM users ORDER BY id")
    assert len(rows) == 2
    assert rows[0]['name'] == 'John'
    assert rows[1]['name'] == 'Jane'


@pytest.mark.asyncio
async def test_insert_data_empty_list(connected_adapter):
    """Test inserting empty data list."""
    result = await connected_adapter.insert_data('users', [])
    assert result == 0


@pytest.mark.asyncio
async def test_insert_data_creates_table(connected_adapter):
    """Test that insert_data creates table if it doesn't exist."""
    data = [
        {'id': 1, 'name': 'John', 'score': 95.5, 'active': True}
    ]
    
    result = await connected_adapter.insert_data('new_table', data)
    
    assert result == 1
    
    # Verify table was created with correct schema
    rows = connected_adapter.execute_query("SELECT * FROM new_table")
    assert len(rows) == 1
    assert rows[0]['id'] == 1
    assert rows[0]['name'] == 'John'
    assert rows[0]['score'] == 95.5
    assert rows[0]['active'] == 1  # SQLite stores boolean as integer


@pytest.mark.asyncio
async def test_insert_data_different_data_types(connected_adapter):
    """Test inserting data with different data types."""
    data = [
        {
            'int_col': 42,
            'float_col': 3.14,
            'str_col': 'hello',
            'bool_col': True,
            'none_col': None
        }
    ]
    
    result = await connected_adapter.insert_data('mixed_types', data)
    
    assert result == 1
    
    # Verify data types were handled correctly
    rows = connected_adapter.execute_query("SELECT * FROM mixed_types")
    assert len(rows) == 1
    row = rows[0]
    assert row['int_col'] == 42
    assert row['float_col'] == 3.14
    assert row['str_col'] == 'hello'
    assert row['bool_col'] == 1  # Boolean stored as integer
    assert row['none_col'] is None


@pytest.mark.asyncio
async def test_insert_data_auto_connect(adapter):
    """Test that insert_data automatically connects if not connected."""
    data = [{'id': 1, 'name': 'Test'}]
    
    result = await adapter.insert_data('test_table', data)
    
    assert adapter.conn is not None
    assert result == 1
    
    adapter.disconnect()


@pytest.mark.asyncio
async def test_insert_data_table_exists(connected_adapter):
    """Test inserting data into existing table."""
    # Create table manually first
    connected_adapter.execute_query("CREATE TABLE existing_table (id INTEGER, name TEXT)")
    
    data = [{'id': 1, 'name': 'Test'}]
    result = await connected_adapter.insert_data('existing_table', data)
    
    assert result == 1


def test_create_table_if_not_exists(connected_adapter):
    """Test table creation with different data types."""
    sample_record = {
        'int_field': 42,
        'float_field': 3.14,
        'bool_field': True,
        'str_field': 'hello'
    }
    
    connected_adapter._create_table_if_not_exists_sync('test_schema', sample_record)
    
    # Verify table was created
    result = connected_adapter.execute_query(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='test_schema'"
    )
    assert len(result) == 1


def test_create_table_already_exists(connected_adapter):
    """Test that creating an existing table doesn't cause errors."""
    # Create table first
    connected_adapter.execute_query("CREATE TABLE existing (id INTEGER)")
    
    sample_record = {'id': 1}
    
    # Should not raise an error
    connected_adapter._create_table_if_not_exists_sync('existing', sample_record)


def test_context_manager_usage(temp_db):
    """Test using adapter in a context-like manner."""
    adapter = SQLiteAdapter(temp_db)
    
    try:
        adapter.connect()
        adapter.execute_query("CREATE TABLE test (id INTEGER)")
        result = adapter.execute_query("SELECT name FROM sqlite_master WHERE type='table'")
        assert len(result) > 0
    finally:
        adapter.disconnect()


@pytest.mark.asyncio
async def test_concurrent_operations(connected_adapter):
    """Test concurrent database operations."""
    # Create multiple insert operations
    tasks = []
    for i in range(5):
        data = [{'id': i, 'value': f'test_{i}'}]
        task = connected_adapter.insert_data(f'table_{i}', data)
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    
    # All operations should succeed
    assert all(result == 1 for result in results)
    
    # Verify all tables were created
    for i in range(5):
        rows = connected_adapter.execute_query(f"SELECT * FROM table_{i}")
        assert len(rows) == 1
