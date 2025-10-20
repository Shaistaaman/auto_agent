# DevOps Architecture Diagram Generation

This directory contains scripts to generate professional architecture diagrams for the Autonomous DevOps Incident Responder project.

## Quick Start

### 1. One-time Setup

```bash
# Make scripts executable
chmod +x setup_diagram_environment.sh
chmod +x run_diagram_generator.sh

# Run setup (installs dependencies)
./setup_diagram_environment.sh
```

### 2. Generate Diagrams

```bash
# Generate all architecture diagrams
./run_diagram_generator.sh
```

### 3. View Results

```bash
# Open all generated diagrams
open *.png
```

## Manual Setup (Alternative)

If the automated scripts don't work, follow these manual steps:

### Step 1: Install System Dependencies

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Graphviz
brew install graphviz

# Install Python 3 (if not installed)
brew install python3
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install diagrams library
pip install diagrams
```

### Step 3: Generate Diagrams

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the generator
python generate_devops_architecture.py

# Deactivate when done
deactivate
```

## Generated Diagrams

The script generates 4 professional architecture diagrams:

### 1. **Detailed Architecture** (`devops_incident_responder_detailed.png`)

- Comprehensive system architecture
- All components and data flows
- Perfect for technical documentation

### 2. **Simplified Architecture** (`devops_incident_responder_simplified.png`)

- High-level overview
- Clean, presentation-ready
- Ideal for executive summaries and demos

### 3. **Compliance Architecture** (`devops_incident_responder_compliance.png`)

- Highlights hackathon requirements
- Shows all required AWS services
- Perfect for submission documentation

### 4. **Cost Comparison** (`devops_incident_responder_costs.png`)

- Visual cost analysis
- Shows 40-52% savings
- Great for business case presentations

## Troubleshooting

### Common Issues

#### 1. "pip: command not found"

```bash
# Install Python 3 and pip
brew install python3
```

#### 2. "dot: command not found"

```bash
# Install Graphviz
brew install graphviz
```

#### 3. "Permission denied"

```bash
# Make scripts executable
chmod +x *.sh
```

#### 4. "Virtual environment activation failed"

```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

#### 5. "Import error: No module named 'diagrams'"

```bash
# Activate virtual environment and reinstall
source venv/bin/activate
pip install --upgrade pip
pip install diagrams
```

### Verification Commands

```bash
# Check Python installation
python3 --version

# Check Graphviz installation
dot -V

# Check virtual environment
source venv/bin/activate
python -c "import diagrams; print('✅ Ready to generate diagrams!')"
```

## File Structure

```
.
├── setup_diagram_environment.sh    # One-time setup script
├── run_diagram_generator.sh        # Diagram generation script
├── generate_devops_architecture.py # Main generator code
├── README_DIAGRAMS.md              # This file
├── venv/                           # Virtual environment (created by setup)
└── *.png                          # Generated diagram files
```

## Customization

To modify the diagrams:

1. Edit `generate_devops_architecture.py`
2. Modify colors, labels, or components as needed
3. Run `./run_diagram_generator.sh` to regenerate

## For Hackathon Submission

These diagrams are specifically designed for the AWS AI Agent Global Hackathon:

- ✅ **Professional Quality**: Publication-ready diagrams
- ✅ **Compliance Focused**: Highlights all required services
- ✅ **Multiple Perspectives**: Technical, business, and compliance views
- ✅ **Cost Optimized**: Shows significant cost savings

Perfect for your hackathon submission package! 🏆
