# Vocab Analyzer - Quick Reference

One-page reference for common commands and options.

## Installation

```bash
pip install -e .
python -m spacy download en_core_web_sm
```

## Commands

### analyze - Full Analysis with Export

```bash
vocab-analyzer analyze <file> [options]
```

**Options:**
- `--format`, `-f`: Output format (json|csv|markdown|md)
- `--output`, `-o`: Output file path
- `--min-level`: Minimum CEFR level (A1-C2)
- `--max-level`: Maximum CEFR level (A1-C2+)
- `--no-examples`: Exclude example sentences
- `--config`, `-c`: Custom config file
- `--quiet`, `-q`: Suppress progress output

**Examples:**
```bash
# Basic JSON output
vocab-analyzer analyze book.txt

# CSV with level filter
vocab-analyzer analyze book.pdf --format csv --min-level B2

# Markdown with custom output
vocab-analyzer analyze book.docx --format md --output report.md

# Quiet mode for scripting
vocab-analyzer analyze book.txt --quiet
```

### stats - Quick Statistics

```bash
vocab-analyzer stats <file> [--config <config>]
```

Shows:
- Total unique words
- Total occurrences
- CEFR level distribution (with visual bars)
- Word type distribution
- Intelligent insights

**Example:**
```bash
vocab-analyzer stats book.txt
```

### extract - Extract Specific Levels

```bash
vocab-analyzer extract <file> --levels <level> [--levels <level>...] [--config <config>]
```

**Example:**
```bash
vocab-analyzer extract book.txt --levels B2 --levels C1
```

Shows top 20 most frequent words per level with Chinese definitions.

## File Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| Plain Text | `.txt` | UTF-8 encoding |
| PDF | `.pdf` | Max 1000 pages |
| Word | `.docx` | Text content only |
| JSON | `.json` | Recursive string extraction |

## Output Formats

| Format | Use Case | File Extension |
|--------|----------|----------------|
| **JSON** | Programming, APIs | `.json` |
| **CSV** | Excel, Spreadsheets | `.csv` |
| **Markdown** | Documentation, Reports | `.md` |

## CEFR Levels

| Level | Description | Example Words |
|-------|-------------|---------------|
| **A1** | Beginner | be, have, go, hello |
| **A2** | Elementary | already, answer, during |
| **B1** | Intermediate | achieve, approach, context |
| **B2** | Upper-Intermediate | analyze, appropriate, complex |
| **C1** | Advanced | ambiguous, paradigm, inherent |
| **C2** | Proficiency | eloquent, quintessential |
| **C2+** | Native/Specialist | epistemology, lexicon |

## Configuration

Default: `config/default_config.yaml`

**Key settings:**
```yaml
nlp:
  model: "en_core_web_sm"
  batch_size: 100

analysis:
  min_word_length: 2
  max_word_length: 30
  exclude_proper_nouns: false

output:
  include_examples: true
  max_examples: 3

performance:
  cache_enabled: true
  cache_size: 10000
```

**Custom config:**
```bash
vocab-analyzer analyze book.txt --config my_config.yaml
```

## Common Patterns

### Batch Processing
```bash
for book in *.txt; do
    vocab-analyzer analyze "$book" --quiet
done
```

### Level-Specific Export
```bash
vocab-analyzer analyze book.txt --min-level B2 --max-level C1 --format csv
```

### Quick Difficulty Check
```bash
vocab-analyzer stats book.txt | grep "Estimated difficulty"
```

### Extract Top Words
```bash
vocab-analyzer extract book.txt --levels B2
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| "spaCy model not found" | `python -m spacy download en_core_web_sm` |
| "ModuleNotFoundError" | `pip install -e .` |
| "Out of memory" | Reduce `nlp.batch_size` in config |
| "PDF extraction failed" | PDF might be image-based (needs OCR) |

## Performance

| File Size | Processing Time |
|-----------|-----------------|
| < 10K words | 1-5 seconds |
| 10K-50K words | 5-20 seconds |
| 50K-200K words | 20-60 seconds |
| 200K+ words | 1-5 minutes |

**Optimization:**
- Increase `batch_size` for large files (200+)
- Use `--quiet` in scripts
- Enable caching (default: on)

## Python API

```python
from vocab_analyzer import VocabularyAnalyzer, Config

# Initialize
config = Config()
analyzer = VocabularyAnalyzer(config)

# Analyze
result = analyzer.analyze("book.txt")

# Access results
print(f"Total words: {len(result.words)}")
print(f"Statistics: {result.statistics}")

# Top words
for word in result.get_top_words(10):
    print(f"{word.word} ({word.level}): {word.frequency}")

# Filter by level
b2_words = result.get_words_by_level("B2")
```

## Quick Start Examples

### Example 1: First Analysis
```bash
vocab-analyzer analyze my_book.txt
# Output: my_book_analysis.json
```

### Example 2: CSV for Excel
```bash
vocab-analyzer analyze book.txt --format csv
# Open my_book_analysis.csv in Excel
```

### Example 3: Check Difficulty
```bash
vocab-analyzer stats book.txt
# See level distribution and insights
```

### Example 4: IELTS Vocab List
```bash
vocab-analyzer analyze text.pdf --min-level B2 --format csv
```

### Example 5: Compare Books
```bash
vocab-analyzer stats book1.txt > book1_stats.txt
vocab-analyzer stats book2.txt > book2_stats.txt
diff book1_stats.txt book2_stats.txt
```

## Help Commands

```bash
# General help
vocab-analyzer --help

# Command help
vocab-analyzer analyze --help
vocab-analyzer stats --help
vocab-analyzer extract --help

# Version
vocab-analyzer --version
```

## Data Sources

- **ECDICT**: 770K English-Chinese dictionary (MIT License)
- **spaCy**: NLP processing (en_core_web_sm)
- **Oxford 3000**: Common word markers
- **BNC/COCA**: Frequency data

## Resources

- **Documentation**: `docs/USER_GUIDE.md`
- **Examples**: `docs/EXAMPLES.md`
- **GitHub**: https://github.com/yourusername/vocab-analyzer
- **Issues**: https://github.com/yourusername/vocab-analyzer/issues

---

**Version**: 0.1.0 (MVP)  
**Updated**: 2025-11-03
