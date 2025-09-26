# Pandas Upgrade to 2.3.1

This document outlines the changes made to upgrade pandas to version 2.3.1 and ensure compatibility across the ServicePytan project.

## Summary of Changes

### 1. Python Version Requirements Updated
- **Before**: Python >= 3.6
- **After**: Python >= 3.9
- **Reason**: Pandas 2.3.1 requires Python 3.9 or higher

### 2. Dependencies Added
- `pandas>=2.3.1` - Latest stable pandas version
- `numpy>=1.24.0` - Required dependency for pandas 2.3.1

### 3. Files Modified

#### setup.py
- Updated `python_requires` from `>=3.6` to `>=3.9`
- Added `extras_require` for optional pandas installation
- Updated Python version classifiers to reflect supported versions
- Added pandas and numpy as optional dependencies

#### requirements.txt (New)
- Created main requirements file with core dependencies
- Included pandas and numpy with version constraints

#### requirements_dev.txt
- Updated all development dependencies to latest compatible versions
- Added pandas and numpy for development environment

#### tox.ini
- Updated test environments to support Python 3.9+
- Added pandas and numpy as test dependencies
- Updated Python version list

#### .travis.yml
- Updated CI/CD to test against Python 3.9+
- Added pandas and numpy installation in CI pipeline

## Installation Options

### Core Installation (without pandas)
```bash
pip install servicepytan
```

### With Data Analysis Support (includes pandas)
```bash
pip install servicepytan[analysis]
```

### Development Installation (includes pandas)
```bash
pip install servicepytan[dev]
```

## Breaking Changes

### Python Version Compatibility
- **Breaking**: Python 3.6, 3.7, and 3.8 are no longer supported
- **Minimum**: Python 3.9 required
- **Recommended**: Python 3.11+ for best performance

### Dependencies
- **New**: pandas 2.3.1+ and numpy 1.24.0+ are now required for data analysis features
- **Optional**: These dependencies are not required for core functionality

## Migration Guide

### For Users
1. **Check Python version**: Ensure you're running Python 3.9 or higher
2. **Update installation**: Use `pip install servicepytan[analysis]` if you need pandas
3. **Test functionality**: Verify your existing code works with the new version

### For Developers
1. **Update Python**: Ensure development environment uses Python 3.9+
2. **Install dev dependencies**: `pip install -r requirements_dev.txt`
3. **Run tests**: `tox` to verify all tests pass

## Testing

### Local Testing
```bash
# Install in development mode with pandas
pip install -e .[dev]

# Run tests
python -m pytest tests/

# Run with tox
tox
```

### CI/CD Testing
- Travis CI now tests against Python 3.9, 3.10, 3.11, 3.12, and 3.13
- All test environments include pandas and numpy
- Flake8 linting runs against Python 3

## Performance Improvements

### Pandas 2.3.1 Benefits
- **Performance**: Up to 2x faster than pandas 1.x for many operations
- **Memory**: Better memory efficiency with new data types
- **Compatibility**: Full compatibility with Python 3.9+
- **Features**: Access to latest pandas features and optimizations

### NumPy 1.24.0+ Benefits
- **Performance**: Improved array operations and mathematical functions
- **Compatibility**: Better integration with pandas 2.3.1
- **Security**: Latest security patches and bug fixes

## Troubleshooting

### Common Issues

#### Python Version Error
```
Error: Python version 3.8 not supported. Requires Python >= 3.9
```
**Solution**: Upgrade to Python 3.9 or higher

#### Pandas Import Error
```
ModuleNotFoundError: No module named 'pandas'
```
**Solution**: Install with pandas support: `pip install servicepytan[analysis]`

#### NumPy Version Conflict
```
VersionConflict: numpy 1.21.0 is incompatible with pandas 2.3.1
```
**Solution**: Upgrade numpy: `pip install "numpy>=1.24.0"`

### Getting Help
- Check Python version: `python --version`
- Check installed packages: `pip list`
- Verify pandas installation: `python -c "import pandas; print(pandas.__version__)"`

## Future Considerations

### Upcoming Pandas Versions
- Monitor pandas releases for new features and performance improvements
- Consider upgrading to pandas 3.x when it becomes stable (requires Python 3.9+)

### Deprecation Warnings
- Some pandas 1.x APIs may show deprecation warnings
- Review and update code to use newer pandas APIs when possible

### Performance Monitoring
- Monitor application performance after upgrade
- Use pandas profiling tools to identify optimization opportunities

## References

- [Pandas 2.3.1 Release Notes](https://pandas.pydata.org/docs/whatsnew/v2.3.1.html)
- [Pandas Installation Guide](https://pandas.pydata.org/docs/getting_started/install.html)
- [Python 3.9+ Features](https://docs.python.org/3/whatsnew/)
- [NumPy 1.24.0 Release Notes](https://numpy.org/doc/stable/release/1.24.0-notes.html)