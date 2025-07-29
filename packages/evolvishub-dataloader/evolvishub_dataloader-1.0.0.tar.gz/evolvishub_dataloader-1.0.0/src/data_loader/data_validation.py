"""
Generic data validation utility to check for NULL values and data quality issues.
"""
import logging
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime

logger = logging.getLogger(__name__)

def validate_data(
    file_path: str,
    data_type: str,
    expected_columns: Optional[List[str]] = None,
    header_patterns: Optional[Dict[str, List[str]]] = None,
    max_header_search_rows: int = 20,
    min_header_score: float = 0.3,
    sample_size: int = 5
) -> Dict[str, Any]:
    """
    Generic function to validate data quality and identify issues in various file formats.
    
    Args:
        file_path (str): Path to the file to validate
        data_type (str): Type of data (e.g., 'sales', 'inventory', 'orders')
        expected_columns (List[str], optional): List of expected column names
        header_patterns (Dict[str, List[str]], optional): Dictionary mapping data types to expected header patterns
        max_header_search_rows (int): Maximum number of rows to search for header
        min_header_score (float): Minimum score threshold for header detection
        sample_size (int): Number of sample values to include in analysis
        
    Returns:
        Dict containing validation results
    """
    try:
        logger.info(f"🔍 VALIDATING FILE: {Path(file_path).name}")
        
        # Determine engine based on file extension
        file_ext = Path(file_path).suffix.lower()
        if file_ext == '.xls':
            engine = 'xlrd'
        elif file_ext == '.xlsx':
            engine = 'openpyxl'
        elif file_ext == '.csv':
            engine = 'python'
        else:
            engine = None
            
        # Read raw file
        if file_ext == '.csv':
            df_raw = pd.read_csv(file_path, header=None)
        else:
            df_raw = pd.read_excel(file_path, engine=engine, header=None)
            
        validation_result = {
            'file_path': file_path,
            'file_name': Path(file_path).name,
            'data_type': data_type,
            'timestamp': datetime.now().isoformat(),
            'file_size_kb': Path(file_path).stat().st_size / 1024,
            'total_rows': len(df_raw),
            'total_columns': len(df_raw.columns),
            'issues': [],
            'warnings': [],
            'data_quality': {}
        }
        
        # Check for completely empty file
        if df_raw.empty:
            validation_result['issues'].append("File is completely empty")
            return validation_result
            
        # Analyze raw data structure
        logger.info(f"📊 Raw file analysis:")
        logger.info(f"   - Total rows: {len(df_raw)}")
        logger.info(f"   - Total columns: {len(df_raw.columns)}")
        
        # Find potential header row
        header_candidates = _find_header_candidates(
            df_raw, 
            data_type, 
            header_patterns, 
            max_header_search_rows,
            min_header_score
        )
        validation_result['header_candidates'] = header_candidates
        
        if not header_candidates:
            validation_result['issues'].append("No valid header row found")
            return validation_result
            
        # Use the best header candidate
        best_header = header_candidates[0]
        logger.info(f"🎯 Using header row {best_header['row_index']}: {best_header['columns'][:5]}...")
        
        # Read with proper header
        if file_ext == '.csv':
            df = pd.read_csv(file_path, header=best_header['row_index'])
        else:
            df = pd.read_excel(file_path, engine=engine, header=best_header['row_index'])
            
        # Analyze data quality
        validation_result['data_quality'] = _analyze_data_quality(df, sample_size)
        
        # Check for expected columns
        if expected_columns:
            missing_cols = _check_expected_columns(df, expected_columns)
            if missing_cols:
                validation_result['issues'].append(f"Missing expected columns: {missing_cols}")
                
        # Log summary
        logger.info(f"✅ Validation complete for {Path(file_path).name}")
        logger.info(f"   - Data rows after header: {len(df)}")
        logger.info(f"   - Columns found: {len(df.columns)}")
        logger.info(f"   - Issues found: {len(validation_result['issues'])}")
        logger.info(f"   - Warnings: {len(validation_result['warnings'])}")
        
        return validation_result
        
    except Exception as e:
        logger.error(f"❌ Validation failed for {file_path}: {str(e)}")
        return {
            'file_path': file_path,
            'file_name': Path(file_path).name,
            'data_type': data_type,
            'timestamp': datetime.now().isoformat(),
            'issues': [f"Validation error: {str(e)}"],
            'warnings': [],
            'data_quality': {}
        }

def _find_header_candidates(
    df_raw: pd.DataFrame,
    data_type: str,
    header_patterns: Optional[Dict[str, List[str]]] = None,
    max_rows: int = 20,
    min_score: float = 0.3
) -> List[Dict]:
    """Find potential header rows based on data type and patterns."""
    candidates = []
    
    # Get patterns for the current data type
    expected_patterns = header_patterns.get(data_type, []) if header_patterns else []
    
    for idx in range(min(max_rows, len(df_raw))):
        row = df_raw.iloc[idx]
        row_values = [str(val).lower().strip() for val in row if pd.notna(val)]
        
        if len(row_values) < 3:  # Skip rows with too few values
            continue
            
        # Count matches with expected patterns
        matches = sum(1 for pattern in expected_patterns 
                     if any(pattern in val for val in row_values))
        
        # Calculate score
        non_null_count = row.count()
        pattern_score = matches / len(expected_patterns) if expected_patterns else 0
        density_score = non_null_count / len(row)
        
        if expected_patterns:
            total_score = (pattern_score * 0.7) + (density_score * 0.3)
        else:
            total_score = density_score  # Use density only if no patterns
        
        if total_score > min_score:
            candidates.append({
                'row_index': idx,
                'columns': row_values,
                'non_null_count': non_null_count,
                'pattern_matches': matches,
                'score': total_score
            })
    
    # Sort by score
    candidates.sort(key=lambda x: x['score'], reverse=True)
    return candidates

