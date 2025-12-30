#!/bin/bash

# Test Runner Script for Autonomous Multi-Agent Red/Blue Team Simulation System
# This script runs various test suites and generates reports

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

# Set up environment
setup_env() {
    print_header "Setting Up Test Environment"
    
    # Activate virtual environment if it exists
    if [ -d "venv" ]; then
        print_status "Activating virtual environment..."
        source venv/bin/activate
    else
        print_error "Virtual environment not found. Please run 'scripts/setup.sh' first."
        exit 1
    fi
    
    # Set PYTHONPATH
    export PYTHONPATH="${PYTHONPATH}:."
    
    print_status "Environment setup completed"
}

# Run unit tests
run_unit_tests() {
    print_header "Running Unit Tests"
    
    print_status "Running unit test suite..."
    pytest tests/test_scenarios.py tests/test_basic_functionality.py -v --tb=short
    
    if [ $? -eq 0 ]; then
        print_status "✅ Unit tests passed!"
        return 0
    else
        print_error "❌ Unit tests failed!"
        return 1
    fi
}

# Run integration tests
run_integration_tests() {
    print_header "Running Integration Tests"
    
    print_status "Running integration test suite..."
    pytest tests/test_config.py -v --tb=short
    
    if [ $? -eq 0 ]; then
        print_status "✅ Integration tests passed!"
        return 0
    else
        print_error "❌ Integration tests failed!"
        return 1
    fi
}

# Run all tests
run_all_tests() {
    print_header "Running All Tests"
    
    print_status "Running complete test suite..."
    pytest tests/ -v --tb=short
    
    if [ $? -eq 0 ]; then
        print_status "✅ All tests passed!"
        return 0
    else
        print_error "❌ Some tests failed!"
        return 1
    fi
}

# Run tests with coverage
run_coverage_tests() {
    print_header "Running Tests with Coverage"
    
    print_status "Running test suite with coverage..."
    pytest tests/ -v --tb=short \
        --cov=agents \
        --cov=orchestration \
        --cov=utils \
        --cov=scenarios \
        --cov=dashboard \
        --cov=mcp_servers \
        --cov-report=html \
        --cov-report=term-missing \
        --cov-report=xml
    
    if [ $? -eq 0 ]; then
        print_status "✅ Tests with coverage passed!"
        print_status "Coverage report generated in htmlcov/"
        return 0
    else
        print_error "❌ Tests with coverage failed!"
        return 1
    fi
}

# Run performance tests
run_performance_tests() {
    print_header "Running Performance Tests"
    
    print_status "Running performance test suite..."
    
    # Check if pytest-benchmark is installed
    if ! python -c "import pytest_benchmark" 2>/dev/null; then
        print_warning "pytest-benchmark not installed. Installing..."
        pip install pytest-benchmark
    fi
    
    pytest --benchmark-only tests/ --benchmark-json=benchmark.json
    
    if [ $? -eq 0 ]; then
        print_status "✅ Performance tests completed!"
        print_status "Benchmark results saved to benchmark.json"
        return 0
    else
        print_error "❌ Performance tests failed!"
        return 1
    fi
}

# Run security tests
run_security_tests() {
    print_header "Running Security Tests"
    
    print_status "Running security test suite..."
    
    # Check if bandit is installed
    if ! python -c "import bandit" 2>/dev/null; then
        print_warning "bandit not installed. Installing..."
        pip install bandit
    fi
    
    # Run security scan
    bandit -r agents/ orchestration/ utils/ scenarios/ dashboard/ mcp_servers/ -f json -o security-report.json
    
    # Check if safety is installed
    if ! python -c "import safety" 2>/dev/null; then
        print_warning "safety not installed. Installing..."
        pip install safety
    fi
    
    # Run dependency vulnerability scan
    safety check --json --output safety-report.json
    
    print_status "✅ Security tests completed!"
    print_status "Security reports generated:"
    print_status "  - security-report.json (bandit)"
    print_status "  - safety-report.json (safety)"
    return 0
}

