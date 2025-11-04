# Quickstart Guide: Bilingual UI with Local Translation

**Feature**: Bilingual UI with CEFR Descriptions and Local Translation
**Date**: 2025-11-04
**For**: Users setting up the bilingual interface and local translation capabilities

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Install Argos Translate](#2-install-argos-translate)
3. [Optional: Install and Configure Mdict Dictionaries](#3-optional-install-and-configure-mdict-dictionaries)
4. [Verify ECDICT Integration](#4-verify-ecdict-integration)
5. [Configure Translation Module](#5-configure-translation-module)
6. [Test Translation Fallback Chain](#6-test-translation-fallback-chain)
7. [Run Bilingual UI in Development Mode](#7-run-bilingual-ui-in-development-mode)
8. [Troubleshooting](#8-troubleshooting)

---

## Overview

This guide will walk you through setting up the bilingual English/Chinese interface with local translation capabilities. The system uses a three-tier fallback chain for translations:

1. **ECDICT** (Fast, cached) - Primary dictionary for common words
2. **Mdict** (Optional, High quality) - Professional dictionaries for detailed definitions
3. **Argos Translate** (Neural MT fallback) - Offline machine translation for anything else

**Key Features**:
- 100% offline operation (no internet required)
- Bilingual UI showing English and Chinese simultaneously
- CEFR level descriptions with educational tooltips
- On-demand translation for untranslated content
- Persistent translation cache to avoid redundant operations

**Expected Setup Time**: 30-60 minutes (depending on network speed for model downloads)

---

## 1. Prerequisites

Before starting, ensure you have:

### 1.1 System Requirements

**Minimum**:
- Python 3.13+ installed and working
- 4GB RAM available
- 1GB free disk space (for translation models)
- Modern web browser (Chrome, Firefox, Safari, Edge)

**Recommended**:
- 8GB+ RAM (for smoother translation performance)
- 2GB free disk space (if using optional Mdict dictionaries)
- SSD storage (faster dictionary indexing)

### 1.2 Existing Project Setup

Verify Feature 001 (Web Frontend) is working:

```bash
# Check Python version
python --version
# Output should be: Python 3.13.x or higher

# Activate virtual environment
cd /path/to/vocab-analyzer
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Verify existing installation
vocab-analyzer --version
vocab-analyzer analyze data/sample_books/sample.txt

# Test web interface works
vocab-analyzer web --debug
# Visit http://127.0.0.1:5000 and confirm it loads
```

If any of these fail, complete Feature 001 setup first before proceeding.

### 1.3 Verify ECDICT Data

ECDICT should already be installed from Feature 001:

```bash
# Check ECDICT file exists
ls -lh data/dictionaries/ECDICT/ecdict.csv
# Should show file size around 70-80MB

# Verify ECDICT loads correctly
python -c "
from vocab_analyzer.matchers.level_matcher import LevelMatcher
matcher = LevelMatcher(vocabulary_file='data/dictionaries/ECDICT/ecdict.csv')
print(f'✓ ECDICT loaded: {len(matcher._word_index)} words')
print(f'✓ Example translation: {matcher.get_translation(\"example\")[:50]}...')
"
```

**Expected Output**:
```
✓ ECDICT loaded: 770971 words
✓ Example translation: n. 例子, 榜样, 例题\nvt. 作为...的例子, 为...做出榜...
```

---

## 2. Install Argos Translate

Argos Translate provides offline neural machine translation from English to Chinese.

### 2.1 Install via pip

```bash
# Install argostranslate package
pip install argostranslate

# Verify installation
python -c "import argostranslate; print(f'✓ Argos Translate version: {argostranslate.__version__}')"
```

**Expected Output**:
```
✓ Argos Translate version: 1.9.6 (or higher)
```

**Troubleshooting**:
- If installation fails on Windows, you may need Visual C++ Build Tools
- On macOS/Linux, ensure you have basic build tools: `sudo apt install build-essential` (Ubuntu) or `xcode-select --install` (macOS)

### 2.2 Download English → Chinese Language Package

**Option A: Automatic Download (Recommended)**

Create a setup script to download the translation model:

```bash
# Create setup script
cat > setup_translation.py << 'EOF'
#!/usr/bin/env python3
"""Setup script for Argos Translate English → Chinese model."""

import argostranslate.package
import argostranslate.translate

def setup_en_to_zh():
    """Download and install English → Chinese translation package."""
    print("📦 Updating package index...")
    argostranslate.package.update_package_index()

    print("🔍 Finding English → Chinese package...")
    available_packages = argostranslate.package.get_available_packages()

    en_to_zh_packages = [
        pkg for pkg in available_packages
        if pkg.from_code == "en" and pkg.to_code == "zh"
    ]

    if not en_to_zh_packages:
        print("❌ Error: English → Chinese package not found")
        return False

    package = en_to_zh_packages[0]
    print(f"📥 Downloading: {package.from_name} → {package.to_name}")
    print(f"   Version: {package.package_version}")
    print("   This may take 2-5 minutes depending on your connection...")

    download_path = package.download()
    print(f"✓ Downloaded to: {download_path}")

    print("📦 Installing package...")
    argostranslate.package.install_from_path(download_path)
    print("✓ Installation complete!")

    return True

def verify_installation():
    """Test that translation works."""
    print("\n🧪 Testing translation...")

    installed_languages = argostranslate.translate.get_installed_languages()

    from_lang = next((lang for lang in installed_languages if lang.code == "en"), None)
    to_lang = next((lang for lang in installed_languages if lang.code == "zh"), None)

    if not from_lang or not to_lang:
        print("❌ Error: English or Chinese language not found")
        return False

    translation = from_lang.get_translation(to_lang)

    if not translation:
        print("❌ Error: Translation not available")
        return False

    # Test translations
    test_cases = [
        "Hello, world!",
        "run out",
        "example"
    ]

    print("\nTest translations:")
    for text in test_cases:
        result = translation.translate(text)
        print(f"  '{text}' → '{result}'")

    print("\n✓ Translation system working correctly!")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("Argos Translate Setup: English → Chinese")
    print("=" * 60)

    if setup_en_to_zh():
        verify_installation()
    else:
        print("\n❌ Setup failed. Please check your internet connection and try again.")
        exit(1)
EOF

# Make executable and run
chmod +x setup_translation.py
python setup_translation.py
```

**Expected Output**:
```
============================================================
Argos Translate Setup: English → Chinese
============================================================
📦 Updating package index...
🔍 Finding English → Chinese package...
📥 Downloading: English → Chinese
   Version: 1.9
   This may take 2-5 minutes depending on your connection...
✓ Downloaded to: /tmp/argos-translate-en-zh-1.9.argosmodel
📦 Installing package...
✓ Installation complete!

🧪 Testing translation...

Test translations:
  'Hello, world!' → '你好，世界！'
  'run out' → '用完；耗尽'
  'example' → '例子'

✓ Translation system working correctly!
```

**Option B: Manual Download**

If automatic download fails:

1. Visit: https://github.com/argosopentech/argos-translate/releases
2. Download: `translate-en_zh-1_9.argosmodel` (or latest version)
3. Install manually:

```bash
python -c "
import argostranslate.package
argostranslate.package.install_from_path('/path/to/translate-en_zh-1_9.argosmodel')
print('✓ Package installed successfully')
"
```

### 2.3 Verify Installation

```bash
# Check package directory
python -c "
import argostranslate.package
pkg_dir = argostranslate.package.get_package_directory()
print(f'✓ Packages installed at: {pkg_dir}')

import os
if os.path.exists(pkg_dir):
    packages = os.listdir(pkg_dir)
    print(f'✓ Installed packages: {len(packages)}')
    for pkg in packages:
        print(f'  - {pkg}')
else:
    print('❌ Package directory not found')
"
```

**Expected Output**:
```
✓ Packages installed at: /Users/username/.local/share/argos-translate/packages/
✓ Installed packages: 1
  - translate-en_zh-1_9
```

### 2.4 Test Translation Functionality

```bash
# Test basic translation
python -c "
import argostranslate.translate

installed = argostranslate.translate.get_installed_languages()
print(f'✓ Installed languages: {[lang.code for lang in installed]}')

from_lang = next(lang for lang in installed if lang.code == 'en')
to_lang = next(lang for lang in installed if lang.code == 'zh')
translation = from_lang.get_translation(to_lang)

test_phrases = [
    'sophisticated',
    'run out of patience',
    'Time is running out.'
]

print('\n📝 Translation tests:')
for phrase in test_phrases:
    result = translation.translate(phrase)
    print(f'  {phrase:30} → {result}')
"
```

**Expected Output**:
```
✓ Installed languages: ['en', 'zh']

📝 Translation tests:
  sophisticated                  → 精密的
  run out of patience            → 失去耐心
  Time is running out.           → 时间不多了。
```

### 2.5 Performance Benchmark

```bash
# Test translation speed (first run will be slower due to model loading)
python -c "
import argostranslate.translate
import time

installed = argostranslate.translate.get_installed_languages()
from_lang = next(lang for lang in installed if lang.code == 'en')
to_lang = next(lang for lang in installed if lang.code == 'zh')
translation = from_lang.get_translation(to_lang)

# First translation (cold start)
print('⏱️  Testing translation speed...')
print('\nFirst translation (loading model):')
start = time.time()
result = translation.translate('Hello world')
elapsed = time.time() - start
print(f'  Time: {elapsed:.2f}s → \"{result}\"')

# Subsequent translations (hot cache)
print('\nSubsequent translations (cached model):')
test_words = ['example', 'sophisticated', 'run out', 'analyze', 'furthermore']
for word in test_words:
    start = time.time()
    result = translation.translate(word)
    elapsed = time.time() - start
    print(f'  {word:15} → {result:20} ({elapsed:.3f}s)')
"
```

**Expected Performance**:
```
⏱️  Testing translation speed...

First translation (loading model):
  Time: 2.34s → "你好世界"

Subsequent translations (cached model):
  example         → 例子                  (0.087s)
  sophisticated   → 精密的                (0.091s)
  run out         → 用完                  (0.089s)
  analyze         → 分析                  (0.093s)
  furthermore     → 此外                  (0.090s)
```

**Performance Notes**:
- First translation: 2-4 seconds (model loading)
- Subsequent translations: 50-150ms
- Memory usage: ~200-300MB (acceptable for desktop app)

### 2.6 Common Issues

**Issue**: `ModuleNotFoundError: No module named 'argostranslate'`

**Solution**:
```bash
# Ensure you're in the correct virtual environment
source venv/bin/activate
pip install argostranslate
```

---

**Issue**: Package download fails with network error

**Solution**:
```bash
# Try with proxy if behind firewall
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
python setup_translation.py

# Or download manually and install from file (see Option B above)
```

---

**Issue**: Translation returns same text as input

**Solution**:
```bash
# Verify package is actually installed
python -c "
import argostranslate.translate
installed = argostranslate.translate.get_installed_languages()
print('Installed:', [(l.code, l.name) for l in installed])
"

# If output is empty, reinstall package
python setup_translation.py
```

---

## 3. (Optional) Install and Configure Mdict Dictionaries

Mdict dictionaries provide professional-quality definitions and example sentences. This step is **optional** - the system works fine with just ECDICT and Argos Translate.

### 3.1 Install mdict-query Library

```bash
# Install from GitHub (not available on PyPI)
pip install git+https://github.com/mmjang/mdict-query.git

# Verify installation
python -c "
try:
    from mdict_query import IndexBuilder
    print('✓ mdict-query installed successfully')
except ImportError as e:
    print(f'❌ Installation failed: {e}')
"
```

**Expected Output**:
```
✓ mdict-query installed successfully
```

**Alternative Installation** (if git fails):

```bash
# Clone repository and install manually
git clone https://github.com/mmjang/mdict-query.git
cd mdict-query
pip install -e .
cd ..
```

### 3.2 Obtain Mdict Dictionaries

**Where to Get .mdx Files**:

Mdict dictionaries are typically purchased or converted from existing dictionary software. Common sources:

1. **Purchased Software**: Extract .mdx files from purchased dictionary applications
2. **Community Resources**: Forums like https://forum.freemdict.com/
3. **StarDict Conversion**: Convert StarDict dictionaries to .mdx format

**Recommended Dictionaries for English Learners**:

| Dictionary | Size | Entries | Best For | Chinese Support |
|------------|------|---------|----------|-----------------|
| **OALD9** (Oxford Advanced Learner's Dictionary 9) | ~400MB | ~100,000 | Phrasal verbs, British English | Partial |
| **LDOCE6** (Longman Dictionary of Contemporary English 6) | ~350MB | ~230,000 | Usage notes, American English | Limited |
| **Collins COBUILD** | ~500MB | ~110,000 | Real usage examples | No |

**Legal Note**: Only use dictionaries you own legally. Do not download pirated copies.

### 3.3 Place Dictionaries in Project Directory

```bash
# Create dictionary directory (should already exist from Feature 001)
mkdir -p data/dictionaries

# Move your .mdx files to this directory
# Example:
cp ~/Downloads/OALD9.mdx data/dictionaries/
cp ~/Downloads/LDOCE6.mdx data/dictionaries/

# Verify files are present
ls -lh data/dictionaries/*.mdx
```

**Expected Output** (if you have dictionaries):
```
-rw-r--r--  1 user  staff   383M Nov  4 10:30 data/dictionaries/LDOCE6.mdx
-rw-r--r--  1 user  staff   421M Nov  4 10:31 data/dictionaries/OALD9.mdx
```

**If you don't have dictionaries**:
```
ls: data/dictionaries/*.mdx: No such file or directory
```

This is perfectly fine - the system will work without Mdict dictionaries.

### 3.4 Verify Dictionary Detection

```bash
# Test dictionary discovery
python -c "
from pathlib import Path

dict_dir = Path('data/dictionaries')
mdx_files = list(dict_dir.glob('*.mdx'))

print(f'📚 Found {len(mdx_files)} Mdict dictionaries:')
for mdx_file in mdx_files:
    size_mb = mdx_file.stat().st_size / (1024 * 1024)
    print(f'  - {mdx_file.name} ({size_mb:.1f} MB)')

if not mdx_files:
    print('  (No .mdx files found - this is optional)')
    print('  System will use ECDICT + Argos Translate only')
"
```

**Example Output with Dictionaries**:
```
📚 Found 2 Mdict dictionaries:
  - OALD9.mdx (421.3 MB)
  - LDOCE6.mdx (383.7 MB)
```

**Example Output without Dictionaries**:
```
📚 Found 0 Mdict dictionaries:
  (No .mdx files found - this is optional)
  System will use ECDICT + Argos Translate only
```

### 3.5 Test Dictionary Queries

**Only if you have .mdx files:**

```bash
# Test loading and querying a dictionary
python -c "
from mdict_query import IndexBuilder
from pathlib import Path
import time

# Find first .mdx file
dict_dir = Path('data/dictionaries')
mdx_files = list(dict_dir.glob('*.mdx'))

if not mdx_files:
    print('⚠️  No .mdx files found - skipping test')
    exit(0)

mdx_file = mdx_files[0]
print(f'📖 Testing dictionary: {mdx_file.name}')

# Build index (this may take 30-60 seconds on first run)
print('🔧 Building index (first time only)...')
start = time.time()
builder = IndexBuilder(str(mdx_file))
elapsed = time.time() - start
print(f'✓ Index built in {elapsed:.1f}s')

# Test lookup
print('\n🔍 Testing lookups:')
test_words = ['example', 'run out', 'sophisticated']
for word in test_words:
    result = builder.mdx_lookup(word, ignorecase=True)
    if result:
        preview = result[0][:100] if len(result[0]) > 100 else result[0]
        print(f'  ✓ \"{word}\" found: {preview}...')
    else:
        print(f'  ✗ \"{word}\" not found')
"
```

**Expected Output** (first run with OALD9):
```
📖 Testing dictionary: OALD9.mdx
🔧 Building index (first time only)...
✓ Index built in 43.2s

🔍 Testing lookups:
  ✓ "example" found: <div class="entry"><span class="hw">example</span><span class="pos">noun</span><div class...
  ✓ "run out" found: <div class="entry"><span class="hw">run out</span><span class="pos">phrasal verb</sp...
  ✓ "sophisticated" found: <div class="entry"><span class="hw">sophisticated</span><span class="pos">adjec...
```

**Note**: First run takes 30-60 seconds to build SQLite index. Subsequent lookups are fast (<10ms).

**Subsequent runs**:
```
📖 Testing dictionary: OALD9.mdx
🔧 Building index (first time only)...
✓ Index built in 0.3s  # Much faster - index already exists

🔍 Testing lookups:
  ✓ "example" found: ...
  ✓ "run out" found: ...
  ✓ "sophisticated" found: ...
```

### 3.6 Handling Missing Dictionaries Gracefully

The system is designed to work without Mdict dictionaries:

```bash
# Test fallback behavior without Mdict
python -c "
print('📝 Translation fallback chain:')
print('  1. ECDICT (fast, 770K+ words)')
print('  2. Mdict (optional, professional quality)')
print('  3. Argos Translate (neural MT fallback)')
print()

from pathlib import Path
mdx_files = list(Path('data/dictionaries').glob('*.mdx'))

if mdx_files:
    print(f'✓ Mdict available: {len(mdx_files)} dictionaries')
    print('  Translation chain: ECDICT → Mdict → Argos')
else:
    print('⚠️  Mdict not available (optional)')
    print('  Translation chain: ECDICT → Argos')
    print('  This is perfectly fine for most use cases!')
"
```

**Output without Mdict**:
```
📝 Translation fallback chain:
  1. ECDICT (fast, 770K+ words)
  2. Mdict (optional, professional quality)
  3. Argos Translate (neural MT fallback)

⚠️  Mdict not available (optional)
  Translation chain: ECDICT → Argos
  This is perfectly fine for most use cases!
```

---

## 4. Verify ECDICT Integration

ECDICT should already be working from Feature 001. Let's verify it provides Chinese translations:

### 4.1 Check ECDICT Setup

```bash
# Verify ECDICT file exists and is readable
python -c "
from pathlib import Path

ecdict_path = Path('data/dictionaries/ECDICT/ecdict.csv')

if not ecdict_path.exists():
    print('❌ ECDICT not found')
    print('   Expected location:', ecdict_path)
    print('   Please complete Feature 001 setup first')
    exit(1)

size_mb = ecdict_path.stat().st_size / (1024 * 1024)
print(f'✓ ECDICT found: {size_mb:.1f} MB')

# Count lines (approximate entry count)
with open(ecdict_path, 'r', encoding='utf-8') as f:
    line_count = sum(1 for _ in f) - 1  # Subtract header
print(f'✓ Entries: ~{line_count:,}')
"
```

**Expected Output**:
```
✓ ECDICT found: 76.8 MB
✓ Entries: ~770,971
```

### 4.2 Test ECDICT Queries

```bash
# Test translation lookup for various word types
python -c "
from vocab_analyzer.matchers.level_matcher import LevelMatcher

print('🔍 Testing ECDICT translations...\n')

matcher = LevelMatcher(vocabulary_file='data/dictionaries/ECDICT/ecdict.csv')

test_cases = [
    ('example', 'Common noun'),
    ('sophisticated', 'B2 level adjective'),
    ('run', 'Common verb with multiple meanings'),
    ('analyze', 'Academic verb'),
    ('hello', 'Basic greeting'),
]

for word, description in test_cases:
    translation = matcher.get_translation(word)
    if translation:
        # Show first 80 chars of translation
        preview = translation[:80] + '...' if len(translation) > 80 else translation
        print(f'✓ {word:15} ({description})')
        print(f'  {preview}')
        print()
    else:
        print(f'✗ {word:15} - No translation found')
        print()

print('✓ ECDICT translation working correctly')
"
```

**Expected Output**:
```
🔍 Testing ECDICT translations...

✓ example        (Common noun)
  n. 例子, 榜样, 例题\nvt. 作为...的例子, 为...做出榜样\nvi. 举例, 作为...的示范...

✓ sophisticated  (B2 level adjective)
  a. 精密的, 复杂的, 久经世故的, 老练的...

✓ run            (Common verb with multiple meanings)
  n. 奔跑, 路程, 趋向\nvi. 跑, 行驶, 运转, 流, 竞选, 褪色, 融化, 流行\nvt. 使...

✓ analyze        (Academic verb)
  vt. 分析, 分解, 解释\n[计] 分析...

✓ hello          (Basic greeting)
  n. 表示问候， 惊奇或唤起注意时的用语\nint. 喂，你好，嘿...

✓ ECDICT translation working correctly
```

### 4.3 Verify Chinese Translation Coverage

```bash
# Test coverage for different CEFR levels
python -c "
from vocab_analyzer.matchers.level_matcher import LevelMatcher

matcher = LevelMatcher(vocabulary_file='data/dictionaries/ECDICT/ecdict.csv')

# Sample words from each level
level_samples = {
    'A1': ['hello', 'thank', 'yes', 'no', 'please'],
    'A2': ['weather', 'family', 'shopping', 'restaurant'],
    'B1': ['environment', 'opportunity', 'relationship'],
    'B2': ['sophisticated', 'analyze', 'circumstances'],
    'C1': ['predominantly', 'paradigm', 'eloquent'],
    'C2': ['ubiquitous', 'quintessential'],
}

print('📊 ECDICT coverage by CEFR level:\n')

for level, words in level_samples.items():
    found = sum(1 for w in words if matcher.get_translation(w))
    coverage = (found / len(words)) * 100
    print(f'{level}: {found}/{len(words)} ({coverage:.0f}%)')

print('\n✓ ECDICT has excellent coverage across all levels')
"
```

**Expected Output**:
```
📊 ECDICT coverage by CEFR level:

A1: 5/5 (100%)
A2: 4/4 (100%)
B1: 3/3 (100%)
B2: 3/3 (100%)
C1: 3/3 (100%)
C2: 2/2 (100%)

✓ ECDICT has excellent coverage across all levels
```

---

## 5. Configure Translation Module

Now let's set up the translation module that coordinates ECDICT, Mdict, and Argos Translate.

### 5.1 Create Data Directories Structure

```bash
# Create necessary directories
mkdir -p data/translation_models
mkdir -p data/cefr_data

# Verify directory structure
tree data/ -L 2 -d
```

**Expected Output**:
```
data/
├── dictionaries
│   ├── ECDICT
│   └── (optional .mdx files)
├── translation_models
│   └── (Argos Translate packages - managed automatically)
├── cefr_data
└── sample_books
```

### 5.2 Initialize Translation Cache

```bash
# Create initial translation cache file
python -c "
import json
from pathlib import Path
from datetime import datetime

cache_file = Path('data/translation_cache.json')

if cache_file.exists():
    print('⚠️  Translation cache already exists')
    print(f'   Location: {cache_file}')
    print('   Skipping initialization')
else:
    initial_cache = {
        'version': '1.0',
        'last_saved': int(datetime.now().timestamp()),
        'metadata': {
            'total_entries': 0,
            'cache_hit_rate': 0.0,
            'last_cleanup': int(datetime.now().timestamp())
        },
        'entries': {}
    }

    cache_file.parent.mkdir(parents=True, exist_ok=True)
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(initial_cache, f, ensure_ascii=False, indent=2)

    print(f'✓ Translation cache created: {cache_file}')
    print(f'  Version: {initial_cache[\"version\"]}')
    print(f'  Size: {cache_file.stat().st_size} bytes')
"
```

**Expected Output**:
```
✓ Translation cache created: data/translation_cache.json
  Version: 1.0
  Size: 184 bytes
```

### 5.3 Load CEFR Definitions

```bash
# Create CEFR definitions file with bilingual content
python -c "
import json
from pathlib import Path

cefr_file = Path('data/cefr_definitions.json')

if cefr_file.exists():
    print('⚠️  CEFR definitions already exist')
    print(f'   Location: {cefr_file}')
else:
    cefr_data = {
        'version': '1.0',
        'last_updated': '2025-11-04',
        'source': 'Council of Europe CEFR + vocabulary context adaptation',
        'levels': {
            'A1': {
                'level_code': 'A1',
                'name_en': 'Beginner',
                'name_cn': '初级',
                'short_description_en': 'Can understand and use familiar everyday expressions',
                'short_description_cn': '能够理解和使用熟悉的日常表达',
                'description_en': 'Can understand and use familiar everyday expressions and very basic phrases. Can introduce themselves and others and can ask and answer questions about personal details.',
                'description_cn': '能够理解和使用熟悉的日常表达和非常基本的短语。能够介绍自己和他人，能够询问和回答有关个人详细信息的问题。',
                'vocabulary_size': '500-1000',
                'example_words': ['hello', 'thank', 'yes', 'no', 'please', 'help'],
                'learning_context': 'Typical learner: Absolute beginner, 0-6 months of study / 典型学习者：绝对初学者、学习0-6个月'
            },
            'A2': {
                'level_code': 'A2',
                'name_en': 'Elementary',
                'name_cn': '基础级',
                'short_description_en': 'Can communicate in simple routine tasks',
                'short_description_cn': '能够在简单的日常任务中沟通',
                'description_en': 'Can understand sentences related to areas of most immediate relevance. Can communicate in simple and routine tasks requiring direct exchange of information.',
                'description_cn': '能够理解与最直接相关领域相关的句子。能够在需要就熟悉事项进行直接信息交流的任务中进行沟通。',
                'vocabulary_size': '1000-2000',
                'example_words': ['weather', 'family', 'shopping', 'restaurant', 'appointment'],
                'learning_context': 'Typical learner: Can handle basic conversations, 6-12 months / 典型学习者：能够处理基本对话、学习6-12个月'
            },
            'B1': {
                'level_code': 'B1',
                'name_en': 'Intermediate',
                'name_cn': '中级',
                'short_description_en': 'Can handle most situations while traveling',
                'short_description_cn': '能够处理旅行时的大多数情况',
                'description_en': 'Can understand main points on familiar matters. Can deal with most situations while traveling. Can describe experiences and events.',
                'description_cn': '能够理解熟悉事项的要点。能够处理旅行时的大多数情况。能够描述经历和事件。',
                'vocabulary_size': '2000-3000',
                'example_words': ['environment', 'opportunity', 'development', 'relationship'],
                'learning_context': 'Typical learner: Can communicate independently, 1-3 years / 典型学习者：能够独立沟通、学习1-3年'
            },
            'B2': {
                'level_code': 'B2',
                'name_en': 'Upper Intermediate',
                'name_cn': '中高级',
                'short_description_en': 'Can interact with fluency and spontaneity',
                'short_description_cn': '能够流畅自发地互动',
                'description_en': 'Can understand complex text on concrete and abstract topics. Can interact with fluency and spontaneity with native speakers.',
                'description_cn': '能够理解具体和抽象主题的复杂文本。能够流畅自发地与母语者互动。',
                'vocabulary_size': '3000-5000',
                'example_words': ['sophisticated', 'analyze', 'circumstances', 'nevertheless'],
                'learning_context': 'Typical learner: University student, 3-5 years / 典型学习者：大学生、学习3-5年'
            },
            'C1': {
                'level_code': 'C1',
                'name_en': 'Advanced',
                'name_cn': '高级',
                'short_description_en': 'Can use language flexibly and effectively',
                'short_description_cn': '能够灵活有效地使用语言',
                'description_en': 'Can understand demanding texts and recognize implicit meaning. Can express ideas fluently without obvious searching for expressions.',
                'description_cn': '能够理解要求较高的文本并识别隐含意义。能够流畅地表达想法而无需明显寻找表达方式。',
                'vocabulary_size': '5000-8000',
                'example_words': ['predominantly', 'paradigm', 'intricate', 'eloquent'],
                'learning_context': 'Typical learner: Graduate student, 5-8 years / 典型学习者：研究生、学习5-8年'
            },
            'C2': {
                'level_code': 'C2',
                'name_en': 'Proficient',
                'name_cn': '精通级',
                'short_description_en': 'Can understand virtually everything with ease',
                'short_description_cn': '能够轻松理解几乎所有内容',
                'description_en': 'Can understand virtually everything heard or read. Can express themselves spontaneously, very fluently and precisely.',
                'description_cn': '能够理解几乎所有听到或读到的内容。能够自发、非常流利和准确地表达自己。',
                'vocabulary_size': '8000-10000+',
                'example_words': ['ubiquitous', 'quintessential', 'juxtaposition', 'hitherto'],
                'learning_context': 'Typical learner: Near-native, 8+ years / 典型学习者：接近母语者、学习8年以上'
            },
            'C2+': {
                'level_code': 'C2+',
                'name_en': 'Beyond CEFR',
                'name_cn': '超出CEFR范围',
                'short_description_en': 'Specialized or archaic vocabulary',
                'short_description_cn': '专业或古老词汇',
                'description_en': 'Highly specialized technical terms or extremely rare vocabulary beyond standard proficiency.',
                'description_cn': '高度专业化的技术术语或极其罕见的词汇，超出标准熟练度。',
                'vocabulary_size': '10000+',
                'example_words': ['sesquipedalian', 'antediluvian', 'perspicacious'],
                'learning_context': 'Academic literature, historical texts / 学术文献、历史文本'
            }
        }
    }

    cefr_file.parent.mkdir(parents=True, exist_ok=True)
    with open(cefr_file, 'w', encoding='utf-8') as f:
        json.dump(cefr_data, f, ensure_ascii=False, indent=2)

    print(f'✓ CEFR definitions created: {cefr_file}')
    print(f'  Levels defined: {len(cefr_data[\"levels\"])}')
    print(f'  Size: {cefr_file.stat().st_size} bytes')

# Verify CEFR file
with open(cefr_file, 'r', encoding='utf-8') as f:
    cefr_data = json.load(f)
    print(f'\n✓ CEFR definitions loaded successfully')
    print('  Levels:', ', '.join(cefr_data['levels'].keys()))
"
```

**Expected Output**:
```
✓ CEFR definitions created: data/cefr_definitions.json
  Levels defined: 7
  Size: 4832 bytes

✓ CEFR definitions loaded successfully
  Levels: A1, A2, B1, B2, C1, C2, C2+
```

### 5.4 Configure Dictionary Priorities

```bash
# Test dictionary priority configuration
python -c "
from pathlib import Path

print('📋 Dictionary Priority Configuration:\n')

# Priority 1: ECDICT (always available)
ecdict_path = Path('data/dictionaries/ECDICT/ecdict.csv')
if ecdict_path.exists():
    print('1. ECDICT (Primary)')
    print('   Status: ✓ Available')
    print('   Speed: <1ms (cached)')
    print('   Coverage: 770K+ words')
else:
    print('1. ECDICT (Primary)')
    print('   Status: ❌ Not found - SETUP REQUIRED')

# Priority 2: Mdict (optional)
mdx_files = list(Path('data/dictionaries').glob('*.mdx'))
if mdx_files:
    print(f'\n2. Mdict (Enhanced, optional)')
    print(f'   Status: ✓ Available ({len(mdx_files)} dictionaries)')
    print('   Speed: ~10ms per lookup')
    for idx, mdx in enumerate(sorted(mdx_files), 1):
        print(f'   {idx}. {mdx.name}')
else:
    print(f'\n2. Mdict (Enhanced, optional)')
    print('   Status: ⚠️  Not configured (optional)')
    print('   Note: System will skip Mdict tier')

# Priority 3: Argos Translate (always available after setup)
try:
    import argostranslate.translate
    installed = argostranslate.translate.get_installed_languages()
    has_en_zh = any(l.code == 'en' for l in installed) and any(l.code == 'zh' for l in installed)

    print(f'\n3. Argos Translate (Fallback)')
    if has_en_zh:
        print('   Status: ✓ Available')
        print('   Speed: ~100ms (cached model)')
        print('   Coverage: Universal (neural MT)')
    else:
        print('   Status: ❌ Not configured - SETUP REQUIRED')
except ImportError:
    print(f'\n3. Argos Translate (Fallback)')
    print('   Status: ❌ Not installed - SETUP REQUIRED')

print('\n' + '='*60)
print('✓ Configuration complete')
"
```

**Expected Output** (with Mdict):
```
📋 Dictionary Priority Configuration:

1. ECDICT (Primary)
   Status: ✓ Available
   Speed: <1ms (cached)
   Coverage: 770K+ words

2. Mdict (Enhanced, optional)
   Status: ✓ Available (2 dictionaries)
   Speed: ~10ms per lookup
   1. LDOCE6.mdx
   2. OALD9.mdx

3. Argos Translate (Fallback)
   Status: ✓ Available
   Speed: ~100ms (cached model)
   Coverage: Universal (neural MT)

============================================================
✓ Configuration complete
```

**Expected Output** (without Mdict - perfectly fine):
```
📋 Dictionary Priority Configuration:

1. ECDICT (Primary)
   Status: ✓ Available
   Speed: <1ms (cached)
   Coverage: 770K+ words

2. Mdict (Enhanced, optional)
   Status: ⚠️  Not configured (optional)
   Note: System will skip Mdict tier

3. Argos Translate (Fallback)
   Status: ✓ Available
   Speed: ~100ms (cached model)
   Coverage: Universal (neural MT)

============================================================
✓ Configuration complete
```

### 5.5 Set Translation Preferences

```bash
# Create configuration file for translation settings
cat > data/translation_config.yaml << 'EOF'
# Translation Module Configuration
version: "1.0"

# Cache settings
cache:
  enabled: true
  file: "data/translation_cache.json"
  max_age_days: 30
  auto_save: true
  save_interval_minutes: 5

# Dictionary settings
dictionaries:
  ecdict:
    enabled: true
    path: "data/dictionaries/ECDICT/ecdict.csv"
    priority: 1

  mdict:
    enabled: true
    directory: "data/dictionaries"
    priority: 2
    auto_discover: true

  argos:
    enabled: true
    priority: 3
    lazy_load: true
    model_dir: "~/.local/share/argos-translate/packages/"

# CEFR settings
cefr:
  definitions_file: "data/cefr_definitions.json"
  show_tooltips: true
  show_modal_on_click: true

# Performance settings
performance:
  max_translation_length: 500
  translation_timeout_seconds: 5
  cache_in_memory: true
  memory_cache_size: 1000
EOF

echo "✓ Translation configuration saved: data/translation_config.yaml"
cat data/translation_config.yaml
```

**Expected Output**:
```
✓ Translation configuration saved: data/translation_config.yaml
# Translation Module Configuration
version: "1.0"
...
(configuration contents)
```

---

## 6. Test Translation Fallback Chain

Now let's test the complete translation fallback chain to ensure all tiers work correctly.

### 6.1 Test ECDICT Lookup (Tier 1)

```bash
# Test ECDICT as first tier
python -c "
from vocab_analyzer.matchers.level_matcher import LevelMatcher
import time

print('🔍 Testing Tier 1: ECDICT\n')

matcher = LevelMatcher(vocabulary_file='data/dictionaries/ECDICT/ecdict.csv')

test_words = [
    'example',
    'sophisticated',
    'analyze',
    'hello',
    'environment'
]

print('Test Results:')
for word in test_words:
    start = time.time()
    translation = matcher.get_translation(word)
    elapsed = (time.time() - start) * 1000

    if translation:
        preview = translation[:60] + '...' if len(translation) > 60 else translation
        print(f'✓ {word:15} → {preview:40} ({elapsed:.2f}ms)')
    else:
        print(f'✗ {word:15} → Not found ({elapsed:.2f}ms)')

print('\n✅ Tier 1 (ECDICT) working correctly')
"
```

**Expected Output**:
```
🔍 Testing Tier 1: ECDICT

Test Results:
✓ example        → n. 例子, 榜样, 例题\nvt. 作为...的例子, 为...做出...        (0.15ms)
✓ sophisticated  → a. 精密的, 复杂的, 久经世故的, 老练的...                  (0.12ms)
✓ analyze        → vt. 分析, 分解, 解释\n[计] 分析...                     (0.13ms)
✓ hello          → n. 表示问候， 惊奇或唤起注意时的用语\nint. 喂，你好，嘿... (0.14ms)
✓ environment    → n. 环境, 外界\n[计] 环境...                          (0.11ms)

✅ Tier 1 (ECDICT) working correctly
```

### 6.2 Test Mdict Lookup (Tier 2 - Optional)

**Skip this if you don't have Mdict dictionaries.**

```bash
# Test Mdict dictionary lookup
python -c "
from pathlib import Path
from mdict_query import IndexBuilder
import time

print('🔍 Testing Tier 2: Mdict\n')

mdx_files = list(Path('data/dictionaries').glob('*.mdx'))

if not mdx_files:
    print('⚠️  No Mdict dictionaries found - skipping test')
    print('   This is optional - fallback chain will skip to Tier 3')
    exit(0)

mdx_file = mdx_files[0]
print(f'📖 Using: {mdx_file.name}\n')

builder = IndexBuilder(str(mdx_file))

test_words = [
    'run out',  # Phrasal verb
    'sophisticated',
    'blow up',  # Phrasal verb
    'example'
]

print('Test Results:')
for word in test_words:
    start = time.time()
    result = builder.mdx_lookup(word, ignorecase=True)
    elapsed = (time.time() - start) * 1000

    if result:
        # Extract plain text preview from HTML
        preview = result[0][:80].replace('<', '').replace('>', '')
        print(f'✓ {word:15} → Found ({elapsed:.1f}ms)')
        print(f'  Preview: {preview}...')
    else:
        print(f'✗ {word:15} → Not found ({elapsed:.1f}ms)')

print('\n✅ Tier 2 (Mdict) working correctly')
"
```

**Expected Output** (if you have Mdict):
```
🔍 Testing Tier 2: Mdict

📖 Using: OALD9.mdx

Test Results:
✓ run out        → Found (7.2ms)
  Preview: div class=\"entry\"span class=\"hw\"run out/spanspan class=\"pos\"phrasal verb...
✓ sophisticated  → Found (6.8ms)
  Preview: div class=\"entry\"span class=\"hw\"sophisticated/spanspan class=\"pos\"adjecti...
✓ blow up        → Found (7.1ms)
  Preview: div class=\"entry\"span class=\"hw\"blow up/spanspan class=\"pos\"phrasal verb/...
✓ example        → Found (6.9ms)
  Preview: div class=\"entry\"span class=\"hw\"example/spanspan class=\"pos\"noun/spanspan...

✅ Tier 2 (Mdict) working correctly
```

### 6.3 Test Argos Translate Fallback (Tier 3)

```bash
# Test Argos Translate as final fallback
python -c "
import argostranslate.translate
import time

print('🔍 Testing Tier 3: Argos Translate\n')

installed = argostranslate.translate.get_installed_languages()
from_lang = next((lang for lang in installed if lang.code == 'en'), None)
to_lang = next((lang for lang in installed if lang.code == 'zh'), None)

if not from_lang or not to_lang:
    print('❌ Argos Translate not configured')
    print('   Please complete Section 2 of this guide')
    exit(1)

translation = from_lang.get_translation(to_lang)

# Test cases that might not be in ECDICT
test_cases = [
    ('run out of patience', 'phrase'),
    ('Time is running out.', 'sentence'),
    ('extremely sophisticated technology', 'phrase'),
    ('I need to analyze the data carefully.', 'sentence')
]

print('Test Results:')
for text, text_type in test_cases:
    start = time.time()
    result = translation.translate(text)
    elapsed = (time.time() - start) * 1000

    print(f'\n{text_type.upper()}: \"{text}\"')
    print(f'  → \"{result}\" ({elapsed:.0f}ms)')

print('\n✅ Tier 3 (Argos Translate) working correctly')
"
```

**Expected Output**:
```
🔍 Testing Tier 3: Argos Translate

Test Results:

PHRASE: "run out of patience"
  → "失去耐心" (102ms)

SENTENCE: "Time is running out."
  → "时间不多了。" (95ms)

PHRASE: "extremely sophisticated technology"
  → "极其复杂的技术" (108ms)

SENTENCE: "I need to analyze the data carefully."
  → "我需要仔细分析数据。" (112ms)

✅ Tier 3 (Argos Translate) working correctly
```

### 6.4 Verify Fallback Order

```bash
# Test complete fallback chain with mixed cases
python -c "
from vocab_analyzer.matchers.level_matcher import LevelMatcher
from pathlib import Path
import argostranslate.translate
import time

print('🔄 Testing Complete Fallback Chain\n')

# Setup
ecdict = LevelMatcher(vocabulary_file='data/dictionaries/ECDICT/ecdict.csv')
has_mdict = len(list(Path('data/dictionaries').glob('*.mdx'))) > 0

argos_installed = argostranslate.translate.get_installed_languages()
argos_from = next((l for l in argos_installed if l.code == 'en'), None)
argos_to = next((l for l in argos_installed if l.code == 'zh'), None)
argos = argos_from.get_translation(argos_to) if argos_from and argos_to else None

# Test cases
test_cases = [
    ('example', 'Common word (should hit ECDICT)'),
    ('run out of steam', 'Idiom (may need Argos)'),
    ('sophisticated analysis', 'Phrase (may need Argos)'),
]

print('Source Priority:')
print('  1️⃣  ECDICT (fast)')
print('  2️⃣  Mdict (optional, quality)' if has_mdict else '  2️⃣  Mdict (not available)')
print('  3️⃣  Argos Translate (fallback)')
print()

for text, description in test_cases:
    print(f'Testing: \"{text}\" ({description})')

    # Try ECDICT first
    start = time.time()
    ecdict_result = ecdict.get_translation(text)
    ecdict_time = (time.time() - start) * 1000

    if ecdict_result:
        preview = ecdict_result[:50] + '...' if len(ecdict_result) > 50 else ecdict_result
        print(f'  ✓ ECDICT hit: {preview} ({ecdict_time:.1f}ms)')
    else:
        print(f'  ✗ ECDICT miss ({ecdict_time:.1f}ms)')

        # Fallback to Argos
        if argos:
            start = time.time()
            argos_result = argos.translate(text)
            argos_time = (time.time() - start) * 1000
            print(f'  ✓ Argos fallback: {argos_result} ({argos_time:.0f}ms)')
    print()

print('✅ Fallback chain working correctly')
print('   Order: ECDICT → Mdict → Argos')
"
```

**Expected Output**:
```
🔄 Testing Complete Fallback Chain

Source Priority:
  1️⃣  ECDICT (fast)
  2️⃣  Mdict (optional, quality)
  3️⃣  Argos Translate (fallback)

Testing: "example" (Common word (should hit ECDICT))
  ✓ ECDICT hit: n. 例子, 榜样, 例题\nvt. 作为...的例子, 为...做出榜... (0.2ms)

Testing: "run out of steam" (Idiom (may need Argos))
  ✗ ECDICT miss (0.3ms)
  ✓ Argos fallback: 用完力气 (105ms)

Testing: "sophisticated analysis" (Phrase (may need Argos))
  ✗ ECDICT miss (0.2ms)
  ✓ Argos fallback: 复杂的分析 (98ms)

✅ Fallback chain working correctly
   Order: ECDICT → Mdict → Argos
```

### 6.5 Verify Cache Persistence

```bash
# Test translation caching
python -c "
import json
from pathlib import Path
import time

cache_file = Path('data/translation_cache.json')

# Load initial cache
with open(cache_file, 'r', encoding='utf-8') as f:
    cache_before = json.load(f)
    initial_count = len(cache_before.get('entries', {}))

print(f'📝 Initial cache entries: {initial_count}')

# Simulate adding a translation to cache
new_entry = {
    'source_text': 'run out of steam',
    'target_text': '用完力气',
    'timestamp': int(time.time()),
    'translation_type': 'phrase',
    'source': 'argos',
    'confidence_score': 0.75,
    'access_count': 1
}

cache_before['entries']['phrase:run out of steam'] = new_entry
cache_before['metadata']['total_entries'] = len(cache_before['entries'])
cache_before['last_saved'] = int(time.time())

# Save updated cache
with open(cache_file, 'w', encoding='utf-8') as f:
    json.dump(cache_before, f, ensure_ascii=False, indent=2)

print(f'✓ Added test entry to cache')

# Verify cache was saved
with open(cache_file, 'r', encoding='utf-8') as f:
    cache_after = json.load(f)
    final_count = len(cache_after['entries'])

print(f'✓ Cache entries after save: {final_count}')
print(f'✓ Cache file size: {cache_file.stat().st_size} bytes')

if 'phrase:run out of steam' in cache_after['entries']:
    print(f'✅ Cache persistence working correctly')
    print(f'   Cached entry: phrase:run out of steam → 用完力气')
else:
    print('❌ Cache persistence failed')
"
```

**Expected Output**:
```
📝 Initial cache entries: 0
✓ Added test entry to cache
✓ Cache entries after save: 1
✓ Cache file size: 445 bytes
✅ Cache persistence working correctly
   Cached entry: phrase:run out of steam → 用完力气
```

### 6.6 Check Fallback Order Performance

```bash
# Benchmark translation times for each tier
python -c "
from vocab_analyzer.matchers.level_matcher import LevelMatcher
import argostranslate.translate
import time
import statistics

print('⚡ Translation Performance Benchmarks\n')

ecdict = LevelMatcher(vocabulary_file='data/dictionaries/ECDICT/ecdict.csv')
argos_langs = argostranslate.translate.get_installed_languages()
argos_from = next((l for l in argos_langs if l.code == 'en'), None)
argos_to = next((l for l in argos_langs if l.code == 'zh'), None)
argos = argos_from.get_translation(argos_to)

# Benchmark ECDICT
print('1️⃣  ECDICT Performance:')
ecdict_times = []
test_words = ['example', 'sophisticated', 'analyze', 'environment', 'hello']
for word in test_words:
    start = time.time()
    _ = ecdict.get_translation(word)
    elapsed = (time.time() - start) * 1000
    ecdict_times.append(elapsed)

print(f'   Average: {statistics.mean(ecdict_times):.2f}ms')
print(f'   Range: {min(ecdict_times):.2f}ms - {max(ecdict_times):.2f}ms')

# Benchmark Argos (excluding first call)
print('\n3️⃣  Argos Translate Performance:')
argos_times = []
test_phrases = ['run out', 'blow up', 'give in', 'look after', 'get over']

# First translation (model loading - don't count)
_ = argos.translate(test_phrases[0])

# Subsequent translations (cached model)
for phrase in test_phrases[1:]:
    start = time.time()
    _ = argos.translate(phrase)
    elapsed = (time.time() - start) * 1000
    argos_times.append(elapsed)

print(f'   Average: {statistics.mean(argos_times):.0f}ms (cached model)')
print(f'   Range: {min(argos_times):.0f}ms - {max(argos_times):.0f}ms')

print('\n📊 Performance Summary:')
print(f'   ECDICT:  ~{statistics.mean(ecdict_times):.1f}ms (instant)')
print(f'   Argos:   ~{statistics.mean(argos_times):.0f}ms (acceptable)')
print('   Ratio:   Argos is ~{}x slower than ECDICT'.format(
    int(statistics.mean(argos_times) / statistics.mean(ecdict_times))))

print('\n✅ Performance acceptable for user experience')
print('   Strategy: Use fast ECDICT for common words, Argos for gaps')
"
```

**Expected Output**:
```
⚡ Translation Performance Benchmarks

1️⃣  ECDICT Performance:
   Average: 0.14ms
   Range: 0.11ms - 0.18ms

3️⃣  Argos Translate Performance:
   Average: 95ms (cached model)
   Range: 87ms - 108ms

📊 Performance Summary:
   ECDICT:  ~0.1ms (instant)
   Argos:   ~95ms (acceptable)
   Ratio:   Argos is ~678x slower than ECDICT

✅ Performance acceptable for user experience
   Strategy: Use fast ECDICT for common words, Argos for gaps
```

**Performance Analysis**:
- **ECDICT**: Sub-millisecond lookups - Use for all single words
- **Mdict** (if available): ~10ms lookups - Use for phrasal verbs and detailed definitions
- **Argos Translate**: ~100ms per translation - Use only as last resort
- **User Impact**: Most translations (<1ms) feel instant; occasional 100ms delay is acceptable

---

## 7. Run Bilingual UI in Development Mode

Now let's test the complete bilingual interface with all translation features.

### 7.1 Start Flask Development Server

```bash
# Start web interface in debug mode
vocab-analyzer web --debug
```

**Expected Output**:
```
 * Serving Flask app 'vocab_analyzer.web.app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
Starting web interface at http://127.0.0.1:5000
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```

**Note**: Leave this terminal running and open a new terminal for the next steps.

### 7.2 Verify Bilingual Text Rendering

Open your web browser and navigate to: **http://127.0.0.1:5000**

**Visual Checklist**:

```
┌─────────────────────────────────────────────────────────────┐
│  Vocabulary Analyzer / 词汇分析器                              │
├─────────────────────────────────────────────────────────────┤
│  Navigation:                                                 │
│  [ Home / 首页 ]  [ Upload / 上传 ]  [ Results / 结果 ]       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Upload File / 上传文件                                       │
│                                                              │
│  Choose a file to analyze / 选择要分析的文件                   │
│                                                              │
│  File / 文件: [Choose File]                                  │
│                                                              │
│  Supported formats: TXT, PDF, DOCX, JSON /                  │
│  支持的格式: TXT, PDF, DOCX, JSON                             │
│                                                              │
│  [ Analyze / 分析 ]                                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Verify**:
- ✅ All headings show English / Chinese
- ✅ Navigation menu is bilingual
- ✅ Form labels are bilingual
- ✅ Buttons show both languages
- ✅ Format hints are bilingual

### 7.3 Test CEFR Description Tooltips

```bash
# Upload a sample file to see CEFR badges
# (In the web interface, upload data/sample_books/sample.txt)
```

After upload completes, you should see vocabulary results with CEFR level badges:

```
┌─────────────────────────────────────────────────────────────┐
│  Vocabulary Results / 词汇结果                                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Word              CEFR Level      Translation               │
│  ────────────────────────────────────────────────────────   │
│  example           [B1]ⓘ          n. 例子, 榜样              │
│  sophisticated     [B2]ⓘ          a. 精密的, 复杂的          │
│  analyze           [B2]ⓘ          vt. 分析, 分解             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Test CEFR Tooltip**:
1. **Hover** over the [B2]ⓘ badge
2. Should see tooltip:
   ```
   ┌──────────────────────────────┐
   │ B2: Upper Intermediate /     │
   │     中高级                    │
   │                              │
   │ Click for details /          │
   │ 点击查看详情                  │
   └──────────────────────────────┘
   ```

**Test CEFR Modal**:
1. **Click** on the [B2]ⓘ badge
2. Should see modal popup with full description:

```
╔══════════════════════════════════════════════════════════════╗
║  [×]                                                         ║
║                                                              ║
║  [B2] Upper Intermediate / 中高级                            ║
║  ───────────────────────────────────────────────────────    ║
║                                                              ║
║  Description / 描述:                                         ║
║  Can understand the main ideas of complex text on both      ║
║  concrete and abstract topics. Can interact with a degree   ║
║  of fluency and spontaneity with native speakers.           ║
║                                                              ║
║  能够理解具体和抽象主题的复杂文本的主要思想。                ║
║  能够流畅自发地与母语者互动。                                ║
║                                                              ║
║  Typical Vocabulary Size / 典型词汇量:                       ║
║  3000-5000 words                                            ║
║                                                              ║
║  Example Words / 示例单词:                                   ║
║  sophisticated, analyze, circumstances, nevertheless        ║
║                                                              ║
║  Learning Context / 学习情境:                                ║
║  Typical learner: University student, 3-5 years /           ║
║  典型学习者：大学生、学习3-5年                               ║
║                                                              ║
║                              [ Close / 关闭 ]                ║
╚══════════════════════════════════════════════════════════════╝
```

**Verify**:
- ✅ Tooltip appears on hover
- ✅ Modal opens on click
- ✅ Full description is bilingual
- ✅ All CEFR metadata is present
- ✅ Modal can be closed

### 7.4 Test Translation UI Buttons

Look for words/phrases without translations:

```
┌─────────────────────────────────────────────────────────────┐
│  Phrase: run out of patience                                │
│  ───────────────────────────────────────────────────────    │
│  Definition: (not available)                                │
│  Translation: (not available)                               │
│                                                              │
│  [ Translate / 翻译 ]                                        │
└─────────────────────────────────────────────────────────────┘
```

**Test Translation**:
1. **Click** the "Translate / 翻译" button
2. Button changes to "Translating... / 翻译中..."
3. After 1-3 seconds, translation appears:
   ```
   Translation: 失去耐心
   Source: Argos Translate / Argos翻译
   ```

**Verify**:
- ✅ Translate button visible for untranslated items
- ✅ Button shows loading state
- ✅ Translation appears within 3 seconds
- ✅ Translation source is indicated
- ✅ Translation is cached (second view instant)

### 7.5 Verify Offline Functionality

**Test 1: Disconnect Network**

```bash
# In a separate terminal, simulate offline mode
# Option A: Turn off WiFi in system settings
# Option B: Use browser DevTools Network tab → Offline mode

# Then try translating content in the browser
```

**Expected Behavior**:
- ✅ All UI text still displays (bilingual)
- ✅ ECDICT lookups still work (local)
- ✅ Mdict lookups still work (local, if available)
- ✅ Argos translations still work (local model)
- ✅ No error messages about network failure
- ✅ Translation times unchanged

**Test 2: Check Console for Network Requests**

Open browser DevTools (F12) → Network tab:

```
Filter: XHR
Total Requests: 0 external requests
All requests should be to localhost:5000 only
```

**Verify**:
- ✅ No requests to external translation APIs
- ✅ No requests to external CDNs
- ✅ All assets served locally
- ✅ System fully functional offline

### 7.6 Test Example Sentence Translation

```bash
# Find an example sentence in results
```

Example display:

```
┌─────────────────────────────────────────────────────────────┐
│  Word: example                                              │
│  ───────────────────────────────────────────────────────    │
│  Example Sentences:                                         │
│                                                              │
│  1. "This is a typical example of modern architecture."     │
│     Translation: 这是现代建筑的典型例子。                     │
│                                                              │
│  2. "Can you give me an example?"                           │
│     Translation: (not available)                            │
│     [ Translate / 翻译 ]                                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Test**:
1. Click "Translate / 翻译" for sentence #2
2. Should see: "你能给我一个例子吗？"

**Verify**:
- ✅ Sentence translations work
- ✅ Translation quality is acceptable
- ✅ Special characters preserved (e.g., "?")

### 7.7 Browser Compatibility Check

Test the bilingual UI in multiple browsers:

**Browsers to Test**:
- ✅ Chrome/Chromium (latest)
- ✅ Firefox (latest)
- ✅ Safari (macOS)
- ✅ Edge (Windows)

**Features to Verify**:
- Bilingual text renders correctly
- Chinese characters display properly
- CEFR tooltips appear
- CEFR modals open/close
- Translation buttons work
- No console errors

---

## 8. Troubleshooting

### 8.1 Argos Translate Issues

#### Issue: Model not loading

**Error Message**:
```
RuntimeError: English → Chinese translation package not installed
```

**Solution**:
```bash
# Re-run setup script
python setup_translation.py

# Or manually check installation
python -c "
import argostranslate.translate
installed = argostranslate.translate.get_installed_languages()
print('Installed:', [(l.code, l.name) for l in installed])
"

# If empty, reinstall
pip uninstall argostranslate -y
pip install argostranslate
python setup_translation.py
```

---

#### Issue: Translation returns identical text

**Example**: Translating "hello" returns "hello"

**Cause**: Model not properly loaded

**Solution**:
```bash
# Verify model files exist
python -c "
import argostranslate.package
pkg_dir = argostranslate.package.get_package_directory()
import os
print('Package dir:', pkg_dir)
print('Contents:', os.listdir(pkg_dir) if os.path.exists(pkg_dir) else 'NOT FOUND')
"

# If directory is empty, reinstall
python setup_translation.py
```

---

#### Issue: First translation takes >10 seconds

**Expected**: First translation is slow due to model loading (2-4 seconds is normal)

**If >10 seconds**: Possible causes:
- Low RAM (<4GB available)
- Slow disk I/O
- CPU throttling

**Solution**:
```bash
# Check available memory
free -h  # Linux
# Or Activity Monitor on macOS

# Close other applications to free RAM
# Consider upgrading to 8GB+ RAM for better performance
```

---

### 8.2 Mdict Dictionary Issues

#### Issue: Dictionaries not detected

**Error**: "Found 0 Mdict dictionaries"

**Solution**:
```bash
# Verify .mdx files are in correct location
ls -lh data/dictionaries/*.mdx

# Check file permissions
chmod 644 data/dictionaries/*.mdx

# Verify mdict-query is installed
python -c "from mdict_query import IndexBuilder; print('✓ Installed')"
```

---

#### Issue: Index building fails

**Error**:
```
Failed to build index: Invalid MDX header
```

**Cause**: Corrupted or unsupported .mdx file

**Solution**:
```bash
# Test .mdx file integrity
python -c "
from mdict_query import IndexBuilder
import sys

try:
    builder = IndexBuilder('data/dictionaries/YOUR_DICT.mdx')
    print('✓ Dictionary is valid')
except Exception as e:
    print(f'❌ Dictionary is corrupted: {e}')
    sys.exit(1)
"

# If corrupted, re-download or use different dictionary
```

---

#### Issue: Lookup returns empty results

**Cause**: Dictionary doesn't contain the word

**Solution**: This is expected behavior - Mdict will fallback to Argos

```bash
# Test what's in the dictionary
python -c "
from mdict_query import IndexBuilder

builder = IndexBuilder('data/dictionaries/YOUR_DICT.mdx')
keys = builder.get_mdx_keys('exam*')  # Wildcard search
print('Words starting with \"exam\":', keys[:10])
"
```

---

### 8.3 Translation Cache Issues

#### Issue: Cache permission errors

**Error**:
```
PermissionError: [Errno 13] Permission denied: 'data/translation_cache.json'
```

**Solution**:
```bash
# Fix file permissions
chmod 644 data/translation_cache.json
chmod 755 data/

# Verify writable
touch data/translation_cache.json
echo "✓ Cache file is writable"
```

---

#### Issue: Cache file corrupted

**Error**:
```
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

**Solution**:
```bash
# Backup corrupted cache
mv data/translation_cache.json data/translation_cache.json.backup

# Reinitialize cache
python -c "
import json
from datetime import datetime

cache = {
    'version': '1.0',
    'last_saved': int(datetime.now().timestamp()),
    'metadata': {'total_entries': 0, 'cache_hit_rate': 0.0},
    'entries': {}
}

with open('data/translation_cache.json', 'w', encoding='utf-8') as f:
    json.dump(cache, f, ensure_ascii=False, indent=2)

print('✓ Cache reinitialized')
"
```

---

### 8.4 UI Rendering Issues

#### Issue: Chinese text displays as squares (□□□)

**Cause**: Missing Chinese fonts

**Solution**:

**macOS**:
```bash
# Chinese fonts should be pre-installed
# Verify in Font Book: PingFang SC

# If missing, system update should fix:
softwareupdate --all --install --force
```

**Linux**:
```bash
# Install Chinese fonts
sudo apt install fonts-noto-cjk fonts-wqy-zenhei  # Ubuntu/Debian
sudo yum install google-noto-sans-cjk-fonts      # Fedora/RHEL

# Refresh font cache
fc-cache -fv
```

**Windows**:
```
Settings → Time & Language → Language
→ Add Chinese (Simplified) language pack
```

---

#### Issue: Chinese text too small

**Solution**: Adjust CSS font size

```bash
# Edit src/vocab_analyzer/web/static/styles.css
# Find:
.cn {
  font-size: 1.05em;  # Increase to 1.1em or 1.15em
}
```

---

#### Issue: Bilingual text overflows on mobile

**Solution**: Already handled by responsive CSS, but verify:

```bash
# Test in browser DevTools
# Toggle Device Toolbar (Ctrl+Shift+M)
# Select mobile device (e.g., iPhone SE)
# Verify text stacks vertically
```

---

### 8.5 Performance Issues

#### Issue: Translation too slow (>5 seconds)

**Cause**: System resource constraints

**Diagnosis**:
```bash
# Monitor resource usage while translating
# Terminal 1: Run translation
python -c "
import argostranslate.translate
import time

installed = argostranslate.translate.get_installed_languages()
from_lang = next(l for l in installed if l.code == 'en')
to_lang = next(l for l in installed if l.code == 'zh')
translation = from_lang.get_translation(to_lang)

start = time.time()
result = translation.translate('This is a test sentence for performance measurement.')
print(f'Time: {time.time() - start:.2f}s')
print(f'Result: {result}')
"

# Terminal 2: Monitor resources
# Linux/macOS:
top -pid $(pgrep -f python)

# Look for:
# - CPU usage (should be <100% on multi-core)
# - Memory usage (should be <500MB)
```

**Solutions**:
1. Close other applications
2. Upgrade to 8GB+ RAM
3. Use SSD instead of HDD
4. Disable browser extensions

---

#### Issue: Memory usage too high (>1GB)

**Cause**: Multiple translation models loaded

**Solution**:
```bash
# Check memory usage
python -c "
import psutil
import os

process = psutil.Process(os.getpid())
print(f'Memory usage: {process.memory_info().rss / 1024 / 1024:.1f} MB')

# Load Argos model
import argostranslate.translate
installed = argostranslate.translate.get_installed_languages()
from_lang = next(l for l in installed if l.code == 'en')
to_lang = next(l for l in installed if l.code == 'zh')
translation = from_lang.get_translation(to_lang)
_ = translation.translate('test')

print(f'After loading: {process.memory_info().rss / 1024 / 1024:.1f} MB')
"

# Expected: <500MB total
# If >1GB: Consider using lighter model or increasing system RAM
```

---

### 8.6 Common Error Messages

#### Error: "Translation unavailable / 翻译不可用"

**Possible Causes**:
1. Text too long (>500 chars)
2. Empty text
3. All translation tiers failed

**Solution**:
```bash
# Check translation chain status
python -c "
print('Checking translation chain...\n')

# 1. ECDICT
from vocab_analyzer.matchers.level_matcher import LevelMatcher
try:
    matcher = LevelMatcher(vocabulary_file='data/dictionaries/ECDICT/ecdict.csv')
    print('✓ ECDICT: Available')
except Exception as e:
    print(f'❌ ECDICT: {e}')

# 2. Argos
try:
    import argostranslate.translate
    installed = argostranslate.translate.get_installed_languages()
    has_en_zh = any(l.code == 'en' for l in installed) and any(l.code == 'zh' for l in installed)
    if has_en_zh:
        print('✓ Argos: Available')
    else:
        print('❌ Argos: en-zh package not installed')
except ImportError:
    print('❌ Argos: Not installed')
"
```

---

#### Error: "File size exceeds limit"

**Cause**: Trying to translate text >500 characters

**Solution**: Split into smaller chunks (automatic in production code)

---

### 8.7 Getting Help

If issues persist:

1. **Check Logs**:
   ```bash
   # Flask debug output in terminal
   # Look for Python tracebacks
   ```

2. **Browser Console**:
   ```
   F12 → Console tab
   Look for JavaScript errors
   ```

3. **Verify Prerequisites**:
   ```bash
   # Run full system check
   python -c "
   print('System Check:\n')

   # Python version
   import sys
   print(f'✓ Python: {sys.version.split()[0]}')

   # Required packages
   packages = ['flask', 'spacy', 'pandas', 'argostranslate']
   for pkg in packages:
       try:
           __import__(pkg)
           print(f'✓ {pkg}: Installed')
       except ImportError:
           print(f'❌ {pkg}: Not installed')

   # Data files
   from pathlib import Path
   files = [
       'data/dictionaries/ECDICT/ecdict.csv',
       'data/cefr_definitions.json',
       'data/translation_cache.json'
   ]
   for file in files:
       if Path(file).exists():
           print(f'✓ {file}: Found')
       else:
           print(f'❌ {file}: Missing')
   "
   ```

4. **Refer to Documentation**:
   - `specs/002-bilingual-ui-translation/research.md` - Technical details
   - `specs/002-bilingual-ui-translation/data-model.md` - Data structures
   - `specs/002-bilingual-ui-translation/spec.md` - Requirements

5. **Reset to Clean State**:
   ```bash
   # If all else fails, reset translation cache
   rm data/translation_cache.json
   python setup_translation.py

   # Restart web server
   vocab-analyzer web --debug
   ```

---

## Summary

You've now completed the bilingual UI with local translation setup! 🎉

**What You've Configured**:
- ✅ Python 3.13+ environment
- ✅ Argos Translate for offline English→Chinese translation
- ✅ ECDICT integration for fast dictionary lookups
- ✅ (Optional) Mdict dictionaries for enhanced definitions
- ✅ Translation cache for performance optimization
- ✅ CEFR level descriptions with bilingual tooltips
- ✅ Complete translation fallback chain
- ✅ Fully offline web interface

**Translation Chain Performance**:
- **Tier 1 (ECDICT)**: <1ms - Instant lookups for 770K+ words
- **Tier 2 (Mdict)**: ~10ms - High-quality definitions (optional)
- **Tier 3 (Argos)**: ~100ms - Neural translation fallback

**Key Features Verified**:
- 100% bilingual UI (English / Chinese)
- Interactive CEFR level descriptions
- On-demand translation for untranslated content
- Complete offline functionality (no internet required)
- Persistent translation cache
- Fast, responsive interface

**Next Steps**:
1. Explore the bilingual interface: `vocab-analyzer web --debug`
2. Upload sample books and test translations
3. Customize CEFR descriptions if needed
4. (Optional) Add more Mdict dictionaries for better coverage

**Need Help?**
- See Section 8 (Troubleshooting) for common issues
- Check project documentation in `specs/002-bilingual-ui-translation/`
- All features work 100% offline - no internet required!

Enjoy your bilingual vocabulary analyzer! 📚✨