def _analyze_data_quality(df: pd.DataFrame, sample_size: int = 5) -> Dict[str, Any]:
    """Analyze data quality metrics."""
    quality_metrics = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'columns': list(df.columns),
        'null_analysis': {},
        'data_type_analysis': {},
        'sample_data': {}
    }
    
    # Analyze each column
    for col in df.columns:
        col_data = df[col]
        
        # NULL analysis
        null_count = col_data.isnull().sum()
        null_percentage = (null_count / len(col_data)) * 100
        
        quality_metrics['null_analysis'][col] = {
            'null_count': int(null_count),
            'null_percentage': round(null_percentage, 2),
            'non_null_count': int(len(col_data) - null_count)
        }
        
        # Data type analysis
        non_null_data = col_data.dropna()
        if len(non_null_data) > 0:
            # Sample values
            sample_values = non_null_data.head(sample_size).tolist()
            quality_metrics['sample_data'][col] = [str(val) for val in sample_values]
            
            # Infer data type
            if non_null_data.dtype == 'object':
                # Try to determine if it's numeric, date, or text
                numeric_count = sum(1 for val in non_null_data.head(10) 
                                  if _is_numeric(str(val)))
                date_count = sum(1 for val in non_null_data.head(10) 
                               if _is_date_like(str(val)))
                
                if numeric_count > 7:
                    inferred_type = 'numeric_as_text'
                elif date_count > 7:
                    inferred_type = 'date_as_text'
                else:
                    inferred_type = 'text'
            else:
                inferred_type = str(non_null_data.dtype)
                
            quality_metrics['data_type_analysis'][col] = {
                'pandas_dtype': str(col_data.dtype),
                'inferred_type': inferred_type,
                'unique_values': int(non_null_data.nunique()),
                'avg_length': round(non_null_data.astype(str).str.len().mean(), 2) if len(non_null_data) > 0 else 0
            }
    
    # Always include 'sample_data' even if empty
    if 'sample_data' not in quality_metrics:
        quality_metrics['sample_data'] = {}
    
    return quality_metrics

def _is_numeric(value: str) -> bool:
    """Check if a string value is numeric."""
    try:
        float(str(value).replace(',', '').replace('$', '').replace('%', ''))
        return True
    except (ValueError, TypeError):
        return False

def _is_date_like(value: str) -> bool:
    """Check if a string value looks like a date."""
    date_indicators = ['-', '/', '\\', ':', 'jan', 'feb', 'mar', 'apr', 'may', 'jun',
                      'jul', 'aug', 'sep', 'oct', 'nov', 'dec', '2020', '2021', '2022', '2023', '2024']
    value_lower = str(value).lower()
    return any(indicator in value_lower for indicator in date_indicators)

def _check_expected_columns(df: pd.DataFrame, expected_columns: List[str]) -> List[str]:
    """Check for missing expected columns."""
    return [col for col in expected_columns 
            if not any(col.lower() in str(df_col).lower() for df_col in df.columns)]

def generate_validation_report(validation_results: List[Dict[str, Any]]) -> str:
    """Generate a comprehensive validation report."""
    if not validation_results:
        return "No validation results available."
        
    report = ["🔍 DATA VALIDATION REPORT", "=" * 50, ""]
    
    for result in validation_results:
        report.append(f"📁 FILE: {result['file_name']}")
        report.append(f"   Type: {result['data_type']}")
        report.append(f"   Size: {result.get('file_size_kb', 0):.1f} KB")
        report.append(f"   Rows: {result.get('total_rows', 0)}")
        report.append(f"   Columns: {result.get('total_columns', 0)}")
        
        if result.get('issues'):
            report.append(f"   ❌ Issues: {len(result['issues'])}")
            for issue in result['issues']:
                report.append(f"      - {issue}")
                
        if result.get('data_quality'):
            dq = result['data_quality']
            report.append(f"   📊 Data Quality:")
            report.append(f"      - Data rows: {dq.get('total_rows', 0)}")
            report.append(f"      - Columns: {dq.get('total_columns', 0)}")
            
            # Show columns with high NULL percentages
            null_analysis = dq.get('null_analysis', {})
            high_null_cols = [(col, data['null_percentage']) 
                             for col, data in null_analysis.items() 
                             if data['null_percentage'] > 50]
            
            if high_null_cols:
                report.append(f"      - High NULL columns:")
                for col, pct in high_null_cols:
                    report.append(f"        * {col}: {pct}% NULL")
                    
        report.append("")
        
    return "\n".join(report) 