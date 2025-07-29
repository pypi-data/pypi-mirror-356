#!/usr/bin/env python
"""Setup script for docsend2pdf-mcp"""

from setuptools import setup, find_packages

setup(
    name="docsend2pdf-mcp",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
)