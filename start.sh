#!/bin/bash

# Vocab Analyzer Web Server Startup Script
# This script activates the virtual environment and starts the Flask web server

echo "======================================================================"
echo "  📚 Vocabulary Analyzer - Web Interface"
echo "======================================================================"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found!"
    echo "   Please run: python3 -m venv venv"
    echo "   Then install dependencies: pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import flask" 2>/dev/null; then
    echo "❌ Error: Flask not installed!"
    echo "   Please run: pip install -r requirements.txt"
    exit 1
fi

echo "✅ Environment ready"
echo ""
echo "🚀 Starting web server..."
echo "   Server will be available at: http://127.0.0.1:5000"
echo ""
echo "   Press CTRL+C to stop the server"
echo "======================================================================"
echo ""

# Start the Flask application
python -m vocab_analyzer.web.app
