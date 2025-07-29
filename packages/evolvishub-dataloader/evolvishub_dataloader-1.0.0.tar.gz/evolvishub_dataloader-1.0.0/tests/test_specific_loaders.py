"""Tests for specific data loaders."""

import pytest
import pandas as pd
from pathlib import Path
import pytest_asyncio
from src.data_loader.generic_data_loader import GenericDataLoader
from src.utils.config_manager import ConfigManager
from tests.sqlite_adapter_mock import SQLiteAdapterMock

@pytest.fixture
def config_manager():
    """Create a ConfigManager instance for testing."""
    return ConfigManager("tests/data_loader.ini")

@pytest_asyncio.fixture
async def data_loader():
    """Create a GenericDataLoader instance for testing."""
    config_manager = ConfigManager("tests/data_loader.ini")
    db = SQLiteAdapterMock()
    loader = GenericDataLoader(db, "tests/data_loader.ini")
    await loader.initialize()
    return loader

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return pd.DataFrame({
        'date': ['2024-01-01', '2024-01-02'],
        'inv_no': ['INV001', 'INV002'],
        'amount': [100.0, 200.0]
    })

@pytest.mark.asyncio
async def test_custom_processor(data_loader, tmp_path):
    """Test using a custom processor."""
    class CustomProcessor:
        async def process(self, data):
            return data.to_dict('records')

    # Create test file
    file_path = tmp_path / "test.xlsx"
    df = pd.DataFrame({'A': [1, 2, 3]})
    df.to_excel(file_path, index=False)

    processor = CustomProcessor()
    results = await data_loader.load_data(str(file_path), "test_table", processor=processor)
    assert results[0]['status'] == 'success'
    assert results[0]['records_loaded'] == 3

@pytest.mark.asyncio
async def test_data_loader(data_loader, tmp_path):
    """Test data loader functionality."""
    # Create test file
    file_path = tmp_path / "test.xlsx"
    df = pd.DataFrame({'date': ['2024-01-01', '2024-01-02'], 'inv_no': ['INV001', 'INV002'], 'amount': [100.0, 200.0]})
    df.to_excel(file_path, index=False)

    results = await data_loader.load_data(str(file_path), "test_table")
    assert results[0]['status'] == 'success'
    assert results[0]['records_loaded'] == 2 