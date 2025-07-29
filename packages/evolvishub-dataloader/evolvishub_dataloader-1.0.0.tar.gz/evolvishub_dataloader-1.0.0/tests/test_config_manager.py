import pytest
import yaml
import configparser
from pathlib import Path
import tempfile
import os
from src.utils.config_manager import ConfigManager

@pytest.fixture
def yaml_config_file():
    """Create a temporary YAML config file for testing."""
    config = {
        'directories': {
            'root': 'test_data',
            'inventory': 'test_data/inventory',
            'sales': 'test_data/sales',
            'purchases': 'test_data/purchases',
            'orders': 'test_data/orders',
            'custom': 'test_data/custom'
        },
        'database': {
            'path': 'test_data/database.db',
            'migrations_path': 'test_migrations'
        },
        'processing': {
            'move_processed': True,
            'add_timestamp': True,
            'timestamp_format': '%Y%m%d_%H%M%S',
            'retry_attempts': 3,
            'retry_delay': 2
        },
        'extensions': {
            'excel': ['.xlsx', '.xls'],
            'csv': ['.csv'],
            'json': ['.json']
        },
        'column_mappings': {
            'sales': {
                'cus_no': 'customer_id',
                'inv_date': 'date',
                'inv_no': 'invoice_number'
            },
            'inventory': {
                'item_no': 'product_id',
                'item_desc_1': 'description'
            },
            'orders': {
                'Order No.': 'order_number',
                'Order Date': 'date'
            }
        },
        'notification': {
            'config_file': 'test_config/notification.ini',
            'types': ['info', 'error']
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(config, f)
        return f.name

@pytest.fixture
def ini_config_file():
    """Create a temporary INI config file for testing."""
    config = configparser.ConfigParser(interpolation=None)  # Disable interpolation
    
    config['directories'] = {
        'root': 'test_data',
        'inventory': 'test_data/inventory',
        'sales': 'test_data/sales',
        'purchases': 'test_data/purchases',
        'orders': 'test_data/orders',
        'custom': 'test_data/custom'
    }
    
    config['database'] = {
        'path': 'test_data/database.db',
        'migrations_path': 'test_migrations'
    }
    
    config['processing'] = {
        'move_processed': 'true',
        'add_timestamp': 'true',
        'timestamp_format': '%Y%m%d_%H%M%S',
        'retry_attempts': '3',
        'retry_delay': '2'
    }
    
    config['logging'] = {
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'file': 'logs/data_loader.log',
        'max_size': '10485760',
        'backup_count': '5'
    }
    
    config['notifications'] = {
        'enabled': 'true',
        'email': 'test@example.com',
        'slack_webhook': 'https://hooks.slack.com/services/test'
    }
    
    config['column_mappings'] = {
        'sales': 'inv_no=invoice_number,inv_date=date,cus_no=customer_id',
        'inventory': 'item_no=product_id,item_desc_1=description',
        'orders': 'Order No.=order_number,Order Date=date'
    }
    
    config['extensions'] = {
        'excel': '.xlsx,.xls',
        'csv': '.csv',
        'json': '.json'
    }
    
    config['notification'] = {
        'config_file': 'test_config/notification.ini',
        'types': 'info,error'
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
        config.write(f)
        return f.name

@pytest.fixture
def cleanup_files(yaml_config_file, ini_config_file):
    """Clean up temporary files after tests."""
    yield
    os.unlink(yaml_config_file)
    os.unlink(ini_config_file)

def test_init_yaml(yaml_config_file, cleanup_files):
    """Test initialization with YAML config file."""
    config = ConfigManager(yaml_config_file)
    assert config.config_file == Path(yaml_config_file)
    assert isinstance(config.config, dict)

def test_init_ini(ini_config_file, cleanup_files):
    """Test initialization with INI config file."""
    config = ConfigManager(ini_config_file)
    assert config.config_file == Path(ini_config_file)
    assert isinstance(config.config, dict)

def test_init_invalid_file():
    """Test initialization with non-existent file."""
    with pytest.raises(FileNotFoundError):
        ConfigManager("nonexistent.yaml")

def test_init_invalid_format():
    """Test initialization with unsupported file format."""
    with tempfile.NamedTemporaryFile(suffix='.txt') as f:
        with pytest.raises(ValueError):
            ConfigManager(f.name)

def test_get(yaml_config_file, cleanup_files):
    """Test getting configuration values."""
    config = ConfigManager(yaml_config_file)
    
    # Test getting nested values
    assert config.get('directories.root') == 'test_data'
    assert config.get('database.path') == 'test_data/database.db'
    
    # Test getting non-existent values
    assert config.get('nonexistent') is None
    assert config.get('nonexistent', default='default') == 'default'

def test_get_data_dir(yaml_config_file, cleanup_files):
    """Test getting data directory paths."""
    config = ConfigManager(yaml_config_file)
    
    # Test getting directory for each data type
    assert config.get_data_dir('inventory') == Path('test_data/inventory')
    assert config.get_data_dir('sales') == Path('test_data/sales')
    assert config.get_data_dir('purchases') == Path('test_data/purchases')
    assert config.get_data_dir('orders') == Path('test_data/orders')
    assert config.get_data_dir('custom') == Path('test_data/custom')
    
    # Test with non-existent data type
    assert config.get_data_dir('nonexistent') == Path('test_data/nonexistent')

def test_get_processed_dir(yaml_config_file, cleanup_files):
    """Test getting processed directory paths."""
    config = ConfigManager(yaml_config_file)
    
    # Test getting processed directory for each data type
    assert config.get_processed_dir('inventory') == Path('test_data/inventory/processed')
    assert config.get_processed_dir('sales') == Path('test_data/sales/processed')
    
    # Test with non-existent data type
    assert config.get_processed_dir('nonexistent') == Path('test_data/nonexistent/processed')

def test_get_failed_dir(yaml_config_file, cleanup_files):
    """Test getting failed directory paths."""
    config = ConfigManager(yaml_config_file)
    
    # Test getting failed directory for each data type
    assert config.get_failed_dir('inventory') == Path('test_data/inventory/failed')
    assert config.get_failed_dir('sales') == Path('test_data/sales/failed')
    
    # Test with non-existent data type
    assert config.get_failed_dir('nonexistent') == Path('test_data/nonexistent/failed')

def test_get_column_mapping(yaml_config_file, cleanup_files):
    """Test getting column mappings."""
    config = ConfigManager(yaml_config_file)
    
    # Test getting mappings for each data type
    sales_mapping = config.get_column_mapping('sales')
    assert sales_mapping['cus_no'] == 'customer_id'
    assert sales_mapping['inv_date'] == 'date'
    assert sales_mapping['inv_no'] == 'invoice_number'
    
    inventory_mapping = config.get_column_mapping('inventory')
    assert inventory_mapping['item_no'] == 'product_id'
    assert inventory_mapping['item_desc_1'] == 'description'
    
    orders_mapping = config.get_column_mapping('orders')
    assert orders_mapping['Order No.'] == 'order_number'
    assert orders_mapping['Order Date'] == 'date'
    
    # Test with non-existent data type
    assert config.get_column_mapping('nonexistent') == {}

def test_get_supported_extensions(yaml_config_file, cleanup_files):
    """Test getting supported file extensions."""
    config = ConfigManager(yaml_config_file)
    
    # Test getting extensions for each file type
    assert config.get_supported_extensions('excel') == ['.xlsx', '.xls']
    assert config.get_supported_extensions('csv') == ['.csv']
    assert config.get_supported_extensions('json') == ['.json']
    
    # Test with non-existent file type
    assert config.get_supported_extensions('nonexistent') == []

def test_get_processing_config(yaml_config_file, cleanup_files):
    """Test getting processing configuration."""
    config = ConfigManager(yaml_config_file)
    
    processing_config = config.get_processing_config()
    assert processing_config['move_processed'] is True
    assert processing_config['add_timestamp'] is True
    assert processing_config['timestamp_format'] == '%Y%m%d_%H%M%S'
    assert processing_config['retry_attempts'] == 3
    assert processing_config['retry_delay'] == 2

def test_get_database_config(yaml_config_file, cleanup_files):
    """Test getting database configuration."""
    config = ConfigManager(yaml_config_file)
    
    database_config = config.get_database_config()
    assert database_config['path'] == 'test_data/database.db'
    assert database_config['migrations_path'] == 'test_migrations'

def test_yaml_ini_equivalence(yaml_config_file, ini_config_file, cleanup_files):
    """Test that YAML and INI configurations produce equivalent results."""
    yaml_config = ConfigManager(yaml_config_file)
    ini_config = ConfigManager(ini_config_file)

    # Test that both configurations produce the same results
    assert yaml_config.get_data_dir('inventory') == ini_config.get_data_dir('inventory')
    assert yaml_config.get_column_mapping('sales') == ini_config.get_column_mapping('sales')
    assert yaml_config.get_supported_extensions('excel') == ini_config.get_supported_extensions('excel')
    assert yaml_config.get_processing_config() == ini_config.get_processing_config()
    assert yaml_config.get_database_config() == ini_config.get_database_config()

def test_get_nested_keys(yaml_config_file, cleanup_files):
    """Test getting deeply nested configuration values."""
    config = ConfigManager(yaml_config_file)

    # Test deeply nested access
    assert config.get('processing.move_processed') is True
    assert config.get('processing.retry_attempts') == 3
    assert config.get('database.path') == 'test_data/database.db'

def test_get_with_default_values(yaml_config_file, cleanup_files):
    """Test getting configuration values with default fallbacks."""
    config = ConfigManager(yaml_config_file)

    # Test existing values
    assert config.get('directories.root', default='fallback') == 'test_data'

    # Test non-existent values with defaults
    assert config.get('nonexistent.key', default='default_value') == 'default_value'
    assert config.get('directories.nonexistent', default='fallback') == 'fallback'

def test_get_section_only(yaml_config_file, cleanup_files):
    """Test getting entire sections."""
    config = ConfigManager(yaml_config_file)

    # Test getting entire section
    directories = config.get('directories')
    assert isinstance(directories, dict)
    assert directories['root'] == 'test_data'
    assert directories['inventory'] == 'test_data/inventory'

def test_malformed_yaml_file():
    """Test handling of malformed YAML file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("invalid: yaml: content: [unclosed")
        f.flush()

        with pytest.raises(Exception):  # Should raise YAML parsing error
            ConfigManager(f.name)

        os.unlink(f.name)

def test_malformed_ini_file():
    """Test handling of malformed INI file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
        f.write("[section\ninvalid ini content")
        f.flush()

        with pytest.raises(Exception):  # Should raise INI parsing error
            ConfigManager(f.name)

        os.unlink(f.name)

def test_empty_yaml_file():
    """Test handling of empty YAML file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("")
        f.flush()

        config = ConfigManager(f.name)
        assert config.config == {} or config.config is None

        os.unlink(f.name)

def test_empty_ini_file():
    """Test handling of empty INI file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
        f.write("")
        f.flush()

        config = ConfigManager(f.name)
        assert isinstance(config.config, dict)

        os.unlink(f.name)

def test_get_column_mapping_with_string_format(ini_config_file, cleanup_files):
    """Test getting column mappings from INI string format."""
    config = ConfigManager(ini_config_file)

    # INI format stores mappings as comma-separated strings
    sales_mapping = config.get_column_mapping('sales')
    assert isinstance(sales_mapping, dict)
    assert 'inv_no' in sales_mapping
    assert sales_mapping['inv_no'] == 'invoice_number'

def test_get_supported_extensions_from_string(ini_config_file, cleanup_files):
    """Test getting extensions from INI string format."""
    config = ConfigManager(ini_config_file)

    # INI format stores extensions as comma-separated strings
    excel_extensions = config.get_supported_extensions('excel')
    assert isinstance(excel_extensions, list)
    assert '.xlsx' in excel_extensions
    assert '.xls' in excel_extensions

def test_config_file_path_handling():
    """Test different path formats for config files."""
    # Test with Path object
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("test: value")
        f.flush()

        config = ConfigManager(Path(f.name))
        assert config.config_file == Path(f.name)

        os.unlink(f.name)

def test_get_with_none_section(yaml_config_file, cleanup_files):
    """Test get method with None values."""
    config = ConfigManager(yaml_config_file)

    # Test with None section
    result = config.get(None, default='default')
    assert result == 'default'

def test_get_processing_config_missing_keys(yaml_config_file, cleanup_files):
    """Test processing config with missing keys."""
    config = ConfigManager(yaml_config_file)

    # Remove processing section temporarily
    original_config = config.config.copy()
    config.config = {k: v for k, v in config.config.items() if k != 'processing'}

    processing_config = config.get_processing_config()
    assert processing_config == {}

    # Restore original config
    config.config = original_config

def test_directory_methods_with_missing_root(yaml_config_file, cleanup_files):
    """Test directory methods when root directory is missing."""
    config = ConfigManager(yaml_config_file)

    # Remove directories section temporarily
    original_config = config.config.copy()
    config.config = {k: v for k, v in config.config.items() if k != 'directories'}

    # Should use default 'data' directory
    data_dir = config.get_data_dir('test')
    assert data_dir == Path('data/test')

    # Restore original config
    config.config = original_config

def test_edge_case_data_types():
    """Test configuration with edge case data types."""
    config_data = {
        'numbers': {
            'zero': 0,
            'negative': -1,
            'float': 3.14159
        },
        'booleans': {
            'true_val': True,
            'false_val': False
        },
        'lists': {
            'empty': [],
            'mixed': [1, 'string', True, None]
        },
        'none_values': {
            'explicit_none': None
        }
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(config_data, f)
        f.flush()

        config = ConfigManager(f.name)

        # Test various data types
        assert config.get('numbers.zero') == 0
        assert config.get('numbers.negative') == -1
        assert config.get('numbers.float') == 3.14159
        assert config.get('booleans.true_val') is True
        assert config.get('booleans.false_val') is False
        assert config.get('lists.empty') == []
        assert config.get('lists.mixed') == [1, 'string', True, None]
        assert config.get('none_values.explicit_none') is None

        os.unlink(f.name)