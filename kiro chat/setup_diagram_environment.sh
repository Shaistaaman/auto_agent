#!/bin/bash

# Setup Script for DevOps Architecture Diagram Generation
# This script creates a virtual environment and installs all dependencies

set -e  # Exit on any error

echo "🚀 Setting up DevOps Architecture Diagram Environment..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first:"
    echo "   brew install python3"
    exit 1
fi

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew is not installed. Please install Homebrew first:"
    echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

# Install Graphviz (required for diagrams library)
echo "📦 Installing Graphviz..."
if ! command -v dot &> /dev/null; then
    brew install graphviz
    echo "✅ Graphviz installed successfully"
else
    echo "✅ Graphviz already installed"
fi

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Removing old one..."
    rm -rf venv
fi

python3 -m venv venv
echo "✅ Virtual environment created"

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install required packages
echo "📦 Installing required packages..."
pip install diagrams

echo "✅ All packages installed successfully!"

# Verify installation
echo "🔍 Verifying installation..."
python -c "import diagrams; print('✅ Diagrams library imported successfully')"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "To generate architecture diagrams:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the diagram generator: python generate_devops_architecture.py"
echo "3. Deactivate when done: deactivate"
echo ""
echo "📁 Generated diagrams will be saved as PNG files in the current directory."