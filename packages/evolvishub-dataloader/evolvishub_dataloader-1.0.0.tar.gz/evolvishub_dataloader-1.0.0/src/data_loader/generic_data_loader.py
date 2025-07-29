import json
from typing import Any, Dict, List, Optional, Union, Callable
from pathlib import Path
import os
import re
import shutil
from datetime import datetime
import time
import asyncio
import pandas as pd
import aiofiles
from abc import ABC, abstractmethod

from src.utils.logger import get_logger
from src.utils.config_manager import ConfigManager
from .sqlite_adapter import SQLiteAdapter

logger = get_logger(__name__)

class DataProcessor(ABC):
    """Abstract base class for data processors."""
    
    @abstractmethod
    async def process(self, data: Any) -> List[Dict[str, Any]]:
        """Process the input data and return a list of records."""
        pass

class ExcelProcessor(DataProcessor):
    """Processor for Excel files."""
    
    def __init__(self, header_row: Optional[int] = None, column_mapping: Optional[Dict[str, str]] = None):
        self.header_row = header_row
        self.column_mapping = column_mapping or {}
    
    async def process(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Process Excel data into records."""
        if self.header_row is not None:
            data.columns = data.iloc[self.header_row]
            data = data.iloc[self.header_row + 1:]
        
        if self.column_mapping:
            data = data.rename(columns=self.column_mapping)
        
        return data.to_dict(orient='records')

class CSVProcessor(DataProcessor):
    """Processor for CSV files."""
    
    def __init__(self, column_mapping: Optional[Dict[str, str]] = None):
        self.column_mapping = column_mapping or {}
    
    async def process(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Process CSV data into records."""
        if self.column_mapping:
            data = data.rename(columns=self.column_mapping)
        records = data.to_dict(orient='records')
        # Convert NaN to None
        import math
        for rec in records:
            for k, v in rec.items():
                if isinstance(v, float) and math.isnan(v):
                    rec[k] = None
        return records

class JSONProcessor(DataProcessor):
    """Processor for JSON files."""
    
    async def process(self, data: Union[Dict, List]) -> List[Dict[str, Any]]:
        """Process JSON data into records."""
        if isinstance(data, dict):
            return [data]
        if isinstance(data, list):
            return data
        raise ValueError("Input data must be a dict or list")

class GenericDataLoader:
    """
    A generic data loader that can handle various data sources and formats asynchronously.
    """
    
    def __init__(self, db: SQLiteAdapter, config_file: str):
        """
        Initialize the GenericDataLoader.
        
        Args:
            db (SQLiteAdapter): Database adapter instance
            config_file (str): Path to the configuration file
        """
        self.db = db
        self.config = ConfigManager(config_file)
        # Register default processors
        self.processors = {
            (ext if ext.startswith('.') else f'.{ext}'): ExcelProcessor for ext in self.config.get_supported_extensions('excel')
        }
        self.processors.update({
            (ext if ext.startswith('.') else f'.{ext}'): CSVProcessor for ext in self.config.get_supported_extensions('csv')
        })
        self.processors.update({
            (ext if ext.startswith('.') else f'.{ext}'): JSONProcessor for ext in self.config.get_supported_extensions('json')
        })
        self._initialized = False
    
    async def initialize(self):
        """Initialize the data loader asynchronously."""
        if not self._initialized:
            await self._ensure_data_directories()
            self.db.connect()
            self._initialized = True
    
    async def _ensure_data_directories(self):
        """Ensure all required data directories exist asynchronously."""
        data_types = self.config.get('data_types', 'types', '').split(',')
        data_types = [dt.strip() for dt in data_types if dt.strip()]
        
        for data_type in data_types:
            # Create main data directory
            data_dir = self.config.get_data_dir(data_type)
            data_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Ensured directory exists: {data_dir}")
            
            # Create processed directory
            processed_dir = self.config.get_processed_dir(data_type)
            processed_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Ensured directory exists: {processed_dir}")
            
            # Create failed directory
            failed_dir = self.config.get_failed_dir(data_type)
            failed_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Ensured directory exists: {failed_dir}")
    
    def register_processor(self, file_extension: str, processor_class: type):
        """
        Register a new processor for a file extension.
        
        Args:
            file_extension (str): File extension (e.g., '.xlsx')
            processor_class (type): Processor class that implements DataProcessor
        """
        if not issubclass(processor_class, DataProcessor):
            raise ValueError("Processor class must implement DataProcessor")
        self.processors[file_extension] = processor_class
    
    def _get_processor(self, file_path: str) -> DataProcessor:
        """
        Get the appropriate processor for a file.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            DataProcessor: The appropriate processor instance
        """
        ext = os.path.splitext(file_path)[1].lower()
        processor_class = self.processors.get(ext)
        if not processor_class:
            raise ValueError(f"No processor registered for extension: {ext}")
        return processor_class()
    
    async def _read_file(self, file_path: str) -> Any:
        """
        Read a file based on its extension asynchronously.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            Any: The file contents in an appropriate format
        """
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in self.config.get_supported_extensions('excel'):
            # Use asyncio.to_thread for CPU-bound operations
            return await asyncio.to_thread(pd.read_excel, file_path)
        elif ext in self.config.get_supported_extensions('csv'):
            return await asyncio.to_thread(pd.read_csv, file_path)
        elif ext in self.config.get_supported_extensions('json'):
            async with aiofiles.open(file_path, 'r') as f:
                content = await f.read()
                return json.loads(content)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")
    
    async def _validate_file(self, file_path: str, validator: Optional[Callable[[Any], bool]] = None) -> bool:
        """
        Validate a file asynchronously.
        
        Args:
            file_path (str): Path to the file
            validator (Callable, optional): Custom validation function
            
        Returns:
            bool: True if file is valid, False otherwise
        """
        try:
            data = await self._read_file(file_path)
            if validator:
                if asyncio.iscoroutinefunction(validator):
                    return await validator(data)
                return validator(data)
            return True
        except Exception as e:
            logger.error(f"Error validating file {file_path}: {str(e)}")
            return False
    
    async def _process_file(self, file_path: str, table_name: str, processor: Optional[DataProcessor] = None) -> Dict[str, Any]:
        """
        Process a single file asynchronously.
        
        Args:
            file_path (str): Path to the file
            table_name (str): Name of the target database table
            processor (DataProcessor, optional): Custom processor instance
            
        Returns:
            Dict[str, Any]: Processing results
        """
        try:
            # Read the file
            data = await self._read_file(file_path)
            
            # Get or create processor
            if processor is None:
                processor = self._get_processor(file_path)
            
            # Process the data
            records = await processor.process(data)
            
            if not records:
                raise ValueError("No records found after processing")
            
            # Insert into database
            await self.db.insert_data(table_name, records)
            
            return {
                'status': 'success',
                'records_loaded': len(records),
                'file_path': file_path
            }
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'file_path': file_path
            }
    
    async def load_data(self, 
                       source: Union[str, Path], 
                       table_name: str,
                       processor: Optional[DataProcessor] = None,
                       validator: Optional[Callable[[Any], bool]] = None,
                       move_processed: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Load data from a source into a database table asynchronously.
        
        Args:
            source (Union[str, Path]): Path to file or directory
            table_name (str): Name of the target database table
            processor (DataProcessor, optional): Custom processor instance
            validator (Callable, optional): Custom validation function
            move_processed (bool, optional): Whether to move processed files
            
        Returns:
            List[Dict[str, Any]]: List of processing results
        """
        source_path = Path(source)
        results = []
        processing_config = self.config.get_processing_config()
        move_processed = move_processed if move_processed is not None else processing_config.get('move_processed', True)
        try:
            if source_path.is_file():
                ext = source_path.suffix.lower()
                if ext not in self.processors:
                    results.append({'status': 'error', 'error': f'Unsupported file extension: {ext}', 'file_path': str(source_path)})
                    return results
                if await self._validate_file(str(source_path), validator):
                    result = await self._process_file(str(source_path), table_name, processor)
                    results.append(result)
                    if move_processed and result['status'] == 'success':
                        await self._move_processed_file(source_path)
                else:
                    results.append({'status': 'skipped', 'file_path': str(source_path)})
            else:
                tasks = []
                for file_path in source_path.glob('*'):
                    if file_path.is_file() and file_path.suffix.lower() in self.processors:
                        tasks.append(self._process_single_file(file_path, table_name, processor, validator, move_processed))
                results = await asyncio.gather(*tasks)
            return results
        except Exception as e:
            logger.error(f"Error loading data from {source}: {str(e)}")
            raise
    
    async def _process_single_file(self, file_path: Path, table_name: str, processor: Optional[DataProcessor],
                                 validator: Optional[Callable[[Any], bool]], move_processed: bool) -> Dict[str, Any]:
        """Helper method to process a single file asynchronously."""
        if await self._validate_file(str(file_path), validator):
            result = await self._process_file(str(file_path), table_name, processor)
            if move_processed and result['status'] == 'success':
                await self._move_processed_file(file_path)
            return result
        return {'status': 'skipped', 'file_path': str(file_path)}
    
    async def _move_processed_file(self, file_path: Path):
        """
        Move a processed file to the processed directory asynchronously.
        
        Args:
            file_path (Path): Path to the processed file
        """
        try:
            processing_config = self.config.get_processing_config()
            timestamp_format = processing_config.get('timestamp_format', '%Y%m%d_%H%M%S')
            
            # Determine the appropriate directory based on file location
            data_types = self.config.get('data_types', 'types', '').split(',')
            data_types = [dt.strip() for dt in data_types if dt.strip()]
            
            for data_type in data_types:
                if str(self.config.get_data_dir(data_type)) in str(file_path):
                    processed_dir = self.config.get_processed_dir(data_type)
                    break
            else:
                processed_dir = file_path.parent / 'processed'
            
            processed_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime(timestamp_format)
            new_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
            target_path = processed_dir / new_name
            
            # Use retry logic for file moves
            retry_attempts = processing_config.get('retry_attempts', 5)
            retry_delay = processing_config.get('retry_delay', 1)
            
            for attempt in range(retry_attempts):
                try:
                    # Use asyncio.to_thread for file operations
                    await asyncio.to_thread(shutil.move, str(file_path), str(target_path))
                    logger.info(f"Moved processed file to: {target_path}")
                    break
                except (PermissionError, OSError) as e:
                    if attempt < retry_attempts - 1:
                        await asyncio.sleep(retry_delay)
                    else:
                        raise e
            
        except Exception as e:
            logger.error(f"Error moving processed file {file_path}: {str(e)}")
    
    async def create_data_load_report(self, 
                                    status: str, 
                                    error_message: Optional[str] = None, 
                                    details: Optional[Dict] = None,
                                    file_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a data load report in the database asynchronously.
        
        Args:
            status (str): Status of the data load ('success' or 'error')
            error_message (str, optional): Error message if status is 'error'
            details (dict, optional): Additional details about the data load
            file_path (str, optional): Path to the file being processed
            
        Returns:
            Dict[str, Any]: The created report
        """
        try:
            # Store details as JSON string in database
            details_json = json.dumps(details) if details else None
            
            report = {
                'timestamp': datetime.now(),
                'status': status,
                'error_message': error_message,
                'details': details_json,
                'file_path': file_path
            }
            
            await self.db.insert_data('data_load_reports', [report])
            logger.info(f"Created data load report with status: {status} for file: {file_path}")
            
            # Return report with parsed details
            return {
                'timestamp': report['timestamp'],
                'status': status,
                'error_message': error_message,
                'details': details,  # Return original details dict, not JSON string
                'file_path': file_path
            }
            
        except Exception as e:
            logger.error(f"Error creating data load report: {str(e)}")
            return {
                'status': 'error',
                'error_message': str(e),
                'timestamp': datetime.now()
            }

async def main():
    """Main function to demonstrate usage."""
    db = SQLiteAdapter()
    loader = GenericDataLoader(db)
    await loader.initialize()

if __name__ == '__main__':
    asyncio.run(main()) 