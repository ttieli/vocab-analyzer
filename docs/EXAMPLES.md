# Vocab Analyzer - Practical Examples

This document provides real-world examples and recipes for using vocab-analyzer effectively.

## Table of Contents

1. [Basic Examples](#basic-examples)
2. [Educational Use Cases](#educational-use-cases)
3. [Content Creation](#content-creation)
4. [Research and Analysis](#research-and-analysis)
5. [Automation Scripts](#automation-scripts)
6. [Integration Examples](#integration-examples)

## Basic Examples

### Example 1: First-Time Analysis

Analyze your first book:

```bash
# Simple analysis with JSON output
vocab-analyzer analyze alice_in_wonderland.txt

# Expected output:
# ✓ Analysis complete!
# Output saved to: alice_in_wonderland_analysis.json
# Total unique words: 2,456
```

### Example 2: View Quick Statistics

Get an overview without creating files:

```bash
vocab-analyzer stats sherlock_holmes.txt
```

**Output:**
```
Analysis Statistics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Basic Metrics
  • Total unique words: 3,245
  • Total occurrences: 45,678

CEFR Level Distribution
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Level │ Count │   %   │ Distribution
──────┼───────┼───────┼──────────────────────────────
A1    |   678 |  20.9% | ██████████
A2    |   812 |  25.0% | ████████████
B1    |   945 |  29.1% | ██████████████
B2    |   534 |  16.5% | ████████
C1    |   198 |   6.1% | ███
C2    |    68 |   2.1% | █
C2+   |    10 |   0.3% |

Word Type Distribution
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • NOUN: 1,456 (44.9%)
  • VERB: 892 (27.5%)
  • ADJ: 578 (17.8%)
  • ADV: 245 (7.5%)
  • OTHER: 74 (2.3%)

Insights
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • B1 is the most common level, making up 29.1% of unique vocabulary
  • This text is suitable for intermediate learners, with 45.9% A1-A2 vocabulary
  • 8.5% of vocabulary is advanced (C1-C2+), indicating moderate complexity
  • Estimated difficulty: Intermediate (B1)
  • Most common word type: Nouns (44.9% of vocabulary)
```

### Example 3: Different Output Formats

#### JSON (for data processing)
```bash
vocab-analyzer analyze book.txt --format json
```

#### CSV (for Excel/spreadsheets)
```bash
vocab-analyzer analyze book.txt --format csv
```

#### Markdown (for documentation)
```bash
vocab-analyzer analyze book.txt --format markdown
```

### Example 4: Extract Specific Levels

Focus on intermediate vocabulary:

```bash
vocab-analyzer extract book.txt --levels B1 --levels B2
```

**Output:**
```
B1 Level (145 words):
  • achieve        (freq: 12) - 完成；达到
  • approach       (freq: 10) - 接近；方法
  • attitude       (freq:  8) - 态度；看法
  • behavior       (freq:  7) - 行为；举止
  • community      (freq:  9) - 社区；团体
  ...

B2 Level (89 words):
  • analyze        (freq:  6) - 分析；研究
  • appropriate    (freq:  5) - 适当的；合适的
  • comprehensive  (freq:  4) - 全面的；综合的
  ...
```

## Educational Use Cases

### Use Case 1: Selecting Graded Readers

**Goal**: Find books appropriate for intermediate students (B1-B2 level)

**Workflow**:
```bash
# Check multiple books
for book in library/*.txt; do
    echo "=== $(basename "$book") ==="
    vocab-analyzer stats "$book" | grep "Estimated difficulty"
done
```

**Sample Output**:
```
=== easy_reader.txt ===
Estimated difficulty: Elementary (A2)

=== intermediate_novel.txt ===
Estimated difficulty: Intermediate (B1)  ← Good match!

=== advanced_text.txt ===
Estimated difficulty: Upper Intermediate (B2)
```

### Use Case 2: Creating Vocabulary Lists for Class

**Goal**: Generate B2 vocabulary flashcards

**Workflow**:
```bash
# Extract B2 words with examples
vocab-analyzer analyze textbook.pdf \
    --min-level B2 \
    --max-level B2 \
    --format csv \
    --output b2_vocabulary.csv

# Open in Excel, sort by frequency
# Print top 50 for flashcards
```

**CSV structure**:
```csv
word,level,word_type,definition_cn,frequency,phonetic,examples
analyze,B2,verb,分析；研究,15,ˈænəlaɪz,"We need to analyze the data.; She analyzed the situation."
```

### Use Case 3: Tracking Student Progress

**Goal**: Monitor vocabulary growth over semester

**Month 1** (September):
```bash
vocab-analyzer stats student_writing_sept.txt > reports/sept.txt
# Estimated difficulty: Elementary (A2)
# A1-A2: 75%
```

**Month 3** (November):
```bash
vocab-analyzer stats student_writing_nov.txt > reports/nov.txt
# Estimated difficulty: Intermediate (B1)
# A1-A2: 55%, B1-B2: 40%
```

**Analysis**: Student has progressed from A2 to B1 level!

### Use Case 4: Curriculum Material Verification

**Goal**: Ensure textbook matches advertised level (B1)

```bash
vocab-analyzer analyze textbook.pdf --format markdown

# Check markdown report:
# - Should have 40-50% B1 vocabulary
# - A1-A2 should be 30-40% (foundation)
# - B2+ should be < 20% (challenge)
```

### Use Case 5: IELTS/TOEFL Preparation

**Goal**: Build Academic Word List vocabulary

```bash
# Extract advanced vocabulary (B2-C1)
vocab-analyzer analyze academic_texts/*.pdf \
    --min-level B2 \
    --max-level C1 \
    --format csv \
    --output ielts_words.csv

# Sort by frequency in Excel
# Focus on top 200 words
```

## Content Creation

### Use Case 6: Writing Graded Content

**Goal**: Write an A2-level blog post

**Workflow**:
1. Write first draft
2. Check vocabulary level:
   ```bash
   vocab-analyzer stats draft.txt
   ```
3. If too difficult, simplify words above A2
4. Re-check until desired distribution:
   ```
   A1-A2: 70-80%
   B1: 15-20%
   B2+: < 10%
   ```

### Use Case 7: Simplifying Technical Documentation

**Goal**: Create beginner-friendly version of technical docs

**Original analysis**:
```bash
vocab-analyzer stats technical_manual.txt
# Result: 45% C1-C2 vocabulary (too advanced!)
```

**After simplification**:
```bash
vocab-analyzer stats simplified_manual.txt
# Result: 60% A1-B1 vocabulary (better!)
```

### Use Case 8: Assessing Article Readability

**Goal**: Check if blog post suits target audience (B1 learners)

```bash
vocab-analyzer stats blog_post.txt
```

**Ideal distribution for B1 audience**:
- A1-A2: 40-50% (foundation)
- B1: 30-40% (target level)
- B2+: 10-20% (challenge)

## Research and Analysis

### Use Case 9: Comparing Author Vocabulary

**Goal**: Compare vocabulary complexity between authors

```bash
# Author A
vocab-analyzer stats author_a_novel.txt | grep "Estimated difficulty"
# Result: Upper Intermediate (B2)

# Author B
vocab-analyzer stats author_b_novel.txt | grep "Estimated difficulty"
# Result: Intermediate (B1)

# Conclusion: Author A uses more complex vocabulary
```

### Use Case 10: Genre Analysis

**Goal**: Determine typical vocabulary level for mystery novels

```bash
# Analyze 10 mystery novels
for book in mystery/*.txt; do
    vocab-analyzer stats "$book" --quiet | grep "C1-C2+" 
done > mystery_complexity.txt

# Average C1-C2+ percentage across genre
```

### Use Case 11: Historical Text Analysis

**Goal**: Track vocabulary evolution over time

```bash
# 19th century novel
vocab-analyzer stats pride_prejudice_1813.txt
# C1-C2+: 15%

# Modern novel
vocab-analyzer stats contemporary_novel_2023.txt  
# C1-C2+: 8%

# Observation: Modern texts use simpler vocabulary
```

## Automation Scripts

### Script 1: Batch Processing Directory

Process all books in a folder:

```bash
#!/bin/bash
# batch_analyze.sh

INPUT_DIR="./books"
OUTPUT_DIR="./analysis_results"

mkdir -p "$OUTPUT_DIR"

for file in "$INPUT_DIR"/*.{txt,pdf,docx}; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        name="${filename%.*}"
        
        echo "Processing: $filename"
        
        vocab-analyzer analyze "$file" \
            --format json \
            --output "$OUTPUT_DIR/${name}_vocab.json" \
            --quiet
    fi
done

echo "Batch processing complete!"
```

**Usage**:
```bash
chmod +x batch_analyze.sh
./batch_analyze.sh
```

### Script 2: Level-Specific Extraction

Extract vocabulary for all CEFR levels:

```bash
#!/bin/bash
# extract_all_levels.sh

BOOK="$1"
OUTPUT_DIR="./levels"

mkdir -p "$OUTPUT_DIR"

for level in A1 A2 B1 B2 C1 C2; do
    echo "Extracting $level vocabulary..."
    
    vocab-analyzer analyze "$BOOK" \
        --min-level "$level" \
        --max-level "$level" \
        --format csv \
        --output "$OUTPUT_DIR/${level}_words.csv" \
        --quiet
done

echo "All levels extracted to $OUTPUT_DIR/"
```

**Usage**:
```bash
./extract_all_levels.sh my_book.txt
```

### Script 3: Comparison Report

Compare two texts side-by-side:

```bash
#!/bin/bash
# compare_texts.sh

TEXT1="$1"
TEXT2="$2"

echo "=== Text 1: $(basename "$TEXT1") ==="
vocab-analyzer stats "$TEXT1"

echo ""
echo "=== Text 2: $(basename "$TEXT2") ==="
vocab-analyzer stats "$TEXT2"
```

**Usage**:
```bash
./compare_texts.sh book1.txt book2.txt
```

### Script 4: Weekly Progress Report

Track student writing over time:

```bash
#!/bin/bash
# weekly_progress.sh

STUDENT_ID="$1"
WEEK="$2"
ESSAY="$3"

REPORT_DIR="./progress_reports/$STUDENT_ID"
mkdir -p "$REPORT_DIR"

vocab-analyzer stats "$ESSAY" > "$REPORT_DIR/week${WEEK}.txt"

echo "Progress report saved: $REPORT_DIR/week${WEEK}.txt"
```

**Usage**:
```bash
./weekly_progress.sh student123 5 essay_week5.txt
```

## Integration Examples

### Example 1: Python Integration

Use vocab-analyzer in your Python application:

```python
#!/usr/bin/env python3
"""Example: Integrate vocab-analyzer into Python app"""

from vocab_analyzer import VocabularyAnalyzer, Config

def analyze_text(text_file: str) -> dict:
    """Analyze a text file and return statistics."""
    
    # Initialize with default config
    config = Config()
    analyzer = VocabularyAnalyzer(config)
    
    # Perform analysis
    result = analyzer.analyze(text_file)
    
    # Extract key metrics
    stats = {
        'total_words': len(result.words),
        'total_occurrences': result.statistics['total_word_occurrences'],
        'level_distribution': result.statistics['level_distribution'],
        'difficulty': estimate_difficulty(result),
        'top_10_words': [
            {
                'word': w.word,
                'level': w.level,
                'frequency': w.frequency
            }
            for w in result.get_top_words(10)
        ]
    }
    
    return stats

def estimate_difficulty(result) -> str:
    """Estimate overall difficulty based on level distribution."""
    level_dist = result.statistics['level_distribution']
    
    beginner_pct = (
        level_dist.get('A1', {}).get('percentage', 0) +
        level_dist.get('A2', {}).get('percentage', 0)
    )
    
    if beginner_pct > 60:
        return "Beginner"
    elif beginner_pct > 40:
        return "Intermediate"
    else:
        return "Advanced"

if __name__ == "__main__":
    stats = analyze_text("sample.txt")
    print(f"Total words: {stats['total_words']}")
    print(f"Difficulty: {stats['difficulty']}")
```

### Example 2: Web API Wrapper

Create a simple Flask API:

```python
#!/usr/bin/env python3
"""Example: Simple Flask API for vocab analysis"""

from flask import Flask, request, jsonify
from vocab_analyzer import VocabularyAnalyzer, Config
import tempfile
import os

app = Flask(__name__)
analyzer = VocabularyAnalyzer(Config())

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze uploaded text file."""
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name
    
    try:
        # Analyze
        result = analyzer.analyze(tmp_path)
        
        # Format response
        response = {
            'total_words': len(result.words),
            'statistics': result.statistics,
            'top_words': [
                {
                    'word': w.word,
                    'level': w.level,
                    'frequency': w.frequency,
                    'definition': w.definition_cn
                }
                for w in result.get_top_words(20)
            ]
        }
        
        return jsonify(response)
        
    finally:
        os.unlink(tmp_path)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**Usage**:
```bash
# Start server
python api.py

# Test with curl
curl -X POST -F "file=@book.txt" http://localhost:5000/analyze
```

### Example 3: CLI Script for Teachers

Custom script for classroom use:

```python
#!/usr/bin/env python3
"""Example: Custom CLI for teachers"""

import click
from vocab_analyzer import VocabularyAnalyzer, Config
from pathlib import Path

@click.command()
@click.argument('student_essay', type=click.Path(exists=True))
@click.option('--target-level', default='B1', help='Target CEFR level')
@click.option('--report', type=click.Path(), help='Save report to file')
def grade_essay(student_essay, target_level, report):
    """Grade student essay based on vocabulary usage."""
    
    analyzer = VocabularyAnalyzer(Config())
    result = analyzer.analyze(student_essay)
    
    # Calculate score
    level_dist = result.statistics['level_distribution']
    target_pct = level_dist.get(target_level, {}).get('percentage', 0)
    
    # Generate feedback
    if target_pct >= 30:
        feedback = "Excellent use of target-level vocabulary!"
        grade = "A"
    elif target_pct >= 20:
        feedback = "Good vocabulary usage, room for improvement."
        grade = "B"
    else:
        feedback = "Needs more target-level vocabulary."
        grade = "C"
    
    # Output
    report_text = f"""
Essay Vocabulary Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Student: {Path(student_essay).stem}
Target Level: {target_level}
Grade: {grade}

Vocabulary Statistics:
  • Total unique words: {len(result.words)}
  • {target_level} vocabulary: {target_pct:.1f}%
  
Feedback:
{feedback}

Top {target_level} Words Used:
"""
    
    target_words = result.get_words_by_level(target_level)[:10]
    for word in target_words:
        report_text += f"  • {word.word} (used {word.frequency}x)\n"
    
    print(report_text)
    
    if report:
        with open(report, 'w') as f:
            f.write(report_text)
        print(f"\nReport saved to: {report}")

if __name__ == '__main__':
    grade_essay()
```

**Usage**:
```bash
python grade_essay.py student_essay.txt --target-level B1 --report feedback.txt
```

## Tips and Best Practices

### Tip 1: Use Appropriate Batch Size

For large files (100K+ words):
```yaml
# config.yaml
nlp:
  batch_size: 200  # Increase for better performance
```

### Tip 2: Filter Early

More efficient:
```bash
vocab-analyzer analyze book.txt --min-level B2  # Filter during analysis
```

Less efficient:
```bash
vocab-analyzer analyze book.txt  # Analyze all, filter later
```

### Tip 3: Leverage Quiet Mode in Scripts

```bash
# In automation scripts
vocab-analyzer analyze "$file" --quiet
```

### Tip 4: Use Meaningful Output Names

```bash
# Good
vocab-analyzer analyze book.txt --output book_b2_vocab.csv

# Not ideal
vocab-analyzer analyze book.txt --output output.csv
```

### Tip 5: Regular Cache Cleanup

```bash
# Clear cache periodically
rm -rf ~/.vocab_analyzer_cache/
```

## Conclusion

These examples demonstrate the versatility of vocab-analyzer for:
- Educational assessment
- Content creation
- Research analysis
- Automation workflows
- Software integration

For more information, see:
- [User Guide](USER_GUIDE.md) for detailed documentation
- [README](../README.md) for installation and basic usage
- [GitHub Issues](https://github.com/yourusername/vocab-analyzer/issues) for support

---

**Contributing**: Found a useful pattern? Share it by opening a PR with your example!
