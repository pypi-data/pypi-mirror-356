import pytest
import pandas as pd
import json
from pathlib import Path
import asyncio
import pytest_asyncio
from src.data_loader.generic_data_loader import GenericDataLoader, ExcelProcessor, CSVProcessor, JSONProcessor
from src.utils.config_manager import ConfigManager
from tests.sqlite_adapter_mock import SQLiteAdapterMock
from unittest.mock import patch

@pytest.fixture
def config_manager():
    """Create a ConfigManager instance for testing."""
    return ConfigManager("tests/data_loader.ini")

@pytest.fixture
def db():
    """Create a database adapter instance for testing."""
    return SQLiteAdapterMock()

@pytest_asyncio.fixture
async def data_loader():
    """Create a GenericDataLoader instance for testing."""
    config_manager = ConfigManager("tests/data_loader.ini")
    db = SQLiteAdapterMock()
    loader = GenericDataLoader(db, "tests/data_loader.ini")
    await loader.initialize()
    return loader

@pytest.fixture
def sample_excel_data():
    return pd.DataFrame({
        'Column1': [1, 2, 3],
        'Column2': ['A', 'B', 'C']
    })

@pytest.fixture
def sample_csv_data():
    return pd.DataFrame({
        'Field1': [1, 2, 3],
        'Field2': ['X', 'Y', 'Z']
    })

@pytest.fixture
def sample_json_data():
    return [
        {'id': 1, 'name': 'Item 1'},
        {'id': 2, 'name': 'Item 2'}
    ]

@pytest.mark.asyncio
async def test_excel_processor(sample_excel_data):
    processor = ExcelProcessor(column_mapping={'Column1': 'col1', 'Column2': 'col2'})
    result = await processor.process(sample_excel_data)
    
    assert len(result) == 3
    assert result[0]['col1'] == 1
    assert result[0]['col2'] == 'A'

@pytest.mark.asyncio
async def test_csv_processor(sample_csv_data):
    processor = CSVProcessor(column_mapping={'Field1': 'field1', 'Field2': 'field2'})
    result = await processor.process(sample_csv_data)
    
    assert len(result) == 3
    assert result[0]['field1'] == 1
    assert result[0]['field2'] == 'X'

@pytest.mark.asyncio
async def test_json_processor(sample_json_data):
    processor = JSONProcessor()
    result = await processor.process(sample_json_data)
    
    assert len(result) == 2
    assert result[0]['id'] == 1
    assert result[0]['name'] == 'Item 1'

@pytest.mark.asyncio
async def test_load_data_single_file(data_loader, tmp_path):
    """Test loading data from a single file."""
    # Create test file
    file_path = tmp_path / "test.xlsx"
    df = pd.DataFrame({'A': [1, 2, 3], 'B': ['X', 'Y', 'Z']})
    df.to_excel(file_path, index=False)
    
    # Test loading
    results = await data_loader.load_data(str(file_path), "test_table")
    assert results[0]['status'] == 'success'
    assert results[0]['records_loaded'] == 3

@pytest.mark.asyncio
async def test_load_data_directory(data_loader, tmp_path):
    """Test loading data from a directory."""
    # Create test files
    for i in range(3):
        file_path = tmp_path / f"test_{i}.xlsx"
        df = pd.DataFrame({'A': [1, 2, 3], 'B': ['X', 'Y', 'Z']})
        df.to_excel(file_path, index=False)
    
    # Test loading
    results = await data_loader.load_data(str(tmp_path), "test_table")
    assert all(r['status'] == 'success' for r in results)
    assert sum(r['records_loaded'] for r in results if r['status'] == 'success') == 9

@pytest.mark.asyncio
async def test_invalid_file(data_loader, tmp_path):
    """Test handling of invalid files."""
    # Create invalid file
    file_path = tmp_path / "invalid.txt"
    file_path.write_text("invalid data")
    
    # Test loading
    results = await data_loader.load_data(str(file_path), "test_table")
    assert results[0]['status'] == 'error'
    assert 'error' in results[0]

@pytest.mark.asyncio
async def test_custom_processor(data_loader, tmp_path):
    """Test using a custom processor."""
    class CustomProcessor(ExcelProcessor):
        async def process(self, data):
            records = await super().process(data)
            return [{'custom': record['A']} for record in records]
    
    # Create test file
    file_path = tmp_path / "test.xlsx"
    df = pd.DataFrame({'A': [1, 2, 3]})
    df.to_excel(file_path, index=False)
    
    # Test loading with custom processor
    processor = CustomProcessor()
    results = await data_loader.load_data(str(file_path), "test_table", processor=processor)
    assert results[0]['status'] == 'success'
    assert results[0]['records_loaded'] == 3

@pytest.mark.asyncio
async def test_async_validator(data_loader, tmp_path):
    """Test using an async validator."""
    async def async_validator(data):
        return len(data) > 0
    
    # Create test file
    file_path = tmp_path / "test.xlsx"
    df = pd.DataFrame({'A': [1, 2, 3]})
    df.to_excel(file_path, index=False)
    
    # Test loading with async validator
    results = await data_loader.load_data(str(file_path), "test_table", validator=async_validator)
    assert results[0]['status'] == 'success'
    assert results[0]['records_loaded'] == 3

@pytest.mark.asyncio
async def test_data_load_report(data_loader):
    """Test creating data load report."""
    report = await data_loader.create_data_load_report(
        status='success',
        details={'records_loaded': 10},
        file_path='test.xlsx'
    )
    assert report['status'] == 'success'
    assert report['details']['records_loaded'] == 10
    assert report['file_path'] == 'test.xlsx'

