"""Configuration manager for data loader."""
import os
import yaml
import configparser
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

class ConfigManager:
    """Configuration manager for handling YAML and INI configuration files."""
    
    def __init__(self, config_file: str):
        """
        Initialize the configuration manager.
        
        Args:
            config_file (str): Path to the configuration file
        """
        self.config_file = Path(config_file)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if not self.config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_file}")
        
        if self.config_file.suffix.lower() == '.yaml':
            return self._load_yaml()
        elif self.config_file.suffix.lower() == '.ini':
            return self._load_ini()
        else:
            raise ValueError(f"Unsupported configuration file format: {self.config_file.suffix}")
    
    def _load_yaml(self) -> Dict[str, Any]:
        """Load YAML configuration."""
        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def _load_ini(self) -> Dict[str, Any]:
        """Load INI configuration."""
        config = configparser.ConfigParser(interpolation=None)  # Disable interpolation
        config.read(self.config_file)
        return self._convert_ini_to_dict(config)
    
    def _convert_ini_to_dict(self, config: configparser.ConfigParser) -> Dict[str, Any]:
        """Convert INI configuration to dictionary."""
        def convert_value(val, key=None, section=None):
            if val.lower() == 'true':
                return True
            if val.lower() == 'false':
                return False
            if val.isdigit():
                return int(val)
            try:
                return float(val)
            except ValueError:
                return val
        result = {}
        for section in config.sections():
            if section == 'column_mappings':
                result[section] = self._parse_column_mappings(config[section])
            elif section == 'supported_extensions':
                result['extensions'] = self._parse_extensions(config[section])
            else:
                result[section] = {k: convert_value(v, k, section) for k, v in config[section].items()}
        return result
    
    def _parse_column_mappings(self, section: configparser.SectionProxy) -> Dict[str, Dict[str, str]]:
        """Parse column mappings from INI format."""
        mappings = {}
        for key, value in section.items():
            mapping_dict = {}
            for pair in value.split(','):
                if '=' in pair:
                    src, dest = pair.split('=')
                    mapping_dict[src.strip()] = dest.strip()
            mappings[key] = mapping_dict
        return mappings
    
    def _parse_extensions(self, section: configparser.SectionProxy) -> Dict[str, List[str]]:
        """Parse supported extensions from INI format."""
        extensions = {}
        for key in section:
            ext_list = [ext.strip() for ext in section[key].split(',') if ext.strip()]
            extensions[key] = ext_list
        return extensions
    
    def get(self, section: str, key: Optional[str] = None, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            section (str): Configuration section or dot-notation path (e.g., 'directories.root')
            key (Optional[str]): Configuration key (if section doesn't contain dot notation)
            default (Any): Default value if key is not found
            
        Returns:
            Any: Configuration value
        """
        if section is None:
            return default
        # Handle dot notation in section
        if key is None and '.' in section:
            section, key = section.split('.', 1)
        
        if section not in self.config:
            return default
        
        if key is None:
            return self.config.get(section, default)
        
        section_data = self.config.get(section, {})
        if not isinstance(section_data, dict):
            return default
        
        # Handle nested keys
        if '.' in key:
            current = section_data
            for part in key.split('.'):
                if not isinstance(current, dict):
                    return default
                current = current.get(part)
                if current is None:
                    return default
            return current
        
        return section_data.get(key, default)
    
    def get_data_dir(self, data_type: str) -> Path:
        """Get data directory path for a specific data type."""
        base_dir = self.get('directories', 'root', 'data')
        return Path(base_dir) / data_type
    
    def get_processed_dir(self, data_type: str) -> Path:
        """Get processed directory path for a specific data type."""
        return self.get_data_dir(data_type) / 'processed'
    
    def get_failed_dir(self, data_type: str) -> Path:
        """Get failed directory path for a specific data type."""
        return self.get_data_dir(data_type) / 'failed'
    
    def get_column_mapping(self, data_type: str) -> Dict[str, str]:
        """Get column mapping for a specific data type."""
        return self.get('column_mappings', data_type, {})
    
    def get_supported_extensions(self, file_type: str) -> List[str]:
        """Get supported file extensions for a specific file type."""
        # Try 'extensions' first, then 'file_types' for compatibility
        exts = self.get('extensions', file_type, None)
        if exts is None:
            exts = self.get('file_types', file_type, [])
        if isinstance(exts, str):
            exts = [e.strip() for e in exts.split(',') if e.strip()]
        # Ensure all extensions start with a dot
        return [e if e.startswith('.') else f'.{e}' for e in exts]
    
    def get_processing_config(self) -> Dict[str, Any]:
        """Get processing configuration."""
        return self.config.get('processing', {})
    
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration."""
        return self.config.get('database', {}) 