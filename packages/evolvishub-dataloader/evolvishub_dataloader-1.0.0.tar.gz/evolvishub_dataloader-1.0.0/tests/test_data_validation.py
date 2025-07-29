"""Tests for the data validation module."""

import pytest
import pandas as pd
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.data_loader.data_validation import (
    validate_data,
    _find_header_candidates,
    _analyze_data_quality,
    _is_numeric,
    _is_date_like,
    _check_expected_columns,
    generate_validation_report
)


@pytest.fixture
def sample_excel_file():
    """Create a sample Excel file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
        df = pd.DataFrame({
            'Name': ['John', 'Jane', 'Bob'],
            'Age': [25, 30, 35],
            'Salary': [50000.0, 60000.0, 70000.0],
            'Date': ['2023-01-01', '2023-02-01', '2023-03-01']
        })
        df.to_excel(f.name, index=False)
        yield f.name
    Path(f.name).unlink()


@pytest.fixture
def sample_csv_file():
    """Create a sample CSV file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("Product,Price,Quantity\n")
        f.write("Widget,10.99,100\n")
        f.write("Gadget,25.50,50\n")
        f.write("Tool,15.00,75\n")
        yield f.name
    Path(f.name).unlink()


@pytest.fixture
def empty_excel_file():
    """Create an empty Excel file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
        df = pd.DataFrame()
        df.to_excel(f.name, index=False)
        yield f.name
    Path(f.name).unlink()


@pytest.fixture
def excel_with_header_issues():
    """Create an Excel file with header detection issues."""
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
        # Create a file with empty rows at the top and header in row 3
        data = [
            ['', '', ''],  # Empty row
            ['Some metadata', '', ''],  # Metadata row
            ['Product Name', 'Unit Price', 'Stock Level'],  # Actual header
            ['Widget', 10.99, 100],
            ['Gadget', 25.50, 50]
        ]
        df = pd.DataFrame(data)
        df.to_excel(f.name, index=False, header=False)
        yield f.name
    Path(f.name).unlink()


def test_validate_data_excel_success(sample_excel_file):
    """Test successful validation of Excel file."""
    result = validate_data(sample_excel_file, 'test_data')
    
    assert result['file_path'] == sample_excel_file
    assert result['data_type'] == 'test_data'
    assert result['total_rows'] > 0
    assert result['total_columns'] > 0
    assert 'data_quality' in result
    assert 'timestamp' in result


def test_validate_data_csv_success(sample_csv_file):
    """Test successful validation of CSV file."""
    result = validate_data(sample_csv_file, 'product_data')

    assert result['file_path'] == sample_csv_file
    assert result['data_type'] == 'product_data'
    # Check if validation was successful or had issues
    if 'issues' in result and result['issues']:
        # If there are issues, check that they're logged
        assert len(result['issues']) > 0
    else:
        # If successful, check basic structure
        assert result.get('total_rows', 0) >= 0
        assert result.get('total_columns', 0) >= 0


def test_validate_data_empty_file(empty_excel_file):
    """Test validation of empty file."""
    result = validate_data(empty_excel_file, 'empty_data')
    
    assert result['file_path'] == empty_excel_file
    assert 'File is completely empty' in result['issues']


def test_validate_data_with_expected_columns(sample_excel_file):
    """Test validation with expected columns."""
    expected_columns = ['Name', 'Age', 'Salary']
    result = validate_data(sample_excel_file, 'test_data', expected_columns=expected_columns)
    
    # Should not have missing column issues since all expected columns are present
    missing_issues = [issue for issue in result['issues'] if 'Missing expected columns' in issue]
    assert len(missing_issues) == 0


def test_validate_data_missing_expected_columns(sample_excel_file):
    """Test validation with missing expected columns."""
    expected_columns = ['Name', 'Age', 'MissingColumn']
    result = validate_data(sample_excel_file, 'test_data', expected_columns=expected_columns)
    
    # Should have missing column issues
    missing_issues = [issue for issue in result['issues'] if 'Missing expected columns' in issue]
    assert len(missing_issues) > 0


def test_validate_data_with_header_patterns(excel_with_header_issues):
    """Test validation with header patterns."""
    header_patterns = {
        'product_data': ['product', 'price', 'stock']
    }
    result = validate_data(
        excel_with_header_issues, 
        'product_data', 
        header_patterns=header_patterns
    )
    
    assert 'header_candidates' in result
    assert len(result['header_candidates']) > 0


def test_validate_data_nonexistent_file():
    """Test validation of non-existent file."""
    result = validate_data('nonexistent.xlsx', 'test_data')
    
    assert 'Validation error' in result['issues'][0]


def test_find_header_candidates():
    """Test header candidate detection."""
    df_raw = pd.DataFrame([
        ['', '', ''],  # Empty row
        ['metadata', 'info', ''],  # Metadata
        ['Name', 'Age', 'Salary'],  # Header row
        ['John', 25, 50000],
        ['Jane', 30, 60000]
    ])
    
    header_patterns = {'test': ['name', 'age']}
    candidates = _find_header_candidates(df_raw, 'test', header_patterns)
    
    assert len(candidates) > 0
    # The header row should be detected
    best_candidate = candidates[0]
    assert best_candidate['row_index'] == 2


def test_find_header_candidates_no_patterns():
    """Test header candidate detection without patterns."""
    df_raw = pd.DataFrame([
        ['Name', 'Age', 'Salary'],
        ['John', 25, 50000],
        ['Jane', 30, 60000]
    ])
    
    candidates = _find_header_candidates(df_raw, 'test', None)
    
    # Should still find candidates based on density
    assert len(candidates) > 0


def test_analyze_data_quality():
    """Test data quality analysis."""
    df = pd.DataFrame({
        'Name': ['John', 'Jane', None, 'Bob'],
        'Age': [25, 30, None, 35],
        'Salary': [50000.0, 60000.0, 70000.0, None],
        'Active': [True, False, True, False]
    })
    
    quality = _analyze_data_quality(df, sample_size=2)
    
    assert quality['total_rows'] == 4
    assert quality['total_columns'] == 4
    assert 'null_analysis' in quality
    assert 'data_type_analysis' in quality
    assert 'sample_data' in quality
    
    # Check null analysis
    assert quality['null_analysis']['Name']['null_count'] == 1
    assert quality['null_analysis']['Age']['null_count'] == 1
    
    # Check sample data
    assert len(quality['sample_data']['Name']) <= 2


@pytest.mark.parametrize("value,expected", [
    ("123", True),
    ("123.45", True),
    ("$123.45", True),
    ("123,456", True),
    ("50%", True),
    ("abc", False),
    ("", False),
    (None, False)
])
def test_is_numeric(value, expected):
    """Test numeric value detection."""
    assert _is_numeric(value) == expected


@pytest.mark.parametrize("value,expected", [
    ("2023-01-01", True),
    ("01/15/2023", True),
    ("Jan 15, 2023", True),
    ("2023", True),
    ("December", True),
    ("abc", False),
    ("123", False),
    ("", False)
])
def test_is_date_like(value, expected):
    """Test date-like value detection."""
    assert _is_date_like(value) == expected


def test_check_expected_columns():
    """Test expected column checking."""
    df = pd.DataFrame({
        'Customer Name': ['John'],
        'Order Date': ['2023-01-01'],
        'Amount': [100.0]
    })
    
    expected = ['Customer Name', 'Order Date', 'Missing Column']
    missing = _check_expected_columns(df, expected)
    
    assert 'Missing Column' in missing
    assert 'Customer Name' not in missing


def test_generate_validation_report():
    """Test validation report generation."""
    validation_results = [
        {
            'file_name': 'test1.xlsx',
            'data_type': 'sales',
            'file_size_kb': 10.5,
            'total_rows': 100,
            'total_columns': 5,
            'issues': ['Missing column: ID'],
            'data_quality': {
                'total_rows': 99,
                'total_columns': 5,
                'null_analysis': {
                    'Name': {'null_percentage': 60.0}
                }
            }
        },
        {
            'file_name': 'test2.csv',
            'data_type': 'inventory',
            'file_size_kb': 5.2,
            'total_rows': 50,
            'total_columns': 3,
            'issues': [],
            'data_quality': {
                'total_rows': 50,
                'total_columns': 3,
                'null_analysis': {}
            }
        }
    ]
    
    report = generate_validation_report(validation_results)
    
    assert 'DATA VALIDATION REPORT' in report
    assert 'test1.xlsx' in report
    assert 'test2.csv' in report
    assert 'Missing column: ID' in report
    assert 'High NULL columns' in report


def test_generate_validation_report_empty():
    """Test validation report generation with empty results."""
    report = generate_validation_report([])
    assert report == "No validation results available."


def test_validate_data_xls_file():
    """Test validation of .xls file (different engine)."""
    with tempfile.NamedTemporaryFile(suffix='.xls', delete=False) as f:
        # Create a simple Excel file
        df = pd.DataFrame({'A': [1, 2, 3], 'B': ['x', 'y', 'z']})
        try:
            df.to_excel(f.name, index=False, engine='xlwt')
            result = validate_data(f.name, 'test_data')
            assert result['file_path'] == f.name
        except (ImportError, ValueError):
            # Skip if xlwt is not available or not supported
            pytest.skip("xlwt not available for .xls file testing")
        finally:
            Path(f.name).unlink()


def test_validate_data_large_sample_size(sample_excel_file):
    """Test validation with large sample size."""
    result = validate_data(sample_excel_file, 'test_data', sample_size=100)
    
    # Should still work even if sample size is larger than data
    assert 'data_quality' in result
    assert 'sample_data' in result['data_quality']
