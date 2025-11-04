# Vocab Analyzer - 英文书词汇等级分析工具

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A CLI tool that analyzes English books and generates vocabulary lists organized by CEFR levels (A1-C2) with Chinese translations.

## Features

- Extract and analyze vocabulary from English books (TXT, PDF, DOCX)
- Classify words by CEFR levels (A1, A2, B1, B2, C1, C2, C2+)
- Recognize phrasal verbs and multi-word expressions
- Provide Chinese definitions for words
- Extract example sentences from source text
- Export results in multiple formats (JSON, CSV, Markdown)
- Statistical analysis and visualization

## Installation

### Prerequisites

- Python 3.10 or higher
- pip

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/vocab-analyzer.git
cd vocab-analyzer
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package:
```bash
pip install -e .
```

4. Download the spaCy language model:
```bash
python -m spacy download en_core_web_sm
```

### Development Installation

For development with additional tools:
```bash
pip install -e ".[dev]"
pre-commit install
```

## Usage

### Basic Analysis

Analyze a single book:
```bash
vocab-analyzer analyze path/to/book.txt
```

### Specify Output Format

```bash
vocab-analyzer analyze book.txt --format json
vocab-analyzer analyze book.txt --format csv
vocab-analyzer analyze book.txt --format markdown
```

### Advanced Options

```bash
vocab-analyzer analyze book.pdf \
    --format json \
    --output results.json \
    --min-level B1 \
    --max-level C1 \
    --no-examples
```

### View Statistics Without Exporting

```bash
vocab-analyzer stats book.txt
```

### Extract Vocabulary by Specific Levels

Extract only words from specific CEFR levels:
```bash
vocab-analyzer extract book.txt --levels B2 --levels C1
```

## Project Structure

```
vocab-analyzer/
├── src/vocab_analyzer/          # Source code
│   ├── models/                  # Data models (Word, Phrase, Analysis)
│   ├── extractors/              # Text extraction (TXT, PDF, DOCX)
│   ├── processors/              # NLP processing (tokenization, lemmatization)
│   ├── matchers/                # CEFR level matching
│   ├── analyzers/               # Statistics and analysis
│   ├── exporters/               # Output formatting (JSON, CSV, MD)
│   ├── core/                    # Core facade and config
│   ├── cli/                     # CLI interface
│   └── utils/                   # Utility functions
├── data/                        # Data resources
│   ├── vocabularies/            # CEFR wordlists
│   ├── phrases/                 # Phrasal verbs dictionary
│   ├── dictionaries/            # ECDICT Chinese-English dictionary
│   ├── sample_books/            # Sample books for testing
│   └── mappings/                # CEFR-IELTS mapping
├── tests/                       # Test suite
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   └── fixtures/                # Test fixtures
├── config/                      # Configuration files
├── scripts/                     # Data preparation scripts
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Development dependencies
├── setup.py                     # Package installation
└── README.md                    # This file
```

## Data Sources

This project uses the following open-source data:

- **ECDICT**: 770K English-Chinese dictionary (MIT License)
  - Source: https://github.com/skywind3000/ECDICT
- **Phrasal Verbs**: Common phrasal verbs dataset
  - Source: https://github.com/Semigradsky/phrasal-verbs
- **Sample Books**: Public domain books from Project Gutenberg
  - Source: https://www.gutenberg.org/

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=vocab_analyzer

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration
```

### Code Formatting

```bash
# Format code
black src/ tests/
isort src/ tests/

# Check code style
flake8 src/ tests/
pylint src/

# Type checking
mypy src/
```

### Pre-commit Hooks

```bash
# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## Configuration

Configuration is managed via `config/default_config.yaml`. You can override settings by creating a custom config file:

```bash
vocab-analyzer analyze book.txt --config my_config.yaml
```

Key configuration options:
- NLP model and batch size
- Data file paths
- Output formats
- Analysis parameters
- Logging level

## Examples

### Example 1: Extract B2+ Vocabulary for IELTS Preparation

```bash
vocab-analyzer analyze pride_and_prejudice.txt \
    --min-level B2 \
    --format csv \
    --output ielts_vocab.csv
```

### Example 2: Analyze Multiple Books

```bash
for book in *.txt; do
    vocab-analyzer analyze "$book" --output "${book%.txt}_vocab.json"
done
```

### Example 3: Get Quick Statistics

```bash
vocab-analyzer stats alice_in_wonderland.txt
```

Output:
```
Total unique words: 2,456
CEFR Level Distribution:
  A1: 523 (21.3%)
  A2: 456 (18.6%)
  B1: 512 (20.9%)
  B2: 398 (16.2%)
  C1: 287 (11.7%)
  C2: 234 (9.5%)
  C2+: 46 (1.9%)
```

## Roadmap

### Phase 1: MVP (✅ Completed - v0.1.0)
- [x] Basic text extraction (TXT, PDF, DOCX, JSON)
- [x] Vocabulary analysis and CEFR level assignment
- [x] JSON/CSV/Markdown output
- [x] CLI interface with rich formatting
- [x] Statistics and insights generation
- [x] Example sentence extraction
- [x] Chinese definitions (ECDICT integration)

**MVP Status**: 97% complete (61/63 tasks), fully functional

### Phase 2: Enhancements (Stories 3-5 - Planned)
- [ ] Advanced phrasal verb recognition (500+ expressions)
- [ ] Context-aware Chinese translations
- [ ] Enhanced example sentence extraction
- [ ] Web interface

### Phase 3: Advanced Features (Future)
- [ ] Batch processing
- [ ] Progress tracking
- [ ] Custom wordlist support
- [ ] Audio pronunciation links

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- ECDICT for the comprehensive English-Chinese dictionary
- spaCy for NLP processing
- Project Gutenberg for public domain books
- All open-source contributors

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the documentation in the `docs/` folder
- Review existing issues for solutions

## Author

Development Team

---

**Note**: This is a personal learning tool designed to help English learners analyze vocabulary in books. For educational purposes only.
