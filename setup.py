"""
Setup configuration for vocab-analyzer package.
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vocab-analyzer",
    version="0.1.0",
    author="Development Team",
    author_email="dev@example.com",
    description="English Book Vocabulary Level Analysis Tool - Analyze vocabulary in English books and classify by CEFR levels",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/vocab-analyzer",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "spacy>=3.7.0",
        "PyPDF2>=2.0.0",
        "python-docx>=1.0.0",
        "pandas>=2.0.0",
        "click>=8.1.0",
        "rich>=13.0.0",
        "PyYAML>=6.0",
        "tqdm>=4.65.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "pylint>=2.17.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "pre-commit>=3.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "vocab-analyzer=vocab_analyzer.cli.main:cli",
        ],
    },
    include_package_data=True,
    package_data={
        "vocab_analyzer": [
            "config/*.yaml",
            "data/mappings/*.json",
        ],
    },
)
