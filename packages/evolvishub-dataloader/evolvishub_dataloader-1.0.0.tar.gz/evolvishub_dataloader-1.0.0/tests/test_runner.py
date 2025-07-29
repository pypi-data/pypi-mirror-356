"""Comprehensive test runner for the evolvishub-dataloader project."""

import pytest
import sys
import os
from pathlib import Path

def run_all_tests():
    """Run all tests with comprehensive coverage reporting."""
    
    # Add the project root to Python path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    
    # Test configuration
    test_args = [
        'tests/',  # Test directory
        '-v',      # Verbose output
        '--tb=short',  # Short traceback format
        '--strict-markers',  # Strict marker checking
        '--disable-warnings',  # Disable warnings for cleaner output
        '-x',      # Stop on first failure (optional)
    ]
    
    # Add coverage if available
    try:
        import coverage
        test_args.extend([
            '--cov=src',  # Coverage for src directory
            '--cov-report=term-missing',  # Show missing lines
            '--cov-report=html:htmlcov',  # HTML coverage report
            '--cov-fail-under=80',  # Fail if coverage below 80%
        ])
        print("Running tests with coverage reporting...")
    except ImportError:
        print("Coverage not available. Install with: pip install pytest-cov")
        print("Running tests without coverage...")
    
    # Run the tests
    exit_code = pytest.main(test_args)
    
    if exit_code == 0:
        print("\n✅ All tests passed!")
        if 'coverage' in locals():
            print("📊 Coverage report generated in htmlcov/index.html")
    else:
        print(f"\n❌ Tests failed with exit code: {exit_code}")
    
    return exit_code

def run_specific_module(module_name):
    """Run tests for a specific module."""
    test_file = f"tests/test_{module_name}.py"
    
    if not Path(test_file).exists():
        print(f"❌ Test file not found: {test_file}")
        return 1
    
    test_args = [
        test_file,
        '-v',
        '--tb=short'
    ]
    
    print(f"Running tests for {module_name}...")
    exit_code = pytest.main(test_args)
    
    if exit_code == 0:
        print(f"✅ All tests passed for {module_name}!")
    else:
        print(f"❌ Tests failed for {module_name} with exit code: {exit_code}")
    
    return exit_code

def list_available_tests():
    """List all available test modules."""
    tests_dir = Path("tests")
    test_files = list(tests_dir.glob("test_*.py"))
    
    print("Available test modules:")
    for test_file in sorted(test_files):
        module_name = test_file.stem.replace("test_", "")
        print(f"  - {module_name}")
    
    return test_files

def check_test_dependencies():
    """Check if all required test dependencies are available."""
    required_packages = [
        'pytest',
        'pytest-asyncio',
        'pandas',
        'openpyxl',
        'xlrd'
    ]
    
    optional_packages = [
        'pytest-cov',
        'xlwt'
    ]
    
    missing_required = []
    missing_optional = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_required.append(package)
    
    for package in optional_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_optional.append(package)
    
    if missing_required:
        print("❌ Missing required packages:")
        for package in missing_required:
            print(f"  - {package}")
        print("\nInstall with: pip install " + " ".join(missing_required))
        return False
    
    if missing_optional:
        print("⚠️  Missing optional packages (tests will still run):")
        for package in missing_optional:
            print(f"  - {package}")
        print("\nInstall with: pip install " + " ".join(missing_optional))
    
    print("✅ All required test dependencies are available!")
    return True

def run_integration_tests():
    """Run integration tests that test multiple components together."""
    integration_tests = [
        'tests/test_generic_data_loader.py',
        'tests/test_specific_loaders.py'
    ]
    
    test_args = integration_tests + [
        '-v',
        '--tb=short',
        '-k', 'not unit'  # Exclude unit tests if marked
    ]
    
    print("Running integration tests...")
    exit_code = pytest.main(test_args)
    
    if exit_code == 0:
        print("✅ All integration tests passed!")
    else:
        print(f"❌ Integration tests failed with exit code: {exit_code}")
    
    return exit_code

def run_unit_tests():
    """Run unit tests for individual components."""
    unit_test_files = [
        'tests/test_logger.py',
        'tests/test_config_manager.py',
        'tests/test_data_validation.py',
        'tests/test_sqlite_adapter.py'
    ]
    
    test_args = unit_test_files + [
        '-v',
        '--tb=short'
    ]
    
    print("Running unit tests...")
    exit_code = pytest.main(test_args)
    
    if exit_code == 0:
        print("✅ All unit tests passed!")
    else:
        print(f"❌ Unit tests failed with exit code: {exit_code}")
    
    return exit_code

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test runner for evolvishub-dataloader")
    parser.add_argument(
        'command',
        choices=['all', 'unit', 'integration', 'list', 'check', 'module'],
        help='Test command to run'
    )
    parser.add_argument(
        '--module',
        help='Specific module to test (use with "module" command)'
    )
    
    args = parser.parse_args()
    
    if args.command == 'check':
        check_test_dependencies()
    elif args.command == 'list':
        list_available_tests()
    elif args.command == 'all':
        if check_test_dependencies():
            exit_code = run_all_tests()
            sys.exit(exit_code)
    elif args.command == 'unit':
        if check_test_dependencies():
            exit_code = run_unit_tests()
            sys.exit(exit_code)
    elif args.command == 'integration':
        if check_test_dependencies():
            exit_code = run_integration_tests()
            sys.exit(exit_code)
    elif args.command == 'module':
        if not args.module:
            print("❌ Please specify a module name with --module")
            sys.exit(1)
        if check_test_dependencies():
            exit_code = run_specific_module(args.module)
            sys.exit(exit_code)
