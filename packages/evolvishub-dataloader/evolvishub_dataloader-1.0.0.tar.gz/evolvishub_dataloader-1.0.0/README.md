<div align="center">
  <img src="assets/png/eviesales.png" alt="Evolvishub Logo" width="200"/>
  <p><a href="https://evolvis.ai">Evolvis AI</a> - Empowering Innovation Through AI</p>
</div>

# Evolvishub Data Loader

A robust, asynchronous data loading and processing framework designed for handling various file formats and database integrations.

---

**Company:** [Evolvis AI](https://evolvis.ai)

**Author:** Alban Maxhuni, PhD  \
Email: a.maxhuni@evolvis.ai

---

## Features

- **Multi-Format Support**: Process Excel, CSV, JSON, and custom file formats
- **Asynchronous Processing**: Built with Python's asyncio for efficient I/O operations
- **Configurable**: YAML and INI configuration support
- **Database Integration**: SQLite and PostgreSQL support
- **Error Handling**: Comprehensive error handling and logging
- **File Management**: Automatic file movement and organization
- **Notification System**: Integrated notification system for process updates
- **Extensible**: Easy to add new processors and validators

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/evolvishub-dataloader.git
cd evolvishub-dataloader
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

The framework supports both YAML and INI configuration formats. Configuration files should be placed in the `config` directory.

### Example YAML Configuration

```yaml
# Data Types Configuration
data_types:
  types: "inventory,sales,purchases,orders,custom"

# Directory Configuration
directories:
  root: "data"
  processed: "data/processed"
  failed: "data/failed"

# Database Configuration
database:
  path: "data/database.db"
  migrations: "migrations"
  backup: "backups"

# File Processing Configuration
processing:
  move_processed: true
  add_timestamp: true
  retry_attempts: 3
  max_file_size: 10485760  # 10MB
```

## Usage

### Basic Usage

```python
from src.data_loader.generic_data_loader import GenericDataLoader
from src.data_loader.sqlite_adapter import SQLiteAdapter

async def main():
    # Initialize database adapter
    db = SQLiteAdapter()
    
    # Create data loader instance
    loader = GenericDataLoader(db)
    await loader.initialize()
    
    # Load data from a file
    results = await loader.load_data(
        source="path/to/your/file.xlsx",
        table_name="your_table_name"
    )
    
    # Process results
    for result in results:
        print(f"Status: {result['status']}")
        print(f"Records loaded: {result.get('records_loaded', 0)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### Custom Processors

You can create custom processors for specific file formats:

```python
from src.data_loader.generic_data_loader import DataProcessor

class CustomProcessor(DataProcessor):
    async def process(self, data):
        # Your custom processing logic here
        return processed_data
```

### Validation

Add custom validation to your data loading process:

```python
async def custom_validator(data):
    # Your validation logic here
    return True

results = await loader.load_data(
    source="path/to/your/file.xlsx",
    table_name="your_table_name",
    validator=custom_validator
)
```

## Testing

Run the test suite:

```bash
PYTHONPATH=./ python -m pytest tests/ -v
```

## Project Structure

```
evolvishub-dataloader/
├── config/
│   ├── data_loader.yaml
│   └── data_loader.ini
├── src/
│   └── data_loader/
│       ├── generic_data_loader.py
│       ├── sqlite_adapter.py
│       └── processors/
├── tests/
│   ├── test_generic_data_loader.py
│   ├── test_config_manager.py
│   └── test_specific_loaders.py
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Acknowledgments

- Thanks to all contributors who have helped shape this project
- Built with [SQLAlchemy](https://www.sqlalchemy.org/)
- Powered by [pandas](https://pandas.pydata.org/)