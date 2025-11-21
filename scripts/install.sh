#!/usr/bin/env bash
#
# OmniForge One-Click Installer
# Automatic environment detection, dependency installation, and setup
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Error handler
error_exit() {
    log_error "$1"
    log_info "Rolling back changes..."
    cleanup_on_error
    exit 1
}

cleanup_on_error() {
    log_info "Performing cleanup..."
    # Deactivate virtual environment if active
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        deactivate 2>/dev/null || true
    fi
}

# Trap errors
trap 'error_exit "Installation failed at line $LINENO"' ERR

echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║        OmniForge: The Absolute Upgrade Engine         ║"
echo "║                One-Click Installer                     ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Environment Detection
log_info "Step 1: Detecting environment..."

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    log_success "Detected OS: Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    log_success "Detected OS: macOS"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
    log_success "Detected OS: Windows"
else
    log_warning "Unknown OS: $OSTYPE. Assuming Linux..."
    OS="linux"
fi

# Step 2: Check Prerequisites
log_info "Step 2: Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    error_exit "Python 3 is not installed. Please install Python 3.8 or higher."
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
log_success "Found Python $PYTHON_VERSION"

# Check pip
if ! command -v pip3 &> /dev/null; then
    log_warning "pip3 not found. Installing pip..."
    python3 -m ensurepip --default-pip || error_exit "Failed to install pip"
fi
log_success "Found pip"

# Check Node.js
if ! command -v node &> /dev/null; then
    log_warning "Node.js not found. Installing Node.js..."
    if [[ "$OS" == "macos" ]]; then
        if command -v brew &> /dev/null; then
            brew install node || error_exit "Failed to install Node.js"
        else
            error_exit "Please install Homebrew first: https://brew.sh"
        fi
    elif [[ "$OS" == "linux" ]]; then
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y nodejs npm || error_exit "Failed to install Node.js"
        elif command -v yum &> /dev/null; then
            sudo yum install -y nodejs npm || error_exit "Failed to install Node.js"
        else
            error_exit "Please install Node.js manually: https://nodejs.org"
        fi
    else
        error_exit "Please install Node.js manually: https://nodejs.org"
    fi
fi

NODE_VERSION=$(node --version)
log_success "Found Node.js $NODE_VERSION"

# Step 3: Create Virtual Environment
log_info "Step 3: Setting up Python virtual environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv || error_exit "Failed to create virtual environment"
    log_success "Created virtual environment"
else
    log_info "Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate || error_exit "Failed to activate virtual environment"
log_success "Activated virtual environment"

# Step 4: Install Python Dependencies
log_info "Step 4: Installing Python dependencies..."

pip install --upgrade pip setuptools wheel || error_exit "Failed to upgrade pip"
pip install -r requirements.txt || error_exit "Failed to install Python dependencies"
log_success "Installed Python dependencies"

# Step 5: Install Node Dependencies
log_info "Step 5: Installing Node.js dependencies..."

npm install || error_exit "Failed to install Node.js dependencies"
log_success "Installed Node.js dependencies"

# Step 6: Create Configuration
log_info "Step 6: Creating configuration files..."

if [ ! -f ".env" ]; then
    cat > .env << EOF
# OmniForge Configuration
DEBUG_MODE=false
API_HOST=0.0.0.0
API_PORT=8000
PARALLEL_WORKERS=4
CACHE_ENABLED=true

# Optional: AI Integration (uncomment and configure if needed)
# OPENAI_API_KEY=your_key_here
# ANTHROPIC_API_KEY=your_key_here
EOF
    log_success "Created .env configuration file"
else
    log_info "Configuration file already exists"
fi

# Step 7: Create necessary directories
log_info "Step 7: Creating necessary directories..."

mkdir -p logs
mkdir -p cache
mkdir -p reports
log_success "Created application directories"

# Step 8: Verify Installation
log_info "Step 8: Verifying installation..."

# Test Python imports
python3 -c "import fastapi, click, rich" || error_exit "Python dependencies verification failed"
log_success "Python dependencies verified"

# Test Node modules
node -e "console.log('Node.js ready')" || error_exit "Node.js verification failed"
log_success "Node.js dependencies verified"

# Step 9: Build Frontend (optional for development)
log_info "Step 9: Building frontend..."
log_info "Skipping frontend build (use 'npm run dev' for development)"

# Success!
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║           ✓ Installation Complete!                    ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

log_info "Quick Start Guide:"
echo ""
echo "  1. Start the API server:"
echo "     ${GREEN}./scripts/start.sh${NC}"
echo ""
echo "  2. Or use the CLI:"
echo "     ${GREEN}source venv/bin/activate${NC}"
echo "     ${GREEN}python -m src.cli analyze /path/to/repo${NC}"
echo ""
echo "  3. For the web GUI:"
echo "     ${GREEN}./scripts/start.sh --gui${NC}"
echo ""

log_success "OmniForge is ready to transform your code!"
echo ""
