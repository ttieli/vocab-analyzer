# Vocab Analyzer Documentation

Welcome to the vocab-analyzer documentation! This directory contains comprehensive guides to help you make the most of the tool.

## Documentation Overview

### 📖 [User Guide](USER_GUIDE.md)
**Complete guide for all users**

Comprehensive documentation covering:
- Installation and setup
- All commands (analyze, stats, extract)
- Advanced features and options
- Understanding output and CEFR levels
- Configuration management
- Troubleshooting common issues
- Frequently asked questions

**Start here if**: You're new to vocab-analyzer or want detailed explanations.

### 🎯 [Quick Reference](QUICK_REFERENCE.md)
**One-page command reference**

Quick lookup for:
- Command syntax and options
- Common usage patterns
- File formats and output formats
- CEFR level descriptions
- Performance tips
- Troubleshooting table

**Start here if**: You need a quick command reminder or syntax lookup.

### 💡 [Practical Examples](EXAMPLES.md)
**Real-world usage scenarios**

Detailed examples for:
- Educational use cases (grading, curriculum planning, student progress)
- Content creation (graded writing, readability assessment)
- Research and analysis (author comparison, genre analysis)
- Automation scripts (batch processing, progress tracking)
- Python integration and API examples

**Start here if**: You want to see how others use vocab-analyzer in practice.

## Quick Navigation

### For Different User Types

#### 🎓 **Students & Self-Learners**
1. Read: [User Guide - Basic Usage](USER_GUIDE.md#basic-usage)
2. Try: [Quick Reference - Common Patterns](QUICK_REFERENCE.md#common-patterns)
3. Explore: [Examples - Educational Use Cases](EXAMPLES.md#educational-use-cases)

#### 👨‍🏫 **Teachers & Educators**
1. Read: [User Guide - Common Use Cases](USER_GUIDE.md#common-use-cases)
2. Try: [Examples - Use Case 1-5](EXAMPLES.md#use-case-1-selecting-graded-readers)
3. Automate: [Examples - Script 4: Weekly Progress Report](EXAMPLES.md#script-4-weekly-progress-report)

#### ✍️ **Content Creators & Writers**
1. Read: [User Guide - Understanding Output](USER_GUIDE.md#understanding-output)
2. Try: [Examples - Content Creation](EXAMPLES.md#content-creation)
3. Optimize: [Examples - Use Case 6-8](EXAMPLES.md#use-case-6-writing-graded-content)

#### 🔬 **Researchers & Analysts**
1. Read: [User Guide - Advanced Features](USER_GUIDE.md#advanced-features)
2. Try: [Examples - Research and Analysis](EXAMPLES.md#research-and-analysis)
3. Integrate: [Examples - Python Integration](EXAMPLES.md#integration-examples)

#### 💻 **Developers**
1. Read: [User Guide - Python API](USER_GUIDE.md#technical-questions)
2. Try: [Quick Reference - Python API](QUICK_REFERENCE.md#python-api)
3. Build: [Examples - Integration Examples](EXAMPLES.md#integration-examples)

## Common Tasks

### Getting Started
```bash
# Install
pip install -e .
python -m spacy download en_core_web_sm

# First analysis
vocab-analyzer analyze my_book.txt

# View help
vocab-analyzer --help
```

See: [User Guide - Installation](USER_GUIDE.md#installation)

### Analyzing Files
```bash
# Basic analysis
vocab-analyzer analyze book.txt

# Different formats
vocab-analyzer analyze book.pdf --format csv
vocab-analyzer analyze book.docx --format markdown

# Filter by level
vocab-analyzer analyze book.txt --min-level B2
```

See: [Quick Reference - Commands](QUICK_REFERENCE.md#commands)

### Viewing Statistics
```bash
# Quick stats
vocab-analyzer stats book.txt

# Extract specific levels
vocab-analyzer extract book.txt --levels B2 --levels C1
```

See: [Examples - Basic Examples](EXAMPLES.md#basic-examples)

### Automation
```bash
# Batch processing
for book in *.txt; do
    vocab-analyzer analyze "$book" --quiet
done
```

See: [Examples - Automation Scripts](EXAMPLES.md#automation-scripts)

## Additional Resources

### Project Files
- **[Main README](../README.md)**: Project overview and installation
- **[MVP Summary](.specify/mvp-implementation-complete.md)**: Complete implementation details
- **[Configuration](../config/default_config.yaml)**: Default settings

### External Resources
- **ECDICT**: [https://github.com/skywind3000/ECDICT](https://github.com/skywind3000/ECDICT)
- **spaCy**: [https://spacy.io](https://spacy.io)
- **CEFR Levels**: [https://www.coe.int/en/web/common-european-framework-reference-languages](https://www.coe.int/en/web/common-european-framework-reference-languages)

### Support
- **GitHub Issues**: [Report bugs or request features](https://github.com/yourusername/vocab-analyzer/issues)
- **Discussions**: [Ask questions and share ideas](https://github.com/yourusername/vocab-analyzer/discussions)

## Documentation Structure

```
docs/
├── README.md              # This file (documentation index)
├── USER_GUIDE.md          # Comprehensive user guide (15K words)
├── QUICK_REFERENCE.md     # One-page reference (5.6K words)
└── EXAMPLES.md            # Practical examples (16K words)
```

## Contributing to Documentation

Found an error or want to improve the docs?

1. Edit the relevant markdown file
2. Submit a pull request
3. Tag with `documentation` label

## Version Information

- **Documentation Version**: 1.0
- **Software Version**: 0.1.0 (MVP)
- **Last Updated**: 2025-11-03
- **Status**: Complete ✅

## Feedback

We'd love to hear from you!

- **Missing something?** Open an issue
- **Found a typo?** Submit a PR
- **Have a suggestion?** Start a discussion

---

**Happy analyzing!** 📚✨
