# Vocab Analyzer - 英文书词汇等级分析工具

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## English

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Production Ready](https://img.shields.io/badge/status-production%20ready-brightgreen.svg)](https://github.com/yourusername/vocab-analyzer)

A powerful CLI tool that analyzes English books and generates vocabulary lists organized by CEFR levels (A1-C2+) with Chinese translations, phrasal verb detection, and comprehensive statistics.

### 🎯 Key Features

- **Interactive Web Interface**: User-friendly web UI with real-time progress, filtering, and search
- **Multi-format Support**: Extract and analyze vocabulary from TXT, PDF, DOCX, and JSON files
- **CEFR Classification**: Classify words by 7 CEFR levels (A1, A2, B1, B2, C1, C2, C2+)
- **Phrasal Verb Detection**: Recognize 124+ common phrasal verbs, including separable forms
- **Chinese Translations**: Integrate 770K+ word ECDICT dictionary with Chinese definitions
- **Multiple Export Formats**: Export results in JSON, CSV, and Markdown formats
- **Statistical Analysis**: Comprehensive vocabulary distribution and insights
- **High Performance**: Process 100-page books in under 60 seconds
- **Beautiful CLI**: Rich terminal interface with progress bars and colored output

### 🌐 Bilingual UI & Translation

New translation capabilities have been added:
- **Bilingual Interface**: Simultaneous English/Chinese UI display
- **Offline Translation**: Three-tier translation (ECDICT → Mdict → Argos Translate)
- **CEFR Education**: Interactive level descriptions and learning guidance
- **Translation Caching**: Persistent cache for improved performance
- **Configurable**: YAML-based configuration for all translation settings

### 📦 Installation

#### Prerequisites

- Python 3.10 or higher
- pip package manager

#### Quick Start

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/vocab-analyzer.git
cd vocab-analyzer
```

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install the package**:
```bash
pip install -e .
```

4. **Download the spaCy language model**:
```bash
python -m spacy download en_core_web_sm
```

#### Development Installation

For development with additional tools:
```bash
pip install -e ".[dev]"
pre-commit install
```

### 🚀 Usage

#### Basic Commands

**Analyze a book** (generates all formats):
```bash
vocab-analyzer analyze book.txt
```

**View statistics only**:
```bash
vocab-analyzer stats book.txt
```

**Extract specific CEFR levels**:
```bash
vocab-analyzer extract book.txt --levels B2 C1
```

#### Advanced Usage

**Specify output format**:
```bash
# Single format
vocab-analyzer analyze book.txt --format json
vocab-analyzer analyze book.txt --format csv
vocab-analyzer analyze book.txt --format markdown

# Custom output path
vocab-analyzer analyze book.pdf --output results/my_vocab.json
```

**Filter by CEFR level**:
```bash
# Only B2-C1 words
vocab-analyzer analyze book.txt --min-level B2 --max-level C1

# Advanced words only (C1+)
vocab-analyzer analyze book.txt --min-level C1
```

**Batch processing**:
```bash
# Analyze multiple books
for book in books/*.txt; do
    vocab-analyzer analyze "$book" --output "results/$(basename "$book" .txt)_vocab.json"
done
```

#### Example Output

**Terminal Statistics**:
```
📚 Analyzing: pride_and_prejudice.txt
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%

📊 Vocabulary Analysis Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total words: 127,377
Unique words: 6,544
Unique phrases: 18

Level Distribution:
  A1 (KET)  ████████████░░░░░░░░  569 (8.7%)
  A2 (PET)  ██████████████░░░░░░  906 (13.8%)
  B1 (FCE)  ████████████████████  2,145 (32.8%)
  B2 (CAE)  ███████████████░░░░░  1,456 (22.3%)
  C1        ██████████░░░░░░░░░░  892 (13.6%)
  C2        ████░░░░░░░░░░░░░░░░  398 (6.1%)
  C2+ (超纲) ██░░░░░░░░░░░░░░░░░░  178 (2.7%)

✅ Output files generated:
  • pride_and_prejudice_vocabulary.json
  • pride_and_prejudice_vocabulary.csv
  • pride_and_prejudice_vocabulary_words.csv
  • pride_and_prejudice_vocabulary_phrases.csv
  • pride_and_prejudice_vocabulary.md

💡 Recommended for IELTS 6.5-7.5 level readers
```

#### 🌐 Web Interface

Launch the interactive web interface for a more user-friendly experience:

```bash
vocab-analyzer web
```

The web interface provides:
- **Drag-and-drop file upload** (TXT, PDF, DOCX)
- **Real-time progress tracking** with Server-Sent Events
- **Interactive results visualization**
  - Filter words by CEFR level (A1-C2+)
  - Search for specific words in real-time
  - Click words to see detailed information with Chinese translations
- **Visual statistics** with CEFR distribution charts
- **Multiple download formats** (JSON, CSV, Markdown)

**Access the interface at**: `http://127.0.0.1:5000`

**Custom port and debug mode**:
```bash
vocab-analyzer web --port 8080 --debug
```

**Browser requirements**: Modern browsers (Chrome, Firefox, Safari, Edge) with JavaScript enabled

### 🏗️ Architecture

#### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VocabularyAnalyzer                        │
│                    (Facade Pattern)                          │
└────────────┬────────────────────────────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
┌─────────┐      ┌─────────────┐
│ Config  │      │ Components  │
└─────────┘      └──────┬──────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
   ┌─────────┐    ┌──────────┐   ┌──────────┐
   │Extractor│    │Processor │   │ Matcher  │
   └─────────┘    └──────────┘   └──────────┘
        │               │               │
        ▼               ▼               ▼
   ┌─────────┐    ┌──────────┐   ┌──────────┐
   │Analyzer │    │Exporter  │   │   CLI    │
   └─────────┘    └──────────┘   └──────────┘
```

#### Design Patterns

1. **Facade Pattern**: `VocabularyAnalyzer` provides a simplified interface to complex subsystems
2. **Strategy Pattern**: Multiple extractors (TXT, PDF, DOCX) and exporters (JSON, CSV, MD)
3. **Singleton Pattern**: Shared spaCy model instance for performance
4. **Factory Pattern**: Dynamic extractor selection based on file type
5. **Template Method**: `BaseExtractor` abstract class for common extraction logic
6. **Dependency Injection**: Configuration-driven component initialization

#### Core Components

**1. Text Extractors** (`src/vocab_analyzer/extractors/`)
- `TxtExtractor`: Plain text files (UTF-8)
- `PdfExtractor`: PDF documents (PyPDF2)
- `DocxExtractor`: Word documents (python-docx)
- `JsonExtractor`: Structured JSON data

**2. NLP Processors** (`src/vocab_analyzer/processors/`)
- `Tokenizer`: spaCy-based tokenization, lemmatization, POS tagging
- `PhraseDetector`: Dependency parsing for phrasal verb detection

**3. Level Matcher** (`src/vocab_analyzer/matchers/`)
- CEFR level classification (43,699 classified words)
- Oxford 3000 marker integration
- Frequency-based level inference
- LRU cache for fast lookups (10,000 entries)

**4. Analyzers** (`src/vocab_analyzer/analyzers/`)
- `StatisticsAnalyzer`: Comprehensive vocabulary statistics
- Level distribution calculation
- Frequency analysis

**5. Exporters** (`src/vocab_analyzer/exporters/`)
- `JsonExporter`: Structured JSON with metadata
- `CsvExporter`: Excel-compatible CSV (separate word and phrase files)
- `MarkdownExporter`: Human-readable Markdown reports

#### Data Flow

```
Input File
    │
    ▼
┌─────────────────┐
│ Text Extraction │ → Raw text
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ NLP Processing  │ → Tokens (lemmatized, POS-tagged)
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Phrase Detection│ → Phrasal verbs identified
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Level Matching  │ → CEFR levels assigned
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Statistics      │ → Analysis results
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Export          │ → JSON/CSV/Markdown files
└─────────────────┘
```

### 📂 Project Structure

```
vocab-analyzer/
├── src/vocab_analyzer/          # Source code
│   ├── models/                  # Data models
│   ├── extractors/              # Text extraction
│   ├── processors/              # NLP processing
│   ├── matchers/                # Level matching
│   ├── analyzers/               # Statistics
│   ├── exporters/               # Output formats
│   ├── core/                    # Core logic
│   ├── cli/                     # CLI interface
│   ├── web/                     # Web interface
│   ├── translation/             # Translation components
│   └── utils/                   # Utilities
├── data/                        # Data resources
│   ├── vocabularies/            # CEFR wordlists
│   ├── phrases/                 # Phrasal verbs
│   ├── dictionaries/            # Dictionaries
│   ├── sample_books/            # Sample texts
│   └── mappings/                # CEFR-IELTS mapping
├── tests/                       # Test suite
│   ├── conftest.py             # Test fixtures
│   ├── unit/                   # Unit tests
│   └── integration/            # Integration tests
├── scripts/                     # Utility scripts
│   ├── prepare_data.py         # Data preparation
│   └── validate_data.py        # Data validation
├── config/                      # Configuration
│   └── default_config.yaml     # Default settings
├── docs/                        # Documentation
│   ├── USER_GUIDE.md           # User guide
│   ├── EXAMPLES.md             # Examples
│   └── QUICK_REFERENCE.md      # Quick reference
├── requirements.txt             # Dependencies
├── setup.py                     # Package setup
└── README.md                    # This file
```

### 📊 Performance

**Benchmarks** (tested on MacBook Pro M1):
- Small files (<5 pages): ~2 seconds
- Medium files (20-50 pages): ~15 seconds
- Large files (100+ pages): <60 seconds
- Memory usage: <400MB peak

**Optimizations**:
- Global spaCy model loading (Singleton pattern)
- LRU cache for word/phrase lookups (10,000 entries)
- Batch processing (100 sentences per batch)
- pandas DataFrame indexing

### 🗂️ Data Sources

This project uses the following open-source data:

| Resource | Size | License | Source |
|----------|------|---------|--------|
| **ECDICT** | 770,608 words | MIT | [skywind3000/ECDICT](https://github.com/skywind3000/ECDICT) |
| **Phrasal Verbs** | 124 verbs | Open Source | [Semigradsky/phrasal-verbs](https://github.com/Semigradsky/phrasal-verbs) |
| **Sample Books** | 3 books | Public Domain | [Project Gutenberg](https://www.gutenberg.org/) |

### 🧪 Development

#### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=vocab_analyzer --cov-report=html

# Run specific test
pytest tests/unit/test_word.py -v

# Run with verbose output
pytest -vv
```

#### Code Quality

```bash
# Format code
black src/ tests/
isort src/ tests/

# Check code style
flake8 src/ tests/
pylint src/ --rcfile=.pylintrc

# Type checking
mypy src/
```

#### Pre-commit Hooks

```bash
# Install hooks (runs on every commit)
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

### ⚙️ Configuration

Default configuration is in `config/default_config.yaml`. Override with custom config:

```bash
vocab-analyzer analyze book.txt --config my_config.yaml
```

**Key configuration options**:
- NLP model and batch size
- Data file paths (dictionaries, wordlists)
- Output formats and templates
- Analysis parameters (min frequency, level thresholds)
- Logging level and format

### 🗺️ Roadmap

#### ✅ Phase 1: MVP (v0.1.0 - Completed)
- [x] Multi-format text extraction (TXT, PDF, DOCX, JSON)
- [x] CEFR level classification (A1-C2+)
- [x] Phrasal verb detection (124 verbs)
- [x] Chinese translations (770K+ words)
- [x] Multiple export formats (JSON, CSV, Markdown)
- [x] CLI with rich formatting
- [x] Comprehensive statistics
- [x] Web interface (Flask/FastAPI)

#### 🔄 Phase 2: Enhancements (Planned)
- [ ] Expand phrasal verb dictionary (500+ verbs)
- [ ] Advanced example sentence extraction
- [ ] Anki deck export format
- [ ] Batch processing mode

#### 🚀 Phase 3: Advanced Features (Future)
- [ ] Progress tracking and learning analytics
- [ ] Custom wordlist support
- [ ] Audio pronunciation integration
- [ ] Multi-language support (French, German, Spanish)
- [ ] Mobile application

### 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 🙏 Acknowledgments

- **ECDICT** for the comprehensive English-Chinese dictionary
- **spaCy** for powerful NLP processing
- **Project Gutenberg** for public domain books
- All open-source contributors

### 📞 Support

For issues, questions, or suggestions:
- 📖 Check [USER_GUIDE.md](docs/USER_GUIDE.md) for detailed usage
- 📝 Review [EXAMPLES.md](docs/EXAMPLES.md) for practical examples
- 🐛 Open an issue on GitHub
- 💬 Join discussions in GitHub Discussions

---

<a name="中文"></a>
## 中文

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: 生产就绪](https://img.shields.io/badge/status-%E7%94%9F%E4%BA%A7%E5%B0%B1%E7%BB%AA-brightgreen.svg)](https://github.com/yourusername/vocab-analyzer)

一个强大的命令行工具，可以分析英文书籍并生成按CEFR等级（A1-C2+）分类的词汇表，包含中文翻译、词组识别和全面的统计分析。

### 🎯 核心功能

- **多格式支持**：从TXT、PDF、DOCX、JSON文件中提取和分析词汇
- **CEFR分级**：将单词分为7个CEFR等级（A1, A2, B1, B2, C1, C2, C2+）
- **词组识别**：识别124+个常用动词短语，包括可分离形式
- **中文翻译**：集成770K+词条的ECDICT词典，提供中文释义
- **多种导出格式**：支持JSON、CSV、Markdown格式导出
- **统计分析**：全面的词汇分布和洞察
- **高性能**：100页书籍处理时间小于60秒
- **精美CLI**：丰富的终端界面，带进度条和彩色输出

### 📦 安装

#### 系统要求

- Python 3.10 或更高版本
- pip 包管理器

#### 快速开始

1. **克隆仓库**：
```bash
git clone https://github.com/yourusername/vocab-analyzer.git
cd vocab-analyzer
```

2. **创建虚拟环境**（推荐）：
```bash
python -m venv venv
source venv/bin/activate  # Windows系统: venv\Scripts\activate
```

3. **安装包**：
```bash
pip install -e .
```

4. **下载spaCy语言模型**：
```bash
python -m spacy download en_core_web_sm
```

#### 开发环境安装

包含额外开发工具的安装：
```bash
pip install -e ".[dev]"
pre-commit install
```

### 🚀 使用方法

#### 基本命令

**分析一本书**（生成所有格式）：
```bash
vocab-analyzer analyze book.txt
```

**仅查看统计信息**：
```bash
vocab-analyzer stats book.txt
```

**提取特定CEFR等级**：
```bash
vocab-analyzer extract book.txt --levels B2 C1
```

#### 高级用法

**指定输出格式**：
```bash
# 单一格式
vocab-analyzer analyze book.txt --format json
vocab-analyzer analyze book.txt --format csv
vocab-analyzer analyze book.txt --format markdown

# 自定义输出路径
vocab-analyzer analyze book.pdf --output results/my_vocab.json
```

**按CEFR等级过滤**：
```bash
# 仅B2-C1单词
vocab-analyzer analyze book.txt --min-level B2 --max-level C1

# 仅高级词汇（C1+）
vocab-analyzer analyze book.txt --min-level C1
```

**批量处理**：
```bash
# 分析多本书
for book in books/*.txt; do
    vocab-analyzer analyze "$book" --output "results/$(basename "$book" .txt)_vocab.json"
done
```

#### 示例输出

**终端统计**：
```
📚 正在分析: 傲慢与偏见.txt
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%

📊 词汇分析完成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
总词数: 127,377
独立单词: 6,544
词组数量: 18

等级分布:
  A1 (KET)  ████████████░░░░░░░░  569 (8.7%)
  A2 (PET)  ██████████████░░░░░░  906 (13.8%)
  B1 (FCE)  ████████████████████  2,145 (32.8%)
  B2 (CAE)  ███████████████░░░░░  1,456 (22.3%)
  C1        ██████████░░░░░░░░░░  892 (13.6%)
  C2        ████░░░░░░░░░░░░░░░░  398 (6.1%)
  C2+ (超纲) ██░░░░░░░░░░░░░░░░░░  178 (2.7%)

✅ 已生成输出文件:
  • pride_and_prejudice_vocabulary.json
  • pride_and_prejudice_vocabulary.csv
  • pride_and_prejudice_vocabulary_words.csv
  • pride_and_prejudice_vocabulary_phrases.csv
  • pride_and_prejudice_vocabulary.md

💡 推荐给雅思6.5-7.5分水平的读者
```

### 🏗️ 系统架构

#### 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                    VocabularyAnalyzer                        │
│                    (外观模式)                                 │
└────────────┬────────────────────────────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
┌─────────┐      ┌─────────────┐
│ 配置    │      │ 核心组件    │
└─────────┘      └──────┬──────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
   ┌─────────┐    ┌──────────┐   ┌──────────┐
   │文本提取 │    │NLP处理   │   │等级匹配  │
   └─────────┘    └──────────┘   └──────────┘
        │               │               │
        ▼               ▼               ▼
   ┌─────────┐    ┌──────────┐   ┌──────────┐
   │统计分析 │    │格式导出  │   │ CLI界面  │
   └─────────┘    └──────────┘   └──────────┘
```

#### 设计模式

1. **外观模式**：`VocabularyAnalyzer`为复杂子系统提供简化接口
2. **策略模式**：多种提取器（TXT、PDF、DOCX）和导出器（JSON、CSV、MD）
3. **单例模式**：共享spaCy模型实例以提升性能
4. **工厂模式**：根据文件类型动态选择提取器
5. **模板方法**：`BaseExtractor`抽象类定义通用提取逻辑
6. **依赖注入**：配置驱动的组件初始化

#### 核心组件

**1. 文本提取器**（`src/vocab_analyzer/extractors/`）
- `TxtExtractor`：纯文本文件（UTF-8）
- `PdfExtractor`：PDF文档（PyPDF2）
- `DocxExtractor`：Word文档（python-docx）
- `JsonExtractor`：结构化JSON数据

**2. NLP处理器**（`src/vocab_analyzer/processors/`）
- `Tokenizer`：基于spaCy的分词、词形还原、词性标注
- `PhraseDetector`：依存句法分析进行动词短语检测

**3. 等级匹配器**（`src/vocab_analyzer/matchers/`）
- CEFR等级分类（43,699个已分类单词）
- Oxford 3000标记集成
- 基于频率的等级推断
- LRU缓存快速查询（10,000条）

**4. 统计分析器**（`src/vocab_analyzer/analyzers/`）
- `StatisticsAnalyzer`：全面的词汇统计
- 等级分布计算
- 频率分析

**5. 格式导出器**（`src/vocab_analyzer/exporters/`）
- `JsonExporter`：带元数据的结构化JSON
- `CsvExporter`：Excel兼容的CSV（单词和词组分离文件）
- `MarkdownExporter`：人类可读的Markdown报告

#### 数据流程

```
输入文件
    │
    ▼
┌─────────────────┐
│ 文本提取        │ → 原始文本
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ NLP处理         │ → 词元（词形还原、词性标注）
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ 词组检测        │ → 识别动词短语
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ 等级匹配        │ → 分配CEFR等级
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ 统计分析        │ → 分析结果
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ 格式导出        │ → JSON/CSV/Markdown文件
└─────────────────┘
```

### 📂 项目结构

```
vocab-analyzer/
├── src/vocab_analyzer/          # 源代码（3,930行）
│   ├── models/                  # 数据模型
│   │   ├── word.py             # Word数据类（126行）
│   │   ├── phrase.py           # Phrase数据类（150行）
│   │   └── analysis.py         # VocabularyAnalysis（267行）
│   ├── extractors/              # 文本提取（374行）
│   │   ├── base.py             # BaseExtractor抽象类
│   │   ├── txt_extractor.py    # TXT文件支持
│   │   ├── pdf_extractor.py    # PDF文件支持
│   │   ├── docx_extractor.py   # DOCX文件支持
│   │   └── json_extractor.py   # JSON文件支持
│   ├── processors/              # NLP处理（530行）
│   │   ├── tokenizer.py        # 分词和词形还原
│   │   └── phrase_detector.py  # 动词短语检测
│   ├── matchers/                # 等级匹配（416行）
│   │   └── level_matcher.py    # CEFR分类
│   ├── analyzers/               # 统计分析（254行）
│   │   └── statistics.py       # 统计分析
│   ├── exporters/               # 输出格式（483行）
│   │   ├── json_exporter.py    # JSON导出
│   │   ├── csv_exporter.py     # CSV导出
│   │   └── markdown_exporter.py# Markdown导出
│   ├── core/                    # 核心逻辑（549行）
│   │   ├── analyzer.py         # VocabularyAnalyzer外观
│   │   └── config.py           # 配置管理
│   ├── cli/                     # CLI界面（231行）
│   │   └── main.py             # 基于Click的CLI
│   └── utils/                   # 工具函数（550行）
│       ├── file_utils.py       # 文件操作
│       ├── text_utils.py       # 文本处理
│       └── cache.py            # 缓存工具
├── data/                        # 数据资源（~205MB）
│   ├── vocabularies/            # CEFR词汇表
│   │   └── cefr_wordlist.csv   # 43,699个已分类单词
│   ├── phrases/                 # 动词短语
│   │   └── phrasal_verbs.csv   # 124个常用动词
│   ├── dictionaries/            # 词典
│   │   └── ECDICT/             # 770,608词条
│   ├── sample_books/            # 样例文本（3本书）
│   └── mappings/                # CEFR-雅思映射
├── tests/                       # 测试套件（165行）
│   ├── conftest.py             # 测试固件
│   ├── unit/                   # 单元测试
│   └── integration/            # 集成测试
├── scripts/                     # 工具脚本（400+行）
│   ├── prepare_data.py         # 数据准备
│   └── validate_data.py        # 数据验证
├── config/                      # 配置文件
│   └── default_config.yaml     # 默认设置
├── docs/                        # 文档（107KB+）
│   ├── USER_GUIDE.md           # 用户指南（15KB）
│   ├── EXAMPLES.md             # 示例（16KB）
│   └── QUICK_REFERENCE.md      # 快速参考（5.6KB）
├── requirements.txt             # 依赖项
├── setup.py                     # 包安装
└── README.md                    # 本文件
```

### 📊 性能指标

**基准测试**（在MacBook Pro M1上测试）：
- 小文件（<5页）：约2秒
- 中文件（20-50页）：约15秒
- 大文件（100+页）：<60秒
- 内存使用：<400MB峰值

**性能优化**：
- 全局spaCy模型加载（单例模式）
- 单词/词组查询LRU缓存（10,000条）
- 批量处理（每批100句）
- pandas DataFrame索引优化

### 🗂️ 数据来源

本项目使用以下开源数据：

| 资源 | 规模 | 许可证 | 来源 |
|------|------|--------|------|
| **ECDICT** | 770,608词 | MIT | [skywind3000/ECDICT](https://github.com/skywind3000/ECDICT) |
| **Phrasal Verbs** | 124个动词 | 开源 | [Semigradsky/phrasal-verbs](https://github.com/Semigradsky/phrasal-verbs) |
| **样例书籍** | 3本书 | 公有领域 | [Project Gutenberg](https://www.gutenberg.org/) |

### 🧪 开发

#### 运行测试

```bash
# 运行所有测试
pytest

# 带覆盖率报告
pytest --cov=vocab_analyzer --cov-report=html

# 运行特定测试
pytest tests/unit/test_word.py -v

# 详细输出
pytest -vv
```

#### 代码质量

```bash
# 格式化代码
black src/ tests/
isort src/ tests/

# 检查代码风格
flake8 src/ tests/
pylint src/ --rcfile=.pylintrc

# 类型检查
mypy src/
```

#### Pre-commit钩子

```bash
# 安装钩子（每次提交时运行）
pre-commit install

# 手动运行所有文件
pre-commit run --all-files
```

### ⚙️ 配置

默认配置在`config/default_config.yaml`。使用自定义配置覆盖：

```bash
vocab-analyzer analyze book.txt --config my_config.yaml
```

**关键配置选项**：
- NLP模型和批处理大小
- 数据文件路径（词典、词汇表）
- 输出格式和模板
- 分析参数（最小频率、等级阈值）
- 日志级别和格式

### 🗺️ 路线图

#### ✅ 第一阶段：MVP（v0.1.0 - 已完成）
- [x] 多格式文本提取（TXT、PDF、DOCX、JSON）
- [x] CEFR等级分类（A1-C2+）
- [x] 动词短语检测（124个动词）
- [x] 中文翻译（770K+单词）
- [x] 多种导出格式（JSON、CSV、Markdown）
- [x] 带丰富格式的CLI
- [x] 全面的统计分析

#### 🔄 第二阶段：功能增强（计划中）
- [ ] 扩展动词短语词典（500+动词）
- [ ] 高级例句提取
- [ ] Anki卡组导出格式
- [ ] Web界面（Flask/FastAPI）
- [ ] 批量处理模式

#### 🚀 第三阶段：高级功能（未来）
- [ ] 进度跟踪和学习分析
- [ ] 自定义词汇表支持
- [ ] 音频发音集成
- [ ] 多语言支持（法语、德语、西班牙语）
- [ ] 移动应用

### 🤝 贡献

欢迎贡献！请查看[CONTRIBUTING.md](CONTRIBUTING.md)了解指南。

1. Fork本仓库
2. 创建功能分支（`git checkout -b feature/AmazingFeature`）
3. 提交更改（`git commit -m 'Add some AmazingFeature'`）
4. 推送到分支（`git push origin feature/AmazingFeature`）
5. 开启Pull Request

### 📄 许可证

本项目采用MIT许可证 - 详见[LICENSE](LICENSE)文件。

### 🙏 致谢

- **ECDICT** 提供全面的英汉词典
- **spaCy** 提供强大的NLP处理
- **Project Gutenberg** 提供公有领域书籍
- 所有开源贡献者

### 📞 支持

如有问题、建议或疑问：
- 📖 查看[USER_GUIDE.md](docs/USER_GUIDE.md)了解详细用法
- 📝 查看[EXAMPLES.md](docs/EXAMPLES.md)了解实践示例
- 🐛 在GitHub上提交issue
- 💬 在GitHub Discussions中参与讨论

---

**注意**：这是一个个人学习工具，旨在帮助英语学习者分析书籍中的词汇。仅供教育目的使用。

**开发团队** | **MIT License** | **v0.1.0**
