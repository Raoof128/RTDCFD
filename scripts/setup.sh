#!/bin/bash

# Autonomous Multi-Agent Red/Blue Team Simulation System Setup Script
# This script sets up the development environment for the project

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

# Check if Python is installed
check_python() {
    print_header "Checking Python Installation"
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_status "Python 3 found: $PYTHON_VERSION"
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version | cut -d' ' -f2)
        print_status "Python found: $PYTHON_VERSION"
        PYTHON_CMD="python"
    else
        print_error "Python is not installed. Please install Python 3.8 or higher."
        exit 1
    fi
    
    # Check Python version
    PYTHON_MAJOR=$($PYTHON_CMD -c "import sys; print(sys.version_info[0])")
    PYTHON_MINOR=$($PYTHON_CMD -c "import sys; print(sys.version_info[1])")
    
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
        print_error "Python 3.8 or higher is required. Found: $PYTHON_MAJOR.$PYTHON_MINOR"
        exit 1
    fi
    
    print_status "Python version check passed: $PYTHON_MAJOR.$PYTHON_MINOR"
}

# Create virtual environment
create_venv() {
    print_header "Creating Virtual Environment"
    
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        $PYTHON_CMD -m venv venv
        print_status "Virtual environment created successfully"
    else
        print_warning "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    pip install --upgrade setuptools wheel
}

# Install dependencies
install_dependencies() {
    print_header "Installing Dependencies"
    
    # Install production dependencies
    print_status "Installing production dependencies..."
    pip install -r requirements.txt
    
    # Install development dependencies
    print_status "Installing development dependencies..."
    pip install -r requirements-dev.txt
    
    # Install pre-commit hooks
    print_status "Installing pre-commit hooks..."
    pre-commit install
    
    print_status "All dependencies installed successfully"
}

# Create necessary directories
create_directories() {
    print_header "Creating Directories"
    
    directories=(
        "storage"
        "logs"
        "reports"
        "data"
        "test-results"
        "coverage"
        "htmlcov"
        "monitoring"
        "scripts"
    )
    
    for dir in "${directories[@]}"; do
        if [ ! -d "$dir" ]; then
            print_status "Creating directory: $dir"
            mkdir -p "$dir"
        else
            print_warning "Directory already exists: $dir"
        fi
    done
    
    print_status "All directories created successfully"
}

# Setup environment variables
setup_env() {
    print_header "Setting Up Environment"
    
    if [ ! -f ".env" ]; then
        print_status "Creating .env file from template..."
        cp .env.example .env
        print_warning "Please edit .env file with your ANTHROPIC_API_KEY"
        print_warning "Add your API key: ANTHROPIC_API_KEY=your_key_here"
    else
        print_warning ".env file already exists"
    fi
    
    print_status "Environment setup completed"
}

