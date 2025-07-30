from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Get version from environment variable or default to 1.0.0
version = os.environ.get("PACKAGE_VERSION", "1.0.0")

setup(
    name="mkdocs-ini-includer",
    version=version,
    author="MkDocs Ini Includer",
    description="A MkDocs plugin to include INI file content in documentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
    ],
    python_requires=">=3.7",
    install_requires=[
        "mkdocs>=1.0.0",
    ],
    entry_points={
        "mkdocs.plugins": [
            "ini-includer = mkdocs_ini_includer:IniIncluderPlugin",
        ]
    },
)