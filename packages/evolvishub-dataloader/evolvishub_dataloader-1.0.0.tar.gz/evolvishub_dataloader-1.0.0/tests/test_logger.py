"""Tests for the logger utility module."""

import pytest
import logging
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.utils.logger import get_logger


@pytest.fixture
def temp_logs_dir():
    """Create a temporary logs directory for testing."""
    temp_dir = Path(tempfile.mkdtemp())
    logs_dir = temp_dir / 'logs'
    logs_dir.mkdir(exist_ok=True)
    
    # Patch the log_dir in the logger module
    with patch('src.utils.logger.Path') as mock_path:
        mock_path.return_value = logs_dir
        yield logs_dir
    
    # Cleanup
    shutil.rmtree(temp_dir)


@pytest.fixture
def cleanup_loggers():
    """Clean up loggers after each test to avoid interference."""
    yield
    # Remove all handlers from all loggers
    for logger_name in list(logging.Logger.manager.loggerDict.keys()):
        logger = logging.getLogger(logger_name)
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
            handler.close()


def test_get_logger_basic(cleanup_loggers):
    """Test basic logger creation."""
    logger = get_logger('test_logger')
    
    assert isinstance(logger, logging.Logger)
    assert logger.name == 'test_logger'
    assert logger.level == logging.INFO


def test_get_logger_handlers(cleanup_loggers, tmp_path):
    """Test that logger has both file and console handlers."""
    with patch('src.utils.logger.Path') as mock_path:
        mock_path.return_value = tmp_path / 'logs'

        logger = get_logger('test_logger')

        # Should have 2 handlers: file and console
        assert len(logger.handlers) == 2

        # Check handler types
        handler_types = [type(handler).__name__ for handler in logger.handlers]
        assert 'FileHandler' in handler_types
        assert 'StreamHandler' in handler_types


def test_get_logger_creates_logs_directory(cleanup_loggers, tmp_path):
    """Test that logger creates logs directory if it doesn't exist."""
    logs_dir = tmp_path / 'logs'

    with patch('src.utils.logger.Path') as mock_path:
        mock_path.return_value = logs_dir

        get_logger('test_logger')

        # Directory should be created
        assert logs_dir.exists()


def test_get_logger_same_instance(cleanup_loggers):
    """Test that getting the same logger name returns the same instance."""
    logger1 = get_logger('same_logger')
    logger2 = get_logger('same_logger')
    
    assert logger1 is logger2


def test_get_logger_no_duplicate_handlers(cleanup_loggers):
    """Test that calling get_logger multiple times doesn't add duplicate handlers."""
    logger1 = get_logger('test_logger')
    initial_handler_count = len(logger1.handlers)
    
    logger2 = get_logger('test_logger')
    final_handler_count = len(logger2.handlers)
    
    assert initial_handler_count == final_handler_count
    assert logger1 is logger2


def test_logger_formatter(cleanup_loggers, tmp_path):
    """Test that logger handlers have the correct formatter."""
    with patch('src.utils.logger.Path') as mock_path:
        mock_path.return_value = tmp_path / 'logs'

        logger = get_logger('test_logger')

        expected_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

        for handler in logger.handlers:
            assert handler.formatter is not None
            assert handler.formatter._fmt == expected_format


def test_logger_levels(cleanup_loggers, tmp_path):
    """Test that logger and handlers have correct levels."""
    with patch('src.utils.logger.Path') as mock_path:
        mock_path.return_value = tmp_path / 'logs'

        logger = get_logger('test_logger')

        assert logger.level == logging.INFO

        for handler in logger.handlers:
            assert handler.level == logging.INFO


def test_logger_file_path(cleanup_loggers, tmp_path):
    """Test that logger creates file with correct path."""
    logs_dir = tmp_path / 'logs'

    with patch('src.utils.logger.Path') as mock_path:
        mock_path.return_value = logs_dir

        logger_name = 'test_logger'
        get_logger(logger_name)

        # Verify the log file was created
        expected_log_file = logs_dir / f'{logger_name}.log'
        assert expected_log_file.exists()


def test_logger_different_names(cleanup_loggers):
    """Test that different logger names create different loggers."""
    logger1 = get_logger('logger1')
    logger2 = get_logger('logger2')
    
    assert logger1 is not logger2
    assert logger1.name == 'logger1'
    assert logger2.name == 'logger2'


def test_logger_logging_functionality(cleanup_loggers, tmp_path):
    """Test that logger actually logs messages."""
    with patch('src.utils.logger.Path') as mock_path:
        mock_path.return_value = tmp_path / 'logs'

        logger = get_logger('test_logger')

        # Mock the handlers to capture log records
        for handler in logger.handlers:
            handler.emit = MagicMock()

        # Test logging at different levels
        logger.info('Test info message')
        logger.warning('Test warning message')
        logger.error('Test error message')

        # Verify that handlers were called
        for handler in logger.handlers:
            assert handler.emit.call_count == 3


def test_logger_with_special_characters(cleanup_loggers):
    """Test logger creation with special characters in name."""
    special_names = ['test.logger', 'test-logger', 'test_logger', 'test123']
    
    for name in special_names:
        logger = get_logger(name)
        assert logger.name == name
        assert isinstance(logger, logging.Logger)


@pytest.mark.parametrize("logger_name", [
    "simple",
    "with.dots",
    "with-dashes", 
    "with_underscores",
    "with123numbers",
    "CamelCase",
    "mixedCase123"
])
def test_logger_name_variations(cleanup_loggers, logger_name):
    """Test logger creation with various name patterns."""
    logger = get_logger(logger_name)
    assert logger.name == logger_name
    assert isinstance(logger, logging.Logger)
    assert len(logger.handlers) == 2  # file and console handlers