# Validate installation
validate_installation() {
    print_header "Validating Installation"
    
    # Test Python imports
    print_status "Testing Python imports..."
    python -c "
import sys
sys.path.insert(0, '.')
try:
    import config
    import scenarios
    print('✅ Core modules imported successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
except Exception as e:
    print(f'❌ Unexpected error: {e}')
    sys.exit(1)
"
    
    # Test configuration
    print_status "Testing configuration..."
    python -c "
import sys
sys.path.insert(0, '.')
try:
    from config import settings
    print(f'✅ Configuration loaded successfully')
    print(f'   Model: {settings.anthropic_model}')
    print(f'   Database: {settings.sqlite_db_path}')
except Exception as e:
    print(f'❌ Configuration error: {e}')
    sys.exit(1)
"
    
    # Test scenarios
    print_status "Testing scenarios..."
    python -c "
import sys
sys.path.insert(0, '.')
try:
    from scenarios import get_available_scenarios
    scenarios = get_available_scenarios()
    print(f'✅ Scenarios loaded: {len(scenarios)} scenarios')
    for scenario in scenarios:
        print(f'   - {scenario}')
except Exception as e:
    print(f'❌ Scenarios error: {e}')
    sys.exit(1)
"
    
    print_status "Installation validation completed successfully"
}

# Run tests
run_tests() {
    print_header "Running Tests"
    
    print_status "Running test suite..."
    pytest tests/ -v --tb=short
    
    if [ $? -eq 0 ]; then
        print_status "All tests passed!"
    else
        print_error "Some tests failed!"
        exit 1
    fi
}

# Run code quality checks
run_quality_checks() {
    print_header "Running Code Quality Checks"
    
    # Format code
    print_status "Formatting code with black..."
    black --check agents/ orchestration/ utils/ scenarios/ dashboard/ mcp_servers/ examples/
    
    # Check imports
    print_status "Checking imports with isort..."
    isort --check-only agents/ orchestration/ utils/ scenarios/ dashboard/ mcp_servers/ examples/
    
    # Lint code
    print_status "Linting code with flake8..."
    flake8 agents/ orchestration/ utils/ scenarios/ dashboard/ mcp_servers/ examples/ --max-line-length=88 --extend-ignore=E203,W503,E501
    
    # Type checking
    print_status "Type checking with mypy..."
    mypy agents/ orchestration/ utils/ scenarios/ dashboard/ mcp_servers/ --ignore-missing-imports
    
    # Security scan
    print_status "Security scanning with bandit..."
    bandit -r agents/ orchestration/ utils/ scenarios/ dashboard/ mcp_servers/ -f json -o bandit-report.json
    
    print_status "Code quality checks completed"
}

# Show help
show_help() {
    echo "Autonomous Multi-Agent Red/Blue Team Simulation System Setup Script"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -v, --validate Validate installation only"
    echo "  -t, --test     Run tests only"
    echo "  -q, --quality  Run quality checks only"
    echo "  -c, --clean    Clean up installation"
    echo ""
    echo "Examples:"
    echo "  $0              Full setup"
    echo "  $0 --validate    Validate installation"
    echo "  $0 --test        Run tests"
    echo "  $0 --quality     Run quality checks"
    echo "  $0 --clean       Clean up installation"
}

# Clean up installation
clean_installation() {
    print_header "Cleaning Up Installation"
    
    # Deactivate virtual environment
    if [ -n "$VIRTUAL_ENV" ]; then
        deactivate
    fi
    
    # Remove virtual environment
    if [ -d "venv" ]; then
        print_status "Removing virtual environment..."
        rm -rf venv
    fi
    
    # Remove cache directories
    cache_dirs=(
        "__pycache__"
        ".pytest_cache"
        ".mypy_cache"
        ".coverage"
        "htmlcov"
        ".tox"
        "build"
        "dist"
        "*.egg-info"
    )
    
    for dir in "${cache_dirs[@]}"; do
        if [ -d "$dir" ]; then
            print_status "Removing cache directory: $dir"
            rm -rf "$dir"
        fi
    done
    
    # Remove temporary files
    find . -name "*.pyc" -delete
    find . -name "*.pyo" -delete
    find . -name "*.pyd" -delete
    
    print_status "Installation cleaned up successfully"
}

# Main function
main() {
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -v|--validate)
                validate_installation
                exit 0
                ;;
            -t|--test)
                run_tests
                exit 0
                ;;
            -q|--quality)
                run_quality_checks
                exit 0
                ;;
            -c|--clean)
                clean_installation
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
    
    # Full setup
    print_header "Autonomous Multi-Agent Red/Blue Team Simulation System Setup"
    
    check_python
    create_venv
    install_dependencies
    create_directories
    setup_env
    validate_installation
    run_tests
    run_quality_checks
    
    print_header "Setup Completed Successfully!"
    print_status "🎉 The Autonomous Multi-Agent Red/Blue Team Simulation System is ready to use!"
    print_status ""
    print_status "Next steps:"
    print_status "1. Edit .env file with your ANTHROPIC_API_KEY"
    print_status "2. Run 'python main.py --list-scenarios' to see available scenarios"
    print_status "3. Run 'python main.py --scenario <scenario_name>' to start simulation"
    print_status "4. Run 'streamlit run dashboard/streamlit_ui.py' to start dashboard"
    print_status ""
    print_status "For help, run: $0 --help"
}

# Run main function
main "$@"
