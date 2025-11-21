# OmniForge: The Absolute Upgrade Engine ⚡

<div align="center">

**Next-Generation Repository Analysis and Transformation System**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![Node](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

[Features](#features) • [Quick Start](#quick-start) • [Architecture](#architecture) • [Documentation](#documentation)

</div>

---

## 🚀 Overview

**OmniForge** is a revolutionary code analysis and transformation engine that automatically analyzes repositories, identifies architectural flaws, detects security vulnerabilities, and generates actionable upgrade recommendations. Built with modern architecture, production-grade error handling, and a polished web interface.

### What Makes OmniForge Special?

- 🔍 **Deep Code Analysis** - Advanced metrics for complexity, maintainability, and code quality
- 🛡️ **Security Scanning** - Automated vulnerability detection across multiple severity levels
- ⚡ **Auto-Upgrade Engine** - Intelligent code modernization to latest standards
- 🏗️ **Architecture Detection** - Automatic identification of design patterns and structure
- 🎨 **Modern Web GUI** - Beautiful dark-themed interface with animations and real-time updates
- 🔧 **One-Click Setup** - Automatic environment detection and dependency installation
- 🌐 **RESTful API** - Production-ready FastAPI backend with comprehensive endpoints
- 💪 **Crash-Proof Design** - Self-healing capabilities and robust error boundaries
- 📊 **Rich Reporting** - Detailed analysis reports in multiple formats

---

## ✨ Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Multi-Language Support** | Python, JavaScript, TypeScript, Java, Go, Rust, C/C++ |
| **Complexity Analysis** | Cyclomatic complexity and maintainability index calculation |
| **Security Scanning** | Detection of hardcoded secrets, SQL injection, command injection, path traversal |
| **Dependency Analysis** | Extract and analyze project dependencies |
| **Architecture Detection** | Identify MVC, microservices, component-based patterns |
| **Code Modernization** | Upgrade to f-strings, type hints, modern exception handling |
| **Parallel Processing** | Multi-threaded analysis for fast performance |
| **Export Capabilities** | JSON and text report generation |

### User Interfaces

#### 1. Command Line Interface (CLI)
```bash
# Analyze a repository
python -m src.cli analyze /path/to/repo

# Start API server
python -m src.cli serve

# Launch web GUI
python -m src.cli gui

# Get system info
python -m src.cli info
```

#### 2. Web GUI
- Dark theme with smooth animations
- Real-time analysis progress
- Interactive visualizations
- Responsive design for all devices
- Error boundaries for stability

#### 3. RESTful API
- `/api/analyze` - Asynchronous analysis
- `/api/analyze-sync` - Synchronous analysis
- `/api/jobs/{job_id}` - Job status checking
- `/api/info` - System information
- `/health` - Health check endpoint

---

## 🎯 Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- Git

### One-Click Installation

```bash
# Clone the repository
git clone https://github.com/MASSIVEMAGNETICS/build_me.git
cd build_me

# Run the installer (automatically detects environment and installs dependencies)
./scripts/install.sh
```

That's it! The installer will:
- ✅ Detect your operating system
- ✅ Check and install prerequisites
- ✅ Create Python virtual environment
- ✅ Install all dependencies
- ✅ Set up configuration files
- ✅ Create necessary directories

### Manual Installation

If you prefer manual setup:

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Node dependencies
npm install

# 4. Create configuration
cp .env.example .env  # Edit as needed
```

---

## 📖 Usage

### CLI Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Analyze a repository
python -m src.cli analyze /path/to/repository

# Save report to file
python -m src.cli analyze /path/to/repo --output report.json --format json

# Verbose output
python -m src.cli analyze /path/to/repo --verbose

# Start API server
python -m src.cli serve --host 0.0.0.0 --port 8000
```

### API Usage

```bash
# Start the server
./scripts/start.sh

# Or with GUI
./scripts/start.sh --gui

# Custom port
./scripts/start.sh --port 8080
```

Access the API:
- API: `http://localhost:8000`
- Interactive Docs: `http://localhost:8000/docs`
- Web GUI: `http://localhost:5173` (when started with --gui)

### Python API Usage

```python
from src.core.engine import OmniForgeEngine
from src.core.config import SystemConfig

# Create engine with custom config
config = SystemConfig(debug_mode=True, parallel_workers=8)
engine = OmniForgeEngine(config=config)

# Analyze repository
report = engine.analyze_repository('/path/to/repo')

# Generate summary
summary = engine.generate_summary(report)
print(summary)

# Export report
engine.export_report(report, 'analysis_report.json')
```

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        OmniForge                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Web GUI    │  │     CLI      │  │  REST API    │     │
│  │  (React)     │  │   (Click)    │  │  (FastAPI)   │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                 │                 │              │
│         └─────────────────┴─────────────────┘              │
│                          │                                 │
│                 ┌────────▼────────┐                        │
│                 │  Core Engine    │                        │
│                 │  (Orchestrator) │                        │
│                 └────────┬────────┘                        │
│                          │                                 │
│         ┌────────────────┼────────────────┐               │
│         │                │                │               │
│   ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐         │
│   │Repository │   │  Security │   │   Code    │         │
│   │ Analyzer  │   │  Scanner  │   │ Upgrader  │         │
│   └───────────┘   └───────────┘   └───────────┘         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Component Overview

1. **Core Engine** - Main orchestration logic
2. **Repository Analyzer** - Code quality and metrics analysis
3. **Security Scanner** - Vulnerability detection
4. **Code Upgrader** - Modernization and transformation
5. **Web GUI** - React-based interface
6. **CLI** - Rich terminal interface
7. **REST API** - FastAPI backend

---

## 📊 Analysis Output

### Code Analysis Metrics
- Total Files & Lines
- Language Distribution
- Complexity Score
- Maintainability Index (0-100)
- Architecture Type
- Issue Count

### Security Scan Results
- **Critical** - Hardcoded secrets, SQL injection
- **High** - Command injection, path traversal
- **Medium** - Weak cryptography
- **Low** - Minor issues

### Recommendations
- Architecture improvements
- Code refactoring opportunities
- Security fixes
- Testing recommendations
- Documentation enhancements

---

## 🔧 Configuration

Create a `.env` file:

```bash
DEBUG_MODE=false
API_HOST=0.0.0.0
API_PORT=8000
PARALLEL_WORKERS=4
CACHE_ENABLED=true
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=src --cov-report=html
```

---

## 🚨 Troubleshooting

**Module not found errors:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Port already in use:**
```bash
./scripts/start.sh --port 8080
```

**Permission denied:**
```bash
chmod +x scripts/*.sh
```

---

## 📜 License

MIT License - see LICENSE file for details.

---

<div align="center">

**Built with ⚡ by the OmniForge Team**

*Transform your codebase into a modern masterpiece*

</div>
