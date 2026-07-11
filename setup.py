"""
Setup configuration for trading_report_generator package.

Allows installation via:
  pip install -e .
  pip install git+https://github.com/rontechvision/Trading-Report-Generator.git
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="trading-report-generator",
    version="0.1.0",
    description="Generate professional HTML trading reports with Figma design tokens",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Trading Bot Claude",
    author_email="rontechvision@gmail.com",
    url="https://github.com/rontechvision/Trading-Report-Generator",
    license="MIT",
    
    # Package discovery
    packages=find_packages(where=".", include=["skills*", "mcp*"]),
    
    # Minimum Python version
    python_requires=">=3.9",
    
    # Dependencies
    install_requires=[
        "Jinja2>=3.0.3",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "pandas>=2.0.3",
        "numpy>=1.24.3",
    ],
    
    # Optional dev dependencies
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    
    # Entry points for CLI
    entry_points={
        "console_scripts": [
            "trading-report=skills.report_generator.cli:main",
        ],
    },
    
    # Metadata
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    
    # Include data files (templates, tokens)
    package_data={
        "skills.report_generator": [
            "templates/*.jinja2",
            "design_tokens.json",
            "sample_data.json",
        ],
    },
    
    include_package_data=True,
)
