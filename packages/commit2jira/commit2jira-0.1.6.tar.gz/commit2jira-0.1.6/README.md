# commit2jira – Build Instructions

To build the Python package:

```bash
# Install required tools
pip install --upgrade setuptools wheel

# Build the package
python setup.py sdist bdist_wheel
```

The built package files will be in the `dist/` directory.
