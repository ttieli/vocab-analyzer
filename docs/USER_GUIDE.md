# Vocab Analyzer User Guide

Welcome to the Vocab Analyzer User Guide! This comprehensive guide will help you get the most out of the vocabulary analysis tool.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Basic Usage](#basic-usage)
4. [Advanced Features](#advanced-features)
5. [Understanding Output](#understanding-output)
6. [Common Use Cases](#common-use-cases)
7. [Configuration](#configuration)
8. [Troubleshooting](#troubleshooting)
9. [FAQ](#faq)

## Quick Start

The fastest way to get started:

```bash
# Install
pip install -e .
python -m spacy download en_core_web_sm

# Analyze a book
vocab-analyzer analyze my_book.txt

# View statistics
vocab-analyzer stats my_book.txt
```

## Installation

### System Requirements

- Python 3.10 or higher
- 2GB RAM minimum (4GB recommended for large files)
- 500MB disk space for dependencies and data

### Step-by-Step Installation

1. **Clone or download the project**
   ```bash
   git clone https://github.com/yourusername/vocab-analyzer.git
   cd vocab-analyzer
   ```

2. **Create a virtual environment** (highly recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the package**
   ```bash
   pip install -e .
   ```

4. **Download spaCy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Verify installation**
   ```bash
   vocab-analyzer --version
   vocab-analyzer --help
   ```

## Basic Usage

### Command Structure

All vocab-analyzer commands follow this pattern:

```bash
vocab-analyzer <command> <file> [options]
```

### Three Main Commands

#### 1. `analyze` - Full Analysis with Export

Analyzes vocabulary and exports results to a file.

```bash
vocab-analyzer analyze book.txt
```

**Common options:**
- `--format`, `-f`: Output format (json, csv, markdown, md)
- `--output`, `-o`: Custom output file path
- `--min-level`: Minimum CEFR level (A1-C2)
- `--max-level`: Maximum CEFR level (A1-C2+)
- `--no-examples`: Exclude example sentences
- `--config`, `-c`: Custom config file
- `--quiet`, `-q`: Suppress progress output

**Examples:**

```bash
# JSON output (default)
vocab-analyzer analyze book.txt

# CSV format
vocab-analyzer analyze book.txt --format csv

# Markdown with custom output path
vocab-analyzer analyze book.txt --format markdown --output report.md

# Filter by level range
vocab-analyzer analyze book.txt --min-level B1 --max-level C1

# Quiet mode (no progress bars)
vocab-analyzer analyze book.txt --quiet
```

#### 2. `stats` - Quick Statistics

Shows statistics without creating output files.

```bash
vocab-analyzer stats book.txt
```

**Output includes:**
- Total unique words
- Total word occurrences
- CEFR level distribution (with visual bars)
- Word type distribution (nouns, verbs, adjectives, etc.)
- Intelligent insights about the text

**Example output:**
```
Analysis Statistics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Basic Metrics
  • Total unique words: 35
  • Total occurrences: 47

CEFR Level Distribution
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Level │ Count │   %   │ Distribution
──────┼───────┼───────┼──────────────────────────────
A1    |    15 |  42.9% | ██████████████████████
A2    |     9 |  25.7% | ████████████
B1    |     4 |  11.4% | █████

Insights
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • This text is suitable for beginners, with 68.6% A1-A2 vocabulary
  • Estimated difficulty: Elementary (A2)
```

#### 3. `extract` - Extract Specific Levels

Extracts vocabulary from specific CEFR levels only.

```bash
vocab-analyzer extract book.txt --levels B2 --levels C1
```

**Features:**
- Shows top 20 most frequent words per level
- Displays frequency counts
- Shows Chinese definitions (first 40 characters)

**Example:**

```bash
vocab-analyzer extract book.txt --levels B2 --levels C1

B2 Level (45 words):
  • sophisticated  (freq: 12) - 复杂的；精密的；老练的
  • inevitable     (freq: 8)  - 不可避免的
  • anticipate     (freq: 7)  - 预期；期望
  ...

C1 Level (23 words):
  • ambiguous      (freq: 5)  - 模棱两可的；含糊不清的
  • paradigm       (freq: 4)  - 范例；典范
  ...
```

## Advanced Features

### Filtering by CEFR Level

Extract only words within a specific level range:

```bash
# Only intermediate vocabulary (B1-B2)
vocab-analyzer analyze book.txt --min-level B1 --max-level B2

# Advanced vocabulary only (C1-C2+)
vocab-analyzer analyze book.txt --min-level C1
```

### Supported File Formats

Vocab-analyzer supports multiple input formats:

1. **Plain Text (.txt)**
   ```bash
   vocab-analyzer analyze book.txt
   ```

2. **PDF (.pdf)**
   ```bash
   vocab-analyzer analyze book.pdf
   ```
   - Supports up to 1000 pages
   - Extracts text from all pages

3. **Word Documents (.docx)**
   ```bash
   vocab-analyzer analyze book.docx
   ```
   - Preserves paragraph structure
   - Extracts all text content

4. **JSON (.json)**
   ```bash
   vocab-analyzer analyze data.json
   ```
   - Recursively extracts all string values
   - Useful for structured data

### Output Formats

#### JSON Format

Best for: Programming, data processing, API integration

```bash
vocab-analyzer analyze book.txt --format json
```

**Structure:**
```json
{
  "source_file": "book.txt",
  "analysis_date": "2025-11-03T10:30:00",
  "words": {
    "analyze": {
      "word": "analyze",
      "level": "B2",
      "word_type": "verb",
      "definition_cn": "分析；研究",
      "frequency": 5,
      "phonetic": "ˈænəlaɪz",
      "examples": [
        "We need to analyze the data.",
        "She analyzed the situation carefully."
      ]
    }
  },
  "statistics": {
    "total_words": 100,
    "level_distribution": {...}
  }
}
```

#### CSV Format

Best for: Excel, spreadsheets, data analysis

```bash
vocab-analyzer analyze book.txt --format csv
```

**Columns:**
- word
- level
- word_type
- definition_cn
- frequency
- phonetic
- examples (if included)

#### Markdown Format

Best for: Documentation, reports, human reading

```bash
vocab-analyzer analyze book.txt --format markdown
```

**Features:**
- Table of contents
- Level-organized sections
- Formatted tables
- Statistics summary

### Custom Configuration

Create a custom config file to override defaults:

```yaml
# my_config.yaml
nlp:
  model: "en_core_web_lg"  # Use larger model
  batch_size: 200

analysis:
  min_word_length: 3
  max_word_length: 25
  exclude_proper_nouns: true

output:
  include_examples: true
  max_examples: 5
```

Use with:
```bash
vocab-analyzer analyze book.txt --config my_config.yaml
```

## Understanding Output

### CEFR Levels Explained

| Level | Description | Vocabulary Size | Example Words |
|-------|-------------|-----------------|---------------|
| **A1** | Beginner | ~500 words | be, have, go, hello, cat |
| **A2** | Elementary | ~1000 words | already, answer, both, during |
| **B1** | Intermediate | ~2000 words | achieve, approach, context |
| **B2** | Upper-Intermediate | ~3000 words | analyze, appropriate, complex |
| **C1** | Advanced | ~4000 words | ambiguous, paradigm, inherent |
| **C2** | Proficiency | ~5000+ words | eloquent, quintessential |
| **C2+** | Native/Specialist | Academic/Technical | lexicon, epistemology |

### Word Type Classification

Words are classified by part of speech:

- **NOUN**: thing, person, place (e.g., book, teacher, London)
- **VERB**: action, state (e.g., run, think, analyze)
- **ADJ**: adjective (e.g., beautiful, complex, quick)
- **ADV**: adverb (e.g., quickly, very, carefully)
- **OTHER**: pronouns, determiners, etc.

### Statistics Insights

The tool generates intelligent insights based on:

1. **Dominant Level**: Most common CEFR level in the text
2. **Beginner Percentage**: A1-A2 vocabulary ratio
3. **Advanced Percentage**: C1-C2+ vocabulary ratio
4. **Difficulty Score**: Weighted average of all levels
5. **Word Type Distribution**: Primary parts of speech used

## Common Use Cases

### Use Case 1: IELTS/TOEFL Preparation

Extract B2-C1 vocabulary for exam prep:

```bash
vocab-analyzer analyze reading_materials.pdf \
    --min-level B2 \
    --max-level C1 \
    --format csv \
    --output ielts_vocab.csv
```

Open the CSV in Excel to create flashcards or study lists.

### Use Case 2: Graded Reader Selection

Check if a book matches student level:

```bash
vocab-analyzer stats book.txt
```

Look at the dominant level and beginner percentage:
- 60%+ A1-A2 → Good for beginners
- 50%+ B1-B2 → Good for intermediate
- 40%+ C1-C2 → Advanced readers only

### Use Case 3: Course Material Analysis

Analyze textbook vocabulary distribution:

```bash
vocab-analyzer analyze textbook.pdf --format markdown
```

Review the markdown report to ensure appropriate level progression.

### Use Case 4: Vocabulary List Generation

Create a study list for a novel:

```bash
vocab-analyzer extract novel.txt \
    --levels B2 \
    --levels C1 \
    --levels C2
```

Focus on the top 20 words per level shown.

### Use Case 5: Batch Processing

Analyze multiple books at once:

```bash
for book in books/*.txt; do
    vocab-analyzer analyze "$book" \
        --format json \
        --output "results/$(basename "$book" .txt).json"
done
```

### Use Case 6: Progress Tracking

Analyze texts periodically to track learning:

```bash
# Month 1
vocab-analyzer stats beginner_book.txt > month1.txt

# Month 3
vocab-analyzer stats intermediate_book.txt > month3.txt

# Compare difficulty levels over time
```

## Configuration

### Default Configuration

Located at `config/default_config.yaml`:

```yaml
data:
  vocabulary_file: "data/vocabularies/ecdict.csv"
  phrases_file: "data/phrases/phrasal_verbs.json"
  cefr_mapping_file: "data/mappings/cefr_ielts_mapping.csv"

nlp:
  model: "en_core_web_sm"
  batch_size: 100
  language: "en"

analysis:
  min_word_length: 2
  max_word_length: 30
  exclude_proper_nouns: false
  exclude_numbers: true

output:
  formats:
    - json
    - csv
    - markdown
  include_examples: true
  max_examples: 3

performance:
  cache_enabled: true
  cache_size: 10000
```

### Environment Variables

You can also use environment variables:

```bash
export VOCAB_ANALYZER_MODEL="en_core_web_lg"
export VOCAB_ANALYZER_BATCH_SIZE=200

vocab-analyzer analyze book.txt
```

## Troubleshooting

### Common Issues

#### 1. "spaCy model not found"

**Problem**: spaCy language model not installed

**Solution**:
```bash
python -m spacy download en_core_web_sm
```

#### 2. "PDF extraction failed"

**Problem**: PDF is image-based (scanned) or encrypted

**Solution**:
- Use OCR software to convert to text first
- Or remove PDF encryption

#### 3. "Out of memory"

**Problem**: File too large for available RAM

**Solution**:
- Reduce batch size in config: `nlp.batch_size: 50`
- Split the file into smaller chunks
- Close other applications

#### 4. "No vocabulary data found"

**Problem**: ECDICT data file missing

**Solution**:
```bash
# Check if file exists
ls data/vocabularies/ecdict.csv

# If missing, download and extract ECDICT
```

#### 5. "ModuleNotFoundError"

**Problem**: Package not installed correctly

**Solution**:
```bash
# Reinstall in development mode
pip install -e .

# Or check virtual environment is activated
source venv/bin/activate
```

### Debug Mode

For detailed error information:

```bash
# Enable Python traceback
vocab-analyzer analyze book.txt --quiet=false

# Or run with Python directly
python -m vocab_analyzer.cli.main analyze book.txt
```

## FAQ

### General Questions

**Q: How accurate is the CEFR level assignment?**

A: The tool uses ECDICT's comprehensive database (770K words) combined with Oxford 3000 markers and frequency data. Accuracy is approximately 85-90% for common words. Academic and technical terms may vary.

**Q: Can I add my own word lists?**

A: Currently not supported in v0.1.0, but planned for v0.2.0. You can modify `data/vocabularies/ecdict.csv` manually.

**Q: Does it support other languages?**

A: Currently English only. Chinese definitions are provided for learners. Multi-language support is planned for future versions.

**Q: How long does analysis take?**

A: Depends on file size:
- Small (< 10K words): 1-5 seconds
- Medium (10K-50K words): 5-20 seconds
- Large (50K-200K words): 20-60 seconds
- Very large (200K+ words): 1-5 minutes

**Q: Is it free to use?**

A: Yes, completely free and open-source (MIT License).

### Technical Questions

**Q: What spaCy model should I use?**

A:
- `en_core_web_sm` (default): Fast, 12MB, good for most cases
- `en_core_web_md`: Better accuracy, 40MB
- `en_core_web_lg`: Best accuracy, 560MB

**Q: Can I run it without internet?**

A: Yes, once spaCy model and data files are downloaded, it works completely offline.

**Q: How much disk space is needed?**

A: Approximately 500MB total:
- spaCy model: 12-560MB
- ECDICT data: 200MB
- Package dependencies: 100MB
- Cache and temp files: 50MB

**Q: Can I use it in my own Python code?**

A: Yes! Example:

```python
from vocab_analyzer import VocabularyAnalyzer, Config

config = Config()
analyzer = VocabularyAnalyzer(config)
result = analyzer.analyze("book.txt")

# Access results
print(f"Total words: {len(result.words)}")
for word in result.get_top_words(10):
    print(f"{word.word} ({word.level}): {word.frequency}")
```

**Q: Does it support multiprocessing?**

A: Not yet in v0.1.0. spaCy's batch processing provides good performance. True multiprocessing is planned for v0.2.0.

### Data Questions

**Q: Where does the vocabulary data come from?**

A: Primary source is ECDICT (770K entries):
- English definitions from WordNet
- Chinese translations from community contributors
- Frequency data from British National Corpus
- Oxford 3000 markers for common words

**Q: How often is data updated?**

A: ECDICT is updated periodically. We recommend pulling the latest version quarterly.

**Q: Can I export in other formats?**

A: Currently JSON, CSV, Markdown. Excel (.xlsx) and HTML formats are planned for v0.2.0.

## Performance Tips

### 1. Optimize for Large Files

```yaml
# config/performance_config.yaml
nlp:
  batch_size: 200  # Increase for faster processing

performance:
  cache_enabled: true
  cache_size: 20000  # Larger cache
```

### 2. Use Quiet Mode for Scripting

```bash
vocab-analyzer analyze book.txt --quiet
```

### 3. Pre-filter by Level

If you only need specific levels, filter during analysis:

```bash
vocab-analyzer analyze book.txt --min-level B2
```

This is faster than analyzing all levels then filtering afterward.

### 4. Choose Appropriate Output Format

- JSON: Slowest (full data serialization)
- CSV: Fast (simple tabular format)
- Markdown: Medium (formatted text)

## Additional Resources

- **GitHub Repository**: https://github.com/yourusername/vocab-analyzer
- **Issue Tracker**: https://github.com/yourusername/vocab-analyzer/issues
- **ECDICT**: https://github.com/skywind3000/ECDICT
- **spaCy Documentation**: https://spacy.io/usage

## Getting Help

If you encounter issues:

1. Check this guide's Troubleshooting section
2. Search existing GitHub issues
3. Create a new issue with:
   - Command you ran
   - Error message
   - System info (OS, Python version)
   - File type and size

---

**Last Updated**: 2025-11-03  
**Version**: 0.1.0 (MVP)
