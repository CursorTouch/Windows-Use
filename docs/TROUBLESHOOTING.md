# Troubleshooting Guide

This guide helps you resolve common issues when using Windows-Use.

## Common Issues

### Installation Issues

#### Issue: `pip install` fails with dependency conflicts
**Solution:**
```bash
# Use UV for better dependency resolution
pip install uv
uv pip install windows-use

# Or create a fresh virtual environment
python -m venv venv
venv\Scripts\activate
pip install windows-use
```

### Runtime Issues

#### Issue: "UIAutomation not available" error
**Symptoms:**
```
ImportError: No module named 'uiautomation'
```

**Solution:**
```bash
pip install uiautomation
# If that fails, try:
pip install --upgrade --force-reinstall uiautomation
```

#### Issue: LLM connection timeouts
**Symptoms:**
```
LLMError: LLM failed after 3 attempts: Connection timeout
```

**Solutions:**
1. Check internet connection
2. Verify API keys are correct
3. Check rate limits with your LLM provider

### Performance Issues

#### Issue: Slow screenshot capture
**Solutions:**
1. Reduce screen resolution
2. Close unnecessary applications
3. Enable performance optimizations:
```python
from windows_use.performance import configure_logging
configure_logging(enable_structured_logging=True)
```

## Getting Help

### Before Reporting Issues
1. Check this troubleshooting guide
2. Search existing GitHub issues
3. Enable debug logging and collect logs

### Reporting Bugs
Include the following information:
- Windows version and build
- Python version
- Windows-Use version
- Complete error traceback

## Contact and Support

- **GitHub Issues**: [Report bugs and feature requests](https://github.com/CursorTouch/Windows-Use/issues)
- **Documentation**: [Full documentation](https://github.com/CursorTouch/Windows-Use/blob/main/README.md)