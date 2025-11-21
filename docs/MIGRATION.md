# Migration Guide

This guide helps you migrate from the old repository structure to OmniForge.

## Overview

OmniForge is a complete transformation from a minimal repository to a production-ready code analysis and upgrade engine. This migration is a **complete replacement** rather than an incremental update.

## What Changed

### Before (Old System)
- Minimal repository with just a README
- No functionality
- No dependencies
- No infrastructure

### After (OmniForge)
- Full-featured code analysis engine
- Modern web GUI
- RESTful API
- CLI interface
- Security scanning
- Code upgrading capabilities
- Production-ready deployment

## Migration Steps

### For New Users

Simply follow the Quick Start guide in the README:

```bash
git clone https://github.com/MASSIVEMAGNETICS/build_me.git
cd build_me
./scripts/install.sh
```

### For Existing Users

If you had the old repository:

1. **Backup any local changes** (if applicable)
   ```bash
   git stash
   ```

2. **Pull the new changes**
   ```bash
   git pull origin main
   ```

3. **Install dependencies**
   ```bash
   ./scripts/install.sh
   ```

4. **Verify installation**
   ```bash
   source venv/bin/activate
   python -m src.cli info
   ```

## New Capabilities

### 1. Code Analysis
OmniForge can now analyze any repository:

```bash
python -m src.cli analyze /path/to/any/repo
```

This will provide:
- Code quality metrics
- Complexity analysis
- Security vulnerabilities
- Architecture detection
- Upgrade recommendations

### 2. Web Interface
Launch the modern GUI:

```bash
./scripts/start.sh --gui
```

Access at http://localhost:5173

### 3. API Server
Start the REST API:

```bash
./scripts/start.sh
```

API available at http://localhost:8000

### 4. Programmatic Usage

```python
from src.core.engine import OmniForgeEngine

engine = OmniForgeEngine()
report = engine.analyze_repository('/path/to/repo')
print(engine.generate_summary(report))
```

## Breaking Changes

This is a **complete rewrite**, so there are no backward compatibility concerns. The old repository had no functionality to maintain.

## Configuration

OmniForge uses environment variables for configuration. Create a `.env` file:

```bash
cp .env.example .env
# Edit .env with your settings
```

Key settings:
- `DEBUG_MODE` - Enable debug logging
- `API_PORT` - API server port
- `PARALLEL_WORKERS` - Number of analysis workers

## Data Migration

No data migration is needed as the old system stored no data.

## Testing Your Migration

1. **Verify Installation**
   ```bash
   source venv/bin/activate
   python -m src.cli info
   ```

2. **Run Tests**
   ```bash
   pytest
   ```

3. **Test CLI**
   ```bash
   python -m src.cli analyze .
   ```

4. **Test API**
   ```bash
   ./scripts/start.sh
   # In another terminal:
   curl http://localhost:8000/health
   ```

## Rollback

If you need to rollback to the previous state:

```bash
git checkout <previous-commit-hash>
```

Note: The previous version had no functionality, so rollback is not recommended.

## Getting Help

If you encounter issues during migration:

1. Check the [Troubleshooting](README.md#troubleshooting) section
2. Review the [Deployment Guide](docs/DEPLOYMENT.md)
3. Open an [issue](https://github.com/MASSIVEMAGNETICS/build_me/issues)

## Next Steps

After migration:

1. Analyze your first repository
2. Explore the web GUI
3. Read the API documentation at `/docs`
4. Customize configuration for your needs
5. Consider deployment to production

## Feature Comparison

| Feature | Old System | OmniForge |
|---------|-----------|-----------|
| Code Analysis | ❌ | ✅ |
| Security Scanning | ❌ | ✅ |
| Web GUI | ❌ | ✅ |
| REST API | ❌ | ✅ |
| CLI | ❌ | ✅ |
| Documentation | Minimal | Comprehensive |
| Tests | ❌ | ✅ |
| Deployment Ready | ❌ | ✅ |

## Conclusion

This migration transforms a minimal repository into a production-ready code analysis platform. All new functionality is additive, with no breaking changes to worry about.

Welcome to OmniForge! 🚀
