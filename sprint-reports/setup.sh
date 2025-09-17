#!/bin/bash

# Sprint Reports Automation Setup Script
# This script sets up the environment for automated sprint report generation

set -e

echo "🚀 Setting up Sprint Reports Automation..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "📁 Working directory: $SCRIPT_DIR"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8 or later.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✅ Python 3 found: $PYTHON_VERSION${NC}"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 is not installed. Please install pip.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ pip3 found${NC}"

# Create virtual environment if it doesn't exist
VENV_DIR="$SCRIPT_DIR/venv"
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${BLUE}📦 Creating virtual environment...${NC}"
    python3 -m venv "$VENV_DIR"
else
    echo -e "${GREEN}✅ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}🔧 Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo -e "${BLUE}⬆️ Upgrading pip...${NC}"
pip install --upgrade pip

# Install requirements
echo -e "${BLUE}📥 Installing Python dependencies...${NC}"
pip install -r "$SCRIPT_DIR/requirements.txt"

# Create necessary directories
echo -e "${BLUE}📁 Creating directories...${NC}"
mkdir -p "$SCRIPT_DIR/output"
mkdir -p "$SCRIPT_DIR/logs"

# Set up environment file
ENV_FILE="$SCRIPT_DIR/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo -e "${YELLOW}📝 Creating environment file...${NC}"
    cp "$SCRIPT_DIR/env_template.txt" "$ENV_FILE"
    echo -e "${YELLOW}⚠️  Please edit $ENV_FILE and add your Jira API token${NC}"
    echo -e "${YELLOW}   You can get your API token from: https://id.atlassian.com/manage-profile/security/api-tokens${NC}"
else
    echo -e "${GREEN}✅ Environment file already exists${NC}"
fi

# Make Python scripts executable
echo -e "${BLUE}🔐 Making scripts executable...${NC}"
chmod +x "$SCRIPT_DIR/ai_efficiency_reporter.py"
chmod +x "$SCRIPT_DIR/scheduler.py"

# Test the installation
echo -e "${BLUE}🧪 Testing installation...${NC}"
cd "$SCRIPT_DIR"

# Check if environment file has been configured
if grep -q "your_api_token_here" "$ENV_FILE" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Environment file needs configuration. Skipping connection test.${NC}"
else
    echo -e "${BLUE}🔗 Testing Jira connection...${NC}"
    if python3 ai_efficiency_reporter.py --help > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Script can be executed${NC}"
    else
        echo -e "${RED}❌ Error running script${NC}"
    fi
fi

# Create activation script
ACTIVATE_SCRIPT="$SCRIPT_DIR/activate.sh"
cat > "$ACTIVATE_SCRIPT" << 'EOF'
#!/bin/bash
# Activation script for Sprint Reports environment
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/venv/bin/activate"
cd "$SCRIPT_DIR"
echo "🚀 Sprint Reports environment activated"
echo "Available commands:"
echo "  python3 ai_efficiency_reporter.py        - Generate report manually"
echo "  python3 scheduler.py                     - Run scheduler"
echo "  python3 scheduler.py --test              - Test report generation"
echo "  python3 scheduler.py --check-date        - Check if today is second Monday"
EOF

chmod +x "$ACTIVATE_SCRIPT"

echo ""
echo -e "${GREEN}🎉 Setup completed successfully!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Edit the environment file: $ENV_FILE"
echo "2. Add your Jira API token (get it from: https://id.atlassian.com/manage-profile/security/api-tokens)"
echo "3. Test the setup: cd $SCRIPT_DIR && source activate.sh && python3 ai_efficiency_reporter.py --help"
echo ""
echo -e "${BLUE}To run reports:${NC}"
echo "• Manual report: cd $SCRIPT_DIR && source activate.sh && python3 ai_efficiency_reporter.py"
echo "• Start scheduler: cd $SCRIPT_DIR && source activate.sh && python3 scheduler.py"
echo "• Test generation: cd $SCRIPT_DIR && source activate.sh && python3 scheduler.py --test"
echo ""
echo -e "${YELLOW}Remember: Reports will only be automatically generated on the second Monday of each month!${NC}"
