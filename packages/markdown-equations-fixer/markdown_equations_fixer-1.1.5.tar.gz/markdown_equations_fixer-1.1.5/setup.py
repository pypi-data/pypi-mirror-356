# setup.py
import os
import re
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Get the version from the __init__.py file
with open(os.path.join(here, "src/markdown_equations_fixer/__init__.py")) as f:
    version_file = f.read()
version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
if version_match:
    version = version_match.group(1)
else:
    raise RuntimeError("Unable to find version string.")

setup(
    name="markdown-equations-fixer",
    version=version,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.0.0",
        "rich>=10.0.0",
        "pypandoc",
    ],
    entry_points={
        "console_scripts": [
            "meq-fixer=markdown_equations_fixer.cli:cli",
        ],
    },
    author="Vivek Singh",
    author_email="vs15vivek@gmail.com",
    description="A CLI tool to fix mathematical equations in markdown files and convert between formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dynstat/markdown-equations-fixer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
