#!/bin/bash

# Run Script for DevOps Architecture Diagram Generation
# This script activates the virtual environment and generates all diagrams

set -e  # Exit on any error

echo "🎨 Generating DevOps Architecture Diagrams..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   chmod +x setup_diagram_environment.sh"
    echo "   ./setup_diagram_environment.sh"
    exit 1
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if the generator script exists and run the most compatible version
if [ -f "generate_devops_architecture_minimal.py" ]; then
    echo "🚀 Running minimal diagram generator (maximum compatibility)..."
    python generate_devops_architecture_minimal.py
elif [ -f "generate_devops_architecture_fixed.py" ]; then
    echo "🚀 Running fixed diagram generator..."
    python generate_devops_architecture_fixed.py
elif [ -f "generate_devops_architecture.py" ]; then
    echo "🚀 Running original diagram generator..."
    python generate_devops_architecture.py
else
    echo "❌ No diagram generator script found in current directory"
    exit 1
fi

# List generated files
echo ""
echo "📁 Generated files:"
ls -la *.png 2>/dev/null || echo "No PNG files found - check for errors above"

echo ""
echo "✅ Diagram generation completed!"
echo "💡 To view diagrams: open *.png"
echo "🔄 To deactivate virtual environment: deactivate"