@pytest.mark.asyncio
async def test_processor_error_handling(data_loader, tmp_path):
    """Test error handling in processors."""
    class FailingProcessor(ExcelProcessor):
        async def process(self, data):
            raise ValueError("Processing failed")

    # Create test file
    file_path = tmp_path / "test.xlsx"
    df = pd.DataFrame({'A': [1, 2, 3]})
    df.to_excel(file_path, index=False)

    # Test loading with failing processor
    processor = FailingProcessor()
    results = await data_loader.load_data(str(file_path), "test_table", processor=processor)
    assert results[0]['status'] == 'error'
    assert 'Processing failed' in results[0]['error']

@pytest.mark.asyncio
async def test_file_validation_failure(data_loader, tmp_path):
    """Test file validation failure."""
    def failing_validator(data):
        return False

    # Create test file
    file_path = tmp_path / "test.xlsx"
    df = pd.DataFrame({'A': [1, 2, 3]})
    df.to_excel(file_path, index=False)

    # Test loading with failing validator
    results = await data_loader.load_data(str(file_path), "test_table", validator=failing_validator)
    assert results[0]['status'] == 'skipped'

@pytest.mark.asyncio
async def test_empty_data_processing(data_loader, tmp_path):
    """Test processing file with no data after processing."""
    class EmptyProcessor(ExcelProcessor):
        async def process(self, data):
            return []  # Return empty list

    # Create test file
    file_path = tmp_path / "test.xlsx"
    df = pd.DataFrame({'A': [1, 2, 3]})
    df.to_excel(file_path, index=False)

    # Test loading with empty processor
    processor = EmptyProcessor()
    results = await data_loader.load_data(str(file_path), "test_table", processor=processor)
    assert results[0]['status'] == 'error'
    assert 'No records found after processing' in results[0]['error']

@pytest.mark.asyncio
async def test_database_error_handling(tmp_path):
    """Test database error handling."""
    class FailingDB:
        def connect(self):
            pass

        async def insert_data(self, table_name, data):
            raise Exception("Database error")

    config_manager = ConfigManager("tests/data_loader.ini")
    db = FailingDB()
    loader = GenericDataLoader(db, "tests/data_loader.ini")
    await loader.initialize()

    # Create test file
    file_path = tmp_path / "test.xlsx"
    df = pd.DataFrame({'A': [1, 2, 3]})
    df.to_excel(file_path, index=False)

    # Test loading with failing database
    results = await loader.load_data(str(file_path), "test_table")
    assert results[0]['status'] == 'error'
    assert 'Database error' in results[0]['error']

@pytest.mark.asyncio
async def test_unsupported_file_extension(data_loader, tmp_path):
    """Test handling of unsupported file extensions."""
    # Create unsupported file
    file_path = tmp_path / "test.txt"
    file_path.write_text("some text content")

    # Test loading unsupported file
    results = await data_loader.load_data(str(file_path), "test_table")
    assert results[0]['status'] == 'error'
    assert 'Unsupported file extension' in results[0]['error']

@pytest.mark.asyncio
async def test_json_processor_with_invalid_data():
    """Test JSON processor with invalid data."""
    processor = JSONProcessor()

    # Test with invalid JSON structure
    invalid_data = "not a list or dict"
    with pytest.raises(ValueError):
        await processor.process(invalid_data)

@pytest.mark.asyncio
async def test_excel_processor_column_mapping():
    """Test Excel processor with column mapping."""
    df = pd.DataFrame({
        'Old_Name': ['John', 'Jane'],
        'Old_Age': [25, 30]
    })

    processor = ExcelProcessor(column_mapping={'Old_Name': 'name', 'Old_Age': 'age'})
    result = await processor.process(df)

    assert len(result) == 2
    assert 'name' in result[0]
    assert 'age' in result[0]
    assert result[0]['name'] == 'John'
    assert result[0]['age'] == 25

@pytest.mark.asyncio
async def test_csv_processor_with_nan_values():
    """Test CSV processor handling NaN values."""
    df = pd.DataFrame({
        'Name': ['John', None, 'Jane'],
        'Age': [25, None, 30]
    })

    processor = CSVProcessor()
    result = await processor.process(df)

    assert len(result) == 3
    # NaN values should be converted to None
    assert result[1]['Name'] is None
    assert result[1]['Age'] is None

@pytest.mark.asyncio
async def test_move_processed_file(data_loader, tmp_path):
    """Test moving processed files."""
    # Create test file
    file_path = tmp_path / "test.xlsx"
    df = pd.DataFrame({'A': [1, 2, 3]})
    df.to_excel(file_path, index=False)

    # Create processed directory
    processed_dir = tmp_path / "processed"
    processed_dir.mkdir()

    # Mock the get_processed_dir method
    with patch.object(data_loader.config, 'get_processed_dir', return_value=processed_dir):
        results = await data_loader.load_data(str(file_path), "test_table", move_processed=True)

        assert results[0]['status'] == 'success'
        # Original file should be moved
        assert not file_path.exists()
        # File should exist in processed directory
        moved_files = list(processed_dir.glob("*"))
        assert len(moved_files) == 1

@pytest.mark.asyncio
async def test_concurrent_file_processing(data_loader, tmp_path):
    """Test concurrent processing of multiple files."""
    # Create multiple test files
    for i in range(5):
        file_path = tmp_path / f"test_{i}.xlsx"
        df = pd.DataFrame({'A': [i, i+1, i+2]})
        df.to_excel(file_path, index=False)

    # Test loading directory
    results = await data_loader.load_data(str(tmp_path), "test_table")

    # All files should be processed successfully
    successful_results = [r for r in results if r['status'] == 'success']
    assert len(successful_results) == 5

    # Total records should be 15 (3 records per file * 5 files)
    total_records = sum(r['records_loaded'] for r in successful_results)
    assert total_records == 15