# Run validation tests
run_validation_tests() {
    print_header "Running Validation Tests"
    
    print_status "Running validation test suite..."
    
    # Run standalone validation
    python -c "
import sys
sys.path.insert(0, '.')
from utils.validation_standalone import check_system_health
check_system_health()
"
    
    if [ $? -eq 0 ]; then
        print_status "✅ Validation tests passed!"
        return 0
    else
        print_error "❌ Validation tests failed!"
        return 1
    fi
}

# Generate test report
generate_report() {
    print_header "Generating Test Report"
    
    # Create reports directory if it doesn't exist
    mkdir -p reports
    
    # Generate HTML test report
    if [ -f "htmlcov/index.html" ]; then
        cp -r htmlcov/* reports/
        print_status "HTML coverage report copied to reports/"
    fi
    
    # Generate JSON summary
    python -c "
import json
import subprocess
import sys
from datetime import datetime

# Get test results
result = subprocess.run(['pytest', '--collect-only', 'tests/'], 
                      capture_output=True, text=True, cwd='.')
test_count = result.stdout.count('collected')

# Get coverage info
coverage_data = {}
if [ -f 'htmlcov/index.html' ]; then
    coverage_data['coverage_available'] = True
else
    coverage_data['coverage_available'] = False

# Get security info
security_data = {}
if [ -f 'security-report.json' ]; then
    with open('security-report.json', 'r') as f:
        security_data = json.load(f)
else
    security_data['security_scan_completed'] = False

# Create summary report
report = {
    'timestamp': datetime.now().isoformat(),
    'test_count': test_count,
    'coverage': coverage_data,
    'security': security_data,
    'status': 'completed'
}

with open('reports/test-summary.json', 'w') as f:
    json.dump(report, f, indent=2)

print(f'Test summary generated: reports/test-summary.json')
"
    
    print_status "Test report generated in reports/"
    return 0
}

# Clean up test artifacts
cleanup() {
    print_header "Cleaning Up Test Artifacts"
    
    # Remove cache files
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    find . -name "*.pyo" -delete 2>/dev/null || true
    find . -name "*.pyd" -delete 2>/dev/null || true
    
    # Remove pytest cache
    rm -rf .pytest_cache 2>/dev/null || true
    
    # Remove coverage files
    rm -f .coverage 2>/dev/null || true
    rm -rf htmlcov 2>/dev/null || true
    
    # Remove test results
    rm -f test-results/*.xml 2>/dev/null || true
    rm -f test-results/*.html 2>/dev/null || true
    
    print_status "Test artifacts cleaned up"
}

# Show help
show_help() {
    echo "Test Runner Script for Autonomous Multi-Agent Red/Blue Team Simulation System"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help          Show this help message"
    echo "  -u, --unit          Run unit tests only"
    echo "  -i, --integration    Run integration tests only"
    echo "  -a, --all           Run all tests"
    echo "  -c, --coverage      Run tests with coverage"
    echo "  -p, --performance   Run performance tests"
    echo "  -s, --security      Run security tests"
    echo "  -v, --validation    Run validation tests"
    echo "  -r, --report        Generate test report"
    -  --clean           Clean up test artifacts"
    echo ""
    echo "Examples:"
    echo "  $0                  Run all tests"
    echo "  $0 --unit          Run unit tests"
    echo "  $0 --coverage      Run tests with coverage"
    echo "  $0 --security      Run security tests"
    echo "  $0 --clean          Clean up test artifacts"
    echo ""
    echo "Environment variables:"
    echo "  PYTHONPATH         Python path for imports"
    echo "  COVERAGE_FILE       Coverage file path"
    echo "  TEST_DATABASE_URL   Test database URL"
}

# Main function
main() {
    # Set up environment
    setup_env
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -u|--unit)
                run_unit_tests
                exit $?
                ;;
            -i|--integration)
                run_integration_tests
                exit $?
                ;;
            -a|--all)
                run_all_tests
                exit $?
                ;;
            -c|--coverage)
                run_coverage_tests
                exit $?
                ;;
            -p|--performance)
                run_performance_tests
                exit $?
                ;;
            -s|--security)
                run_security_tests
                exit $?
                ;;
            -v|--validation)
                run_validation_tests
                exit $?
                ;;
            -r|--report)
                generate_report
                exit $?
                ;;
            --clean)
                cleanup
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
        shift
    done
    
    # Default: run all tests
    run_all_tests
    generate_report
}

# Run main function
main "$@"
