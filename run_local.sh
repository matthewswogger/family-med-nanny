#!/bin/bash


set -e  # Exit on any error

# Configuration
SLACK_FASTAPI_DIR="family_med_nanny"

echo "=========================================="
echo "SCRIPT SETUP AND VALIDATION"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# Check if we're in the right directory
if [ ! -d "$SLACK_FASTAPI_DIR" ]; then
    print_error "$SLACK_FASTAPI_DIR directory not found. Please run this script from the project root."
    exit 1
fi

# Check for .env file
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Please create one with proper credentials."
    exit 1
fi

echo ""
echo "SCRIPT SETUP COMPLETE - STARTING FASTAPI APP"
echo "=========================================="

print_status "Starting FastAPI server in background..."
python $SLACK_FASTAPI_DIR/run.py
