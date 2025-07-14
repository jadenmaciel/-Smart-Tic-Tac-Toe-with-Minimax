#!/usr/bin/env python3
"""
Simple test runner for Smart Tic-Tac-Toe tests.

This script runs all tests without requiring external dependencies like pytest.
It provides basic test discovery and execution functionality.
"""

import sys  # Import system functionality for exit codes and path management
import os  # Import os module for file system operations
import traceback  # Import traceback for detailed error reporting
import importlib.util  # Import utility for dynamic module loading

def load_module_from_file(filepath):
    """
    Load a Python module from a file path.
    
    Args:
        filepath (str): Path to the Python file to load
        
    Returns:
        module: The loaded module object
    """
    # Reason: Load test modules dynamically to run tests without pytest
    # This allows us to discover and execute test functions programmatically
    
    module_name = os.path.basename(filepath).replace('.py', '')  # Extract module name from filename
    spec = importlib.util.spec_from_file_location(module_name, filepath)  # Create module specification
    module = importlib.util.module_from_spec(spec)  # Create module from specification
    spec.loader.exec_module(module)  # Execute the module to load its contents
    return module  # Return the loaded module

def discover_test_files(test_dir):
    """
    Discover all test files in the given directory.
    
    Args:
        test_dir (str): Directory to search for test files
        
    Returns:
        list: List of test file paths
    """
    # Reason: Find all test files automatically for comprehensive test execution
    # This ensures we don't miss any tests when adding new ones
    
    test_files = []  # Initialize list to store test file paths
    
    for filename in os.listdir(test_dir):  # Iterate through all files in test directory
        if filename.startswith('test_') and filename.endswith('.py'):  # Check if file is a test file
            test_files.append(os.path.join(test_dir, filename))  # Add full path to test files list
    
    return test_files  # Return list of discovered test files

def run_test_function(test_func, test_name):
    """
    Run a single test function and report results.
    
    Args:
        test_func (callable): The test function to execute
        test_name (str): Name of the test for reporting
        
    Returns:
        bool: True if test passed, False if failed
    """
    # Reason: Execute individual test functions with proper error handling
    # This provides detailed feedback about test success or failure
    
    try:
        test_func()  # Execute the test function
        print(f"✅ {test_name} - PASSED")  # Report successful test
        return True  # Return success status
    except AssertionError as e:  # Catch assertion failures
        print(f"❌ {test_name} - FAILED: {e}")  # Report assertion failure
        return False  # Return failure status
    except Exception as e:  # Catch any other exceptions
        print(f"💥 {test_name} - ERROR: {e}")  # Report unexpected error
        print(traceback.format_exc())  # Print detailed error traceback
        return False  # Return failure status

def run_tests_in_module(module, module_name):
    """
    Run all test methods in a given module.
    
    Args:
        module: The test module to execute
        module_name (str): Name of the module for reporting
        
    Returns:
        tuple: (passed_count, total_count)
    """
    # Reason: Execute all test methods within a module systematically
    # This handles both function-based and class-based test structures
    
    passed = 0  # Initialize counter for passed tests
    total = 0  # Initialize counter for total tests
    
    print(f"\n🧪 Running tests in {module_name}")  # Print module header
    print("-" * 50)  # Print separator line
    
    # Find and run test functions
    for name in dir(module):  # Iterate through all names in the module
        if name.startswith('test_'):  # Check if name is a test function
            test_func = getattr(module, name)  # Get the actual function object
            if callable(test_func):  # Verify it's actually callable
                total += 1  # Increment total test count
                if run_test_function(test_func, f"{module_name}.{name}"):  # Run the test
                    passed += 1  # Increment passed count if successful
    
    # Find and run test classes
    for name in dir(module):  # Iterate through all names in the module again
        obj = getattr(module, name)  # Get the object
        if (isinstance(obj, type) and name.startswith('Test')):  # Check if it's a test class
            # Get all test methods first
            test_methods = []  # Initialize list for test methods
            for method_name in dir(obj):  # Iterate through class methods
                if method_name.startswith('test_'):  # Check if method is a test
                    test_methods.append(method_name)  # Add to test methods list
            
            # Run each test method with a fresh instance for proper isolation
            for method_name in test_methods:  # Iterate through test methods
                try:
                    test_instance = obj()  # Create fresh instance for each test
                    
                    # Run setup if it exists
                    if hasattr(test_instance, 'setup_method'):  # Check for setup method
                        test_instance.setup_method()  # Run setup before test
                    
                    # Run the specific test method
                    test_method = getattr(test_instance, method_name)  # Get the test method
                    total += 1  # Increment total test count
                    if run_test_function(test_method, f"{module_name}.{name}.{method_name}"):  # Run test
                        passed += 1  # Increment passed count if successful
                    
                    # Run teardown if it exists
                    if hasattr(test_instance, 'teardown_method'):  # Check for teardown method
                        test_instance.teardown_method()  # Run cleanup after test
                        
                except Exception as e:  # Catch any setup/teardown errors
                    print(f"💥 {module_name}.{name}.{method_name} - SETUP/TEARDOWN ERROR: {e}")  # Report error
                    total += 1  # Count as one failed test
    
    return passed, total  # Return test results

def main():
    """Main test runner function."""
    # Reason: Coordinate the entire test execution process
    # This provides a comprehensive test run with summary reporting
    
    print("🚀 Smart Tic-Tac-Toe Test Runner")  # Print header
    print("=" * 50)  # Print main separator
    
    # Add project root to path for imports
    project_root = os.path.dirname(os.path.abspath(__file__))  # Get project directory
    sys.path.insert(0, project_root)  # Add to Python path for imports
    
    # Discover and run tests
    tests_dir = os.path.join(project_root, 'tests')  # Construct tests directory path
    
    if not os.path.exists(tests_dir):  # Check if tests directory exists
        print("❌ Tests directory not found!")  # Report missing tests
        sys.exit(1)  # Exit with error code
    
    test_files = discover_test_files(tests_dir)  # Find all test files
    
    if not test_files:  # Check if any test files were found
        print("⚠️  No test files found!")  # Report no tests
        sys.exit(1)  # Exit with error code
    
    total_passed = 0  # Initialize total passed counter
    total_tests = 0  # Initialize total tests counter
    
    # Run tests in each file
    for test_file in test_files:  # Iterate through all discovered test files
        try:
            module = load_module_from_file(test_file)  # Load the test module
            module_name = os.path.basename(test_file).replace('.py', '')  # Extract module name
            passed, total = run_tests_in_module(module, module_name)  # Run tests in module
            total_passed += passed  # Add to overall passed count
            total_tests += total  # Add to overall test count
        except Exception as e:  # Catch module loading errors
            print(f"💥 Failed to load {test_file}: {e}")  # Report loading error
            print(traceback.format_exc())  # Print detailed error
    
    # Print summary
    print("\n" + "=" * 50)  # Print summary separator
    print(f"📊 Test Results Summary")  # Print summary header
    print(f"✅ Passed: {total_passed}")  # Report passed count
    print(f"❌ Failed: {total_tests - total_passed}")  # Report failed count
    print(f"📈 Total:  {total_tests}")  # Report total count
    
    if total_passed == total_tests:  # Check if all tests passed
        print("🎉 All tests passed!")  # Celebrate success
        sys.exit(0)  # Exit with success code
    else:
        print("💔 Some tests failed!")  # Report failures
        sys.exit(1)  # Exit with error code

# Reason: Run the test suite when this file is executed directly
# This allows easy execution of all tests with "python3 run_tests.py"
if __name__ == "__main__":
    main()  # Execute the main test runner 