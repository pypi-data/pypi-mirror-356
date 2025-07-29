"""
EvolvisHub DataLoader - A comprehensive data loading framework.

This package provides a robust, async-capable data loading framework for Excel, CSV, 
and JSON files with built-in data validation, SQLite integration, and comprehensive 
error handling.

Key Features:
- Async/await support for concurrent file processing
- Excel (.xlsx, .xls), CSV, and JSON file support
- Built-in data validation and quality analysis
- SQLite database integration with automatic table creation
- Comprehensive error handling and logging
- Configurable processing with YAML/INI support
- Extensible processor architecture
- Production-ready with comprehensive test coverage

Example Usage:
    from evolvishub_dataloader import GenericDataLoader, SQLiteAdapter
    
    async def main():
        db = SQLiteAdapter("data.db")
        loader = GenericDataLoader(db, "config.yaml")
        await loader.initialize()
        
        results = await loader.load_data("data.xlsx", "my_table")
        print(f"Loaded {results[0]['records_loaded']} records")

For more information, see the documentation at:
https://github.com/evolvisai/evolvishub-dataloader
"""

__version__ = "1.0.0"
__author__ = "EvolvisAI"
__email__ = "info@evolvis.ai"
__license__ = "MIT"

# Import main classes for easy access
from .data_loader.generic_data_loader import (
    GenericDataLoader,
    DataProcessor,
    ExcelProcessor,
    CSVProcessor,
    JSONProcessor
)
from .data_loader.sqlite_adapter import SQLiteAdapter
from .data_loader.data_validation import validate_data, generate_validation_report
from .utils.config_manager import ConfigManager
from .utils.logger import get_logger

__all__ = [
    # Main classes
    "GenericDataLoader",
    "SQLiteAdapter", 
    "ConfigManager",
    
    # Processors
    "DataProcessor",
    "ExcelProcessor", 
    "CSVProcessor",
    "JSONProcessor",
    
    # Utilities
    "validate_data",
    "generate_validation_report",
    "get_logger",
    
    # Metadata
    "__version__",
    "__author__",
    "__email__",
    "__license__"
